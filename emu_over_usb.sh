#!/bin/bash
set -x

device="$1"
echo "$device"
if [[ $device == "" ]]
then
    echo "Run with /dev/sdx or /path/to/something.iso"
    exit 1
fi

if [ "$EUID" -ne 0 ]
  then echo "Run as root"
  exit 2
fi

rmmod g_multi
cd /sys/kernel/config/
cd usb_gadget
mkdir g1
cd g1
echo "0x316d" > idVendor
echo "0x4c05" > idProduct
echo "0xEF" > bDeviceClass
echo "0x02" > bDeviceSubClass
echo "0x01" > bDeviceProtocol
mkdir strings/0x409
echo "0123456789" > strings/0x409/serialnumber
echo "Purism, SPC" > strings/0x409/manufacturer
echo "Librem 5" > strings/0x409/product
mkdir functions/ecm.usb0
mkdir functions/acm.GS0
mkdir functions/mass_storage.0
mkdir configs/c.1
mkdir configs/c.1/strings/0x409
echo "CDC ACM+ECM" > configs/c.1/strings/0x409/configuration
echo "$device" > functions/mass_storage.0/lun.0/file
echo "Librem 5" > functions/mass_storage.0/lun.0/inquiry_string
ln -s functions/acm.GS0 configs/c.1
ln -s functions/ecm.usb0 configs/c.1
ln -s functions/mass_storage.0 configs/c.1
echo "38100000.usb" > UDC
