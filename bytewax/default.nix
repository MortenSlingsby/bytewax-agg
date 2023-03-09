final: prev:
let
  packageOverrides = python-final: python-prev: {
    bytewax = prev.callPackage ./bytewax.nix  { inherit (python-prev) buildPythonPackage fetchPypi lib
      dill multiprocess; };
  };
in {
  python3 = prev.python3.override { inherit packageOverrides; };
}
