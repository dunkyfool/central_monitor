#!/bin/bash

MAC=`ifconfig | grep enp6s0 | grep -oE HWaddr.+ | cut -d' ' -f2`
CAM="b8:2a:72:f5:4d:d8"

if [ "${MAC}" = "${CAM}" ]; then
	echo "[INFO] Machine ${HOSTNAME} is verified!"
else
	echo "[ERROR] Machine ${HOSTNAME} is not verified!"
	exit 1
fi
