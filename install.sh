#!/usr/bin/env bash

mkdir -p backup

cp /usr/share/X11/xkb/symbols/us backup/us
cp /usr/share/X11/xkb/symbols/level5 backup/level5
sudo cp keyboard-layout-files/pkl-us /usr/share/X11/xkb/symbols/us
sudo cp keyboard-layout-files/pkl-level5 /usr/share/X11/xkb/symbols/level5

echo Log out and log back in to complete the installation
