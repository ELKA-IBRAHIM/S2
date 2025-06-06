{ stdenv
, fetchzip
, lib
, python3
}:
let
  customPython = python3.withPackages ( ps:
    with ps; [
      netifaces aiohttp aiofiles jinja2 qrcode
    ]
  );
in
stdenv.mkDerivation rec {
  pname = "typst-serve-watch";
  version = "0.1";

  srcs = [
    (lib.fileset.toSource {
      root = ./.;
      fileset = lib.fileset.unions [
        ./server.py ./preview.html.j2
      ];
    })
    (fetchzip {
      url = "https://github.com/mozilla/pdf.js/releases/download/v2.16.105/pdfjs-2.16.105-dist.zip";
      sha256 = "sha256-WHgbkIsIWMs5HfEgN7laRkWQvAWHq+YT8/s5Y2/PFpA=";
      stripRoot = false;
      name = "pdfjs";
    })
  ];

  sourceRoot = ".";

  installPhase = ''
    mkdir -p "$out/share"
    install -Dm 755 source/server.py "$out/share/server.py"
    install -Dm 644 source/preview.html.j2 "$out/share/preview.html.j2"

    cp -r ./pdfjs $out/share
    find $out/share/pdfjs -type f -exec chmod 644 {} \;
    find $out/share/pdfjs -type d -exec chmod 755 {} \;

    mkdir -p $out/bin
    cat > $out/bin/${pname} <<EOF
    #!${stdenv.shell}
    exec ${customPython}/bin/python $out/share/server.py --template $out/share/preview.html.j2 --pdfjs-folder $out/share/pdfjs "\$@"
    EOF
    chmod 755 $out/bin/${pname}
  '';

  meta = with lib; {
    description = ''GUI automation Python module for human beings'';
    homepage = "https://github.com/asweigart/pyautogui";
    license = licenses.bsd3;
    maintainers = [ "Scott Hamilton <sgn.hamilton+nixpkgs@protonmail.com>" ];
    platforms = platforms.linux;
  };
}
