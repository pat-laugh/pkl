#!/usr/bin/env bash

mkdir -p .install_files
./generate_uninstall.py >.install_files/run.sh
. .install_files/run.sh
