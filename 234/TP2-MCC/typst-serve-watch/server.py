import os
import argparse
import qrcode
import subprocess
import asyncio
import signal
import sys
import socket
import netifaces
from aiohttp import web
import aiofiles
from jinja2 import Template
from typing import Dict, Set, Optional, List

DEFAULT_PORT = 27717

class AppState:
    def __init__(self):
        self.websockets: Set[web.WebSocketResponse] = set()
        self.typst_proc: Optional[subprocess.Popen] = None
        self.last_status: Optional[str] = None
        self.last_logs: Optional[str] = None
        self.watch_task: Optional[asyncio.Task] = None
        self.logs_buffer: List[str] = []
        self.in_logs_buffer: bool = False
        self.logs_block_past_first_empty_line: bool = False

async def watch_typst(state: AppState):
    proc = await asyncio.create_subprocess_shell(
        "nix run .#watch",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True
    )

    state.typst_proc = proc
    buffer = ""

    try:
        while True:
            chunk = await proc.stderr.read(1024)
            if not chunk:
                break

            chunk = chunk.decode('utf-8')
            buffer += chunk

            while '\n' in buffer:
                line, buffer = buffer.split('\n', 1)
                line = line.strip()

                if "compiled successfully" in line:
                    state.last_status = 'success'
                    state.in_logs_buffer = False
                    state.logs_buffer = []
                    print("Update detected - sending to clients")
                    await notify_clients(state, 'update')
                elif "compiled with errors" in line:
                    state.last_status = 'error'
                    state.in_logs_buffer = True
                    state.logs_block_past_first_empty_line = False
                    state.logs_buffer = [line]
                elif "compiled with warnings" in line:
                    state.last_status = 'warning'
                    state.in_logs_buffer = True
                    state.logs_block_past_first_empty_line = False
                    state.logs_buffer = [line]
                elif state.in_logs_buffer:
                    state.logs_buffer.append(line)
                    if not line.strip():  # Empty line indicates error block end
                        if not state.logs_block_past_first_empty_line:
                            state.logs_block_past_first_empty_line = True
                        else:
                            state.last_logs = '\n'.join(state.logs_buffer)
                            await notify_clients(state, state.last_status)
                            state.in_logs_buffer = False
    except asyncio.CancelledError:
        pass
    finally:
        if proc.returncode is None:
            proc.terminate()
            try:
                await asyncio.wait_for(proc.wait(), timeout=1.0)
            except (asyncio.TimeoutError, subprocess.TimeoutExpired):
                proc.kill()

async def notify_clients(state: AppState, event_type: str):
    for ws in set(state.websockets):
        try:
            if event_type == 'update':
                await ws.send_json({'type': 'update'})
            elif event_type == 'error' or event_type == 'warning':
                await ws.send_json({
                    'type': event_type,
                    'message': state.last_logs
                })
        except ConnectionError:
            state.websockets.discard(ws)

async def websocket_handler(request: web.Request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    request.app['state'].websockets.add(ws)

    try:
        async for msg in ws:
            if msg.type == web.WSMsgType.TEXT and msg.data == 'get_pdf':
                if os.path.exists('main.pdf'):
                    async with aiofiles.open('main.pdf', 'rb') as f:
                        await ws.send_bytes(await f.read())
    finally:
        request.app['state'].websockets.discard(ws)
    return ws

async def handle_client_html(request: web.Request):
    print("[DEBUG] GET client received, sending preview.html")
    return web.Response(
        text=request.app["preview_html"],
        content_type='text/html'
    )

async def on_startup(app: web.Application):
    app['state'] = AppState()
    state: AppState = app['state']
    state.watch_task = asyncio.create_task(watch_typst(state))

async def on_shutdown(app: web.Application):
    state: AppState = app['state']

    # Close all WebSocket connections
    close_tasks = [ws.close() for ws in set(state.websockets)]
    await asyncio.gather(*close_tasks, return_exceptions=True)

    # Cancel watch task
    if state.watch_task:
        state.watch_task.cancel()
        try:
            await state.watch_task
        except asyncio.CancelledError:
            pass

def get_local_ips():
    """Get all active local IP addresses"""
    ips = []
    try:
        hostname = socket.gethostname()
        # Get all IP addresses associated with the host
        all_ips = socket.getaddrinfo(hostname, None)

        # Filter IPv4 addresses that aren't loopback
        for ip in all_ips:
            if ip[0] == socket.AF_INET:  # IPv4 only
                addr = ip[4][0]
                if not addr.startswith('127.'):
                    ips.append(addr)

        # Also check network interfaces directly
        import netifaces
        for interface in netifaces.interfaces():
            addrs = netifaces.ifaddresses(interface)
            if netifaces.AF_INET in addrs:
                for link in addrs[netifaces.AF_INET]:
                    if 'addr' in link and not link['addr'].startswith('127.'):
                        if link['addr'] not in ips:
                            ips.append(link['addr'])
    except Exception as e:
        print(f"Could not detect all IPs: {e}")
        # Fallback to basic detection
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ips.append(s.getsockname()[0])
            s.close()
        except:
            ips.append('localhost')

    return ips or ['localhost']


async def serve(runner: web.AppRunner):
    await runner.setup()
    port = runner.app["args"].port
    site = web.TCPSite(runner, '0.0.0.0', port)
    print(f"Server started, listening on port {port}")
    await site.start()
    await asyncio.Event().wait()

def print_terminal_qr(url: str):
    """Generate and print QR code to terminal"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=4,  # Smaller for better terminal display
        border=1,
    )
    qr.add_data(url)
    qr.make(fit=True)

    print("\n\x1b[1;34mScan this QR code to connect to the server:\x1b[0m")
    qr.print_ascii(tty=True)
    print(f"\n\x1b[1;32mOr open in browser: {url}\x1b[0m\n")

def parse_args():
    parser = argparse.ArgumentParser(description='Typst Watch Server for building and serving the PDF')
    parser.add_argument('--template', type=str,
                        default='./preview.html.j2',
                        help='Path to the Jinja2 preview.html.j2 template file')
    parser.add_argument('--pdfjs-folder', type=str,
                        default='./pdfjs',
                        help='Path to the pdfjs folder (PDF.js from Mozilla)')
    parser.add_argument('--port', type=int,
                        default=DEFAULT_PORT,
                        help='Port number to listen to')
    return parser.parse_args()

def main():
    args = parse_args()
    port = args.port
    # Configure event loop policy
    if sys.version_info >= (3, 10):
        asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())

    local_ips = get_local_ips()
    for ip in local_ips:
        print(f"Server starting at http://{ip}:{port}")

    app = web.Application()
    app["args"] = args
    with open(args.template, 'r') as file:
        template = Template(file.read())
        print(f"[DEBUG] using template file `{args.template}`")
        ip = local_ips[0] if len(local_ips) > 0 else "localhost"
        app["preview_html"] = template.render(host=ip, port=port)
        url = f"http://{ip}:{port}"
        print_terminal_qr(url)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    # Setup routes
    app.router.add_get('/', handle_client_html)
    app.router.add_get('/ws', websocket_handler)
    app.router.add_static('/pdfjs', path=args.pdfjs_folder)  # For serving PDFs

    runner = web.AppRunner(app)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        # Start server
        server_task = loop.create_task(serve(runner))

        # Signal handling
        if sys.platform != 'win32':
            loop.add_signal_handler(signal.SIGINT, lambda: server_task.cancel())
            loop.add_signal_handler(signal.SIGTERM, lambda: server_task.cancel())

        loop.run_until_complete(server_task)
    except (asyncio.CancelledError, KeyboardInterrupt):
        print("\nShutting down server...")
    finally:
        # Proper cleanup sequence
        loop.run_until_complete(app.shutdown())
        loop.run_until_complete(runner.cleanup())
        loop.close()

if __name__ == '__main__':
    main()
