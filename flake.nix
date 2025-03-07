{
  inputs = {
    artiq.url = "git+https://github.com/m-labs/artiq.git?ref=release-8&rev=431c415423e709178263d3463f8c4ab905e9b796";
    nixpkgs.follows = "artiq/nixpkgs";
  };

  outputs = { self, artiq, nixpkgs }:
    let
      pkgs = import nixpkgs { system = "x86_64-linux"; };
      # Combine attribute sets for convenience
      artiq-full = artiq.packages.x86_64-linux;

      makeArtiqBoardPackage = variant: artiq.makeArtiqBoardPackage {
        target = "kasli";
        variant = variant;
        buildCommand = 
          "python -m artiq.gateware.targets.kasli ${./firmware}/${variant}.json";
      };

      makeVariantDDB = variant: pkgs.runCommand "ddb-${variant}"  
      {
        buildInputs = [
          artiq.devShells.x86_64-linux.boards.buildInputs
        ];
      }
      ''
      mkdir -p $out
      artiq_ddb_template ${./firmware}/${variant}.json -o $out/device_db.py
      '';

    in rec
    {
      # Default shell for `nix develop`
      devShells.x86_64-linux.default = pkgs.mkShell {
        buildInputs = [
          # Python packages
          (pkgs.python3.withPackages (ps: [
            # From the artiq flake
            artiq-full.artiq
            artiq-full.misoc
            ps.pillow
          ]))
          # Non-Python packages
          artiq-full.openocd-bscanspi # needed for flashing boards, also provides proxy bitstreams
        ];
      };
      packages.x86_64-linux.default = pkgs.buildEnv{
        name="oshqe";
        paths = devShells.x86_64-linux.default.buildInputs;
      };
      packages.x86_64-linux = {
        pw2502001 = makeArtiqBoardPackage "pw2502001";

        ddb_pw2502001 = makeVariantDDB "pw2502001";
      };
    };

  # Settings to enable substitution from the M-Labs servers (avoiding local builds)
  nixConfig = {
    extra-trusted-public-keys = [
      "nixbld.m-labs.hk-1:5aSRVA5b320xbNvu30tqxVPXpld73bhtOeH6uAjRyHc="
    ];
    extra-substituters = [ "https://nixbld.m-labs.hk" ];
    sandbox = false;
  };
}
