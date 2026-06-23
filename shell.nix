{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  packages = [
    pkgs.python3
    pkgs.python3Packages.kivy
    pkgs.python3Packages.pudb
    pkgs.python3Packages.selenium
    pkgs.python3Packages.numpy
    pkgs.chromedriver
    pkgs.chromium
  ];
  shellHook = ''
    export CHROME_PATH="${pkgs.chromium}/bin/chromium"
    export CHROMEDRIVER_PATH="${pkgs.chromedriver}/bin/chromedriver"
  '';
}
