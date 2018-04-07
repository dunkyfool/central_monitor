#!/bin/bash

DIR=/home/ethos
TWO=2

#reboot
touch /var/log/wtmp

# ip -> minerid -> freq
IP=`ifconfig  | grep -oE addr:.*B | tr -d 'addr: B'`
MINERID=`curl -s "central_monitor:8080/?mac=${IP}"| tr -d 'miner{}'`
FREQ=`curl -s "central_monitor:8080/?miner=${MINERID}"`

#setFreq
for idx in {1..8};
do
	NO_IDX=$((TWO*idx-1))
	FREQ_IDX=$((TWO*idx))
	GPU_NO=`cat ${DIR}/freq.csv | cut -d',' -f ${NO_IDX}`
	GPU_FREQ=`cat ${DIR}/freq.csv | cut -d',' -f ${FREQ_IDX}`
	sh /opt/central_monitor/script/setFreq.sh ${GPU_NO} ${GPU_FREQ}
done
