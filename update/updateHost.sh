#!/bin/bash

PASS=digitalespacio
IP=192.168.88.215

echo ${PASS} | sudo -E cp /etc/hosts hosts
echo ${PASS} | sudo -E chown ethos:ethos hosts

if `grep -q central_monitor hosts`
then 
   sed -i "s/$(grep central hosts)/${IP} central_monitor/g" hosts
else
   echo "${IP} central_monitor" >> hosts
fi

echo ${PASS} | sudo -E cp hosts /etc/hosts
