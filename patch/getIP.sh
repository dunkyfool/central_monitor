#!/bin/bash

USER=ethos
PASS=digitalespacio

sshpass -p ${PASS} ssh ${USER}@192.168.88.${1} -o StrictHostKeyChecking=no ifconfig -a | grep -Po 'HWaddr \K.*$'
#sshpass -p udsn806u ssh ryan@localhost -o StrictHostKeyChecking=no ifconfig -a | grep -Po 'HWaddr \K.*$'
