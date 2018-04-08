#!/bin/bash

PASS=digitalespacio
IP=${1}

if [ "${IP}" = "" ]; then
  echo "Enter IP"
  exit 0
fi

sshpass -p ${PASS} scp -o StrictHostKeyChecking=no -r /opt/central_monitor ethos@${1}:/home/ethos/
sshpass -p ${PASS} ssh -o StrictHostKeyChecking=no ethos@${1} sh /home/ethos/central_monitor/update/copy2opt.sh
sshpass -p ${PASS} ssh -o StrictHostKeyChecking=no ethos@${1} sh /home/ethos/central_monitor/update/updateHost.sh
sshpass -p ${PASS} ssh -o StrictHostKeyChecking=no ethos@${1} sh /home/ethos/central_monitor/update/freshCrontab.sh

