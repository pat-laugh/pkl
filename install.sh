#!/usr/bin/env bash

mkdir -p .install_files
./generate_install.py >.install_files/run.sh
. .install_files/run.sh
