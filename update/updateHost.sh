#!/bin/bash

PASS=digitalespacio
IP=192.168.88.215

echo ${PASS} | sudo -E cp /etc/hosts /tmp/hosts

if `grep -q central_monitor /tmp/hosts`
then 
   sed -i "s/$(grep central /tmp/hosts)/${IP} central_monitor/g" /tmp/hosts
else
   echo "${IP} central_monitor" > /tmp/hosts
fi

echo ${PASS} | sudo -E cp /tmp/hosts /etc/hosts
