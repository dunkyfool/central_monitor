#!/bin/bash

# Declare
FILE=/opt/central_monitor/txt/log
LOG=/opt/central_monitor/txt/gpu_metrics.prom
TIME=`head -n1 ${FILE}`
VERSION=`head -n3 ${FILE} | tail -n1 | cut -d' ' -f3`

# Parser
function gpu_parser {
	rm -f ${LOG}
	for LINE in 9 12 15 18 21 24 27 30
	do
		GPU=`head -n${LINE}  ${FILE} | tail -n2`
		GPU_NO=`echo ${GPU} | cut -d'|' -f2 | cut -d' ' -f2`
		GPU_FAN=`echo ${GPU} | cut -d'|' -f6 | cut -d' ' -f2 | sed 's/.$//'`
		GPU_TEMP=`echo ${GPU} | cut -d'|' -f6 | cut -d' ' -f3 | sed 's/.$//'`
		GPU_PWR=`echo ${GPU} | cut -d'|' -f6 | cut -d' ' -f5 | sed 's/.$//'`
		GPU_MAX_PWR=`echo ${GPU} | cut -d'|' -f6 | cut -d' ' -f7 | sed 's/.$//'`
		GPU_MEM=`echo ${GPU} | cut -d'|' -f7 | cut -d' ' -f2 | sed 's/...$//'`
		GPU_MAX_MEM=`echo ${GPU} | cut -d'|' -f7 | cut -d' ' -f4 | sed 's/...$//'`
		GPU_UTIL=`echo ${GPU} | cut -d '|' -f8 | cut -d' ' -f2 | sed 's/.$//'`
		
		echo "node_gpu_metrics{devid=\"${GPU_NO}\", content=\"GPU_FAN\"} ${GPU_FAN}" >> ${LOG}
		echo "node_gpu_metrics{devid=\"${GPU_NO}\", content=\"GPU_TEMP\"} ${GPU_TEMP}" >> ${LOG}
		echo "node_gpu_metrics{devid=\"${GPU_NO}\", content=\"GPU_MEM\"} ${GPU_MEM}" >> ${LOG}
		echo "node_gpu_metrics{devid=\"${GPU_NO}\", content=\"GPU_MAX_MEM\"} ${GPU_MAX_MEM}" >> ${LOG}
		echo "node_gpu_metrics{devid=\"${GPU_NO}\", content=\"GPU_PWR\"} ${GPU_PWR}" >> ${LOG}
		echo "node_gpu_metrics{devid=\"${GPU_NO}\", content=\"GPU_MAX_PWR\"} ${GPU_MAX_PWR}" >> ${LOG}
		echo "node_gpu_metrics{devid=\"${GPU_NO}\", content=\"GPU_UTIL\"} ${GPU_UTIL}" >> ${LOG}
	done
}

echo ${TIME}
echo ${VERSION}
gpu_parser
