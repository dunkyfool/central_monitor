#!/bin/bash

DIR=/home/dunkyfool
TWO=2

for idx in {1..8};
do
	NO_IDX=$((TWO*idx-1))
	FREQ_IDX=$((TWO*idx))
	GPU_NO=`cat ${DIR}/freq.csv | cut -d',' -f ${NO_IDX}`
	GPU_FREQ=`cat ${DIR}/freq.csv | cut -d',' -f ${FREQ_IDX}`
	sh /opt/central_monitor/script/setFreq.sh ${GPU_NO} ${GPU_FREQ}
done
