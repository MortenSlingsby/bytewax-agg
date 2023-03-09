{
  description = "bytewax";

  nixConfig.flake-registry ="https://raw.githubusercontent.com/bkkp/flake-registry/main/flake-registry.json";

  outputs = {
    self,
    nixpkgs,
  }@inputs:
  let

    pkgs = import nixpkgs {
      system = "x86_64-linux";
      overlays = [
        self.overlays.bytewax
       ];
    };

  in {
    overlays.bytewax = import ./bytewax;

    devShells."x86_64-linux".default = pkgs.mkShell rec {
      packages = with pkgs; [
        glow
        python3.pkgs.bytewax
        python3.pkgs.kafka-python
        python3.pkgs.pandas
      ];
      shellHook = ''
          export LD_LIBRARY_PATH="${pkgs.lib.makeLibraryPath packages}:$LD_LIBRARY_PATH"
          export LD_LIBRARY_PATH="${pkgs.stdenv.cc.cc.lib.outPath}/lib:$LD_LIBRARY_PATH"
          export PYTHONPATH=$PWD:$PYTHONPATH
        '';
    };

  };
}
