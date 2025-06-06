{ description = "A Typst project";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    localShamilton.url = "github:SCOTT-HAMILTON/nur-packages";

    typix = {
      url = "github:loqusion/typix";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    flake-utils.url = "github:numtide/flake-utils";

    # Example of downloading icons from a non-flake source
    # font-awesome = {
    #   url = "github:FortAwesome/Font-Awesome";
    #   flake = false;
    # };
  };

  outputs = inputs @ {
    nixpkgs,
    typix,
    flake-utils,
    localShamilton,
    ...
  }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = nixpkgs.legacyPackages.${system};
      inherit (pkgs) lib;

      typixLib = typix.lib.${system};

      src = typixLib.cleanTypstSource ./.;
      commonArgs = {
        typstSource = "main.typ";

        fontPaths = [
          # Add paths to fonts here
          # "${pkgs.roboto}/share/fonts/truetype"
        ];

        virtualPaths = [
          # Add paths that must be locally accessible to typst here
          # {
          #   dest = "icons";
          #   src = "${inputs.font-awesome}/svgs/regular";
          # }
        ];
      };

      # Compile a Typst project, *without* copying the result
      # to the current directory
      build-drv = typixLib.buildTypstProject (commonArgs
        // {
          inherit src;
        });

      # Compile a Typst project, and then copy the result
      # to the current directory
      build-local-drv = typixLib.buildTypstProjectLocal (commonArgs
        // {
          inherit src;
        });

      # Watch a project and recompile on changes
      watch-script-drv = typixLib.watchTypstProject commonArgs;
      typst-serve-watch-drv = pkgs.callPackage ./typst-serve-watch {};

      vscodium-drv = pkgs.runCommand "vscodium-with-tinymist" {
        buildInputs = [ pkgs.makeWrapper ];
        inherit (pkgs.vscodium) meta;
      } ''
        mkdir -p $out/bin
        makeWrapper ${pkgs.vscodium}/bin/codium $out/bin/codium \
          --prefix PATH : "${pkgs.tinymist}/bin"
      '';
      
      make-demo-drv = with pkgs; stdenv.mkDerivation rec {
        pname = "make-demo";
        version = "1.0";

        propagatedBuildInputs = [
          pdftk
          poppler_utils
          coreutils
          xmlstarlet
        ];
        dontUnpack = true;

        installPhase = ''
          mkdir -p $out/bin
          cat > $out/bin/${pname} <<EOF
          #!${stdenv.shell}
          tmp=\$(mktemp -d)
          rm main.pdf
          nix develop --command bash -c "typst compile main.typ"
          ${pdftk}/bin/pdftk main.pdf cat 1 output \$tmp/page1.pdf
          ${poppler_utils}/bin/pdftocairo -svg \$tmp/page1.pdf demo/doc.svg
          rm -rf \$tmp
          ${xmlstarlet}/bin/xmlstarlet ed -L \
              -i "/*[local-name()='svg']/*[1]" -t elem -n "rect" \
              -s "/*[local-name()='svg']/rect[1]" -t attr -n "width" -v "100%" \
              -s "/*[local-name()='svg']/rect[1]" -t attr -n "height" -v "100%" \
              -s "/*[local-name()='svg']/rect[1]" -t attr -n "fill" -v "white" \
              demo/doc.svg
          EOF
          chmod +x $out/bin/${pname}
        '';
      };
    in {
      checks = {
        inherit build-drv build-local-drv watch-script-drv;
      };

      packages.default = build-drv;

      apps = rec {
        default = watch;
        build = flake-utils.lib.mkApp {
          drv = build-drv;
        };
        build-local = flake-utils.lib.mkApp {
          drv = build-local-drv;
        };
        watch = flake-utils.lib.mkApp {
          drv = watch-script-drv;
        };
        typst-serve-watch = flake-utils.lib.mkApp {
          drv = typst-serve-watch-drv;
        };
        jupyter-lab = flake-utils.lib.mkApp {
          drv = pkgs.jupyter;
          exePath = "/bin/jupyter-lab";
        };
        vscodium = flake-utils.lib.mkApp {
          drv = vscodium-drv;
          exePath = "/bin/codium";
        };
        make-demo = flake-utils.lib.mkApp {
          drv = make-demo-drv;
        };
      };

      devShells.default = typixLib.devShell {
        inherit (commonArgs) fontPaths virtualPaths;

        packages = with pkgs; [
          (python3.withPackages (ps: with ps; [
            jupyter
            ipython
            localShamilton.packages."${system}".pyfemm
            numpy
            scipy
            matplotlib
            numba
            pandas
            jinja2
            tqdm
            aiohttp
            aiofiles
            netifaces
          ]))
          wineWowPackages.stable
          # vscodium
          vscode
          tinymist
          # jetbrains.pycharm-community
          # WARNING: Don't run `typst-build` directly, instead use `nix run .#build`
          # See https://github.com/loqusion/typix/issues/2
          # build-script
          watch-script-drv
          # More packages can be added here, like typstfmt
          # pkgs.typstfmt
        ];
      };
    });
}
