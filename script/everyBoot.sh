#!/bin/bash

DIR=/home/ethos
FILE=freq.csv
PASS=digitalespacio
TWO=2

#reboot
echo ${PASS} | sudo -E touch /var/log/wtmp

# ip -> minerid -> freq
IP=`ifconfig  | grep -oE addr:.*B | tr -d 'addr: B'`
MINERID=`curl -s "central_monitor:8080/ip/?id=${IP}"| tr -d 'miner{}'`
curl -s "central_monitor:8080/miner/?id=${MINERID}" | python -m json.tool | grep dev | tr -d 'dev_" ,frq' | sed 's/:/,/g; s/$/,/g' | tr -d '\n' > ${DIR}/${FILE}

OUTPUT=`cat ${DIR}/${FILE}`
echo ${IP} ${MINERID} ${OUTPUT}

#setFreq
for idx in $(seq 1 8)
do
	NO_IDX=$((TWO*idx-1))
	FREQ_IDX=$((TWO*idx))
	GPU_NO=`cat ${DIR}/${FILE} | cut -d',' -f ${NO_IDX}`
	GPU_FREQ=`cat ${DIR}/${FILE} | cut -d',' -f ${FREQ_IDX}`
	sh /opt/central_monitor/script/setFreq.sh ${GPU_NO} ${GPU_FREQ}
done
