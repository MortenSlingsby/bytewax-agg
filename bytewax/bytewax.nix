{ buildPythonPackage, fetchPypi, lib, dill, multiprocess }:

buildPythonPackage rec {
  pname = "bytewax";
  version = "0.15.1";
  format = "wheel";

  src = fetchPypi {
    inherit version pname format;
    sha256 = "sha256-ThWYrvz8rncXitvUw0NEj/TtdPLLCeohPkDoRVnP5kI=";
    python = "cp310";
    dist = "cp310";
    abi = "cp310";
    platform = "manylinux_2_31_x86_64";
  };

  propagatedBuildInputs = [
    dill
    multiprocess
  ];

  doCheck = true;
}
