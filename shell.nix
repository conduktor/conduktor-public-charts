# Nix dev shell for conduktor ctl project
# if nix installed you can smply run `nix-shell` to enter the dev shell
# if nix-direnv is installed, just add `use nix` in your .envrc file
{ pkgs ? import <nixpkgs> {} }:
let
  unstableTarball = builtins.fetchTarball https://github.com/NixOS/nixpkgs/archive/nixos-unstable.tar.gz;
  pkgs = import <nixpkgs> {};
  unstable = import unstableTarball {};

  shell = pkgs.mkShell {
    buildInputs = [
      pkgs.k3d
      pkgs.kubernetes-helm
      pkgs.kubeconform
      pkgs.pre-commit
     (pkgs.python3.withPackages (python-pkgs: with python-pkgs; [
          click
          pydantic
          pyyaml
          rich
          gitpython
      ]))
     ];
  };
in shell
