#!/bin/bash
set -e

if [ "$#" -ne 2 ]; then
    echo "Usage: upload.sh <device> <install_odroid_go>"
    echo "Example: upload.sh /dev/ttyUSB0 true"
    exit 1
fi

DEVICE=$1
INSTALL_ODROID_GO=$2

if [ "$INSTALL_ODROID_GO" = true ] ; then
    echo "Installing ODROID-GO MicroPython library"
    rm -rf ODROID-GO-MicroPython/odroid_go/examples
    rshell --buffer-size 32 -a -p $DEVICE rsync ODROID-GO-MicroPython/odroid_go /flash/odroid_go
fi

echo "Uploading files to $DEVICE"
rshell --buffer-size 32 -a -p $DEVICE cp src/boot.py src/ui.py /flash/
rshell --buffer-size 32 -a -p $DEVICE cp imgs/flame.bmp imgs/water.bmp /flash/imgs/

echo "Connecting to $DEVICE REPL"
echo "Press Ctrl+D to reboot the device and Ctrl+X to exit"
rshell --buffer-size 32 -a -p $DEVICE repl
