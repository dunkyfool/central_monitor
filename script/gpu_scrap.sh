#!/bin/bash

# Declare
FILE=test/log
TIME=`head -n1 ${FILE}`
VERSION=`head -n3 ${FILE} | tail -n1 | cut -d' ' -f3`

# Parser
function gpu_parser {
	for LINE in 9 12 15 18 21 24 27 30
	do
		GPU=`head -n${LINE}  ${FILE} | tail -n2`
		GPU_NO=`echo ${GPU} | cut -d'|' -f2 | cut -d' ' -f2`
		GPU_FAN=`echo ${GPU} | cut -d'|' -f6 | cut -d' ' -f2`
		GPU_TEMP=`echo ${GPU} | cut -d'|' -f6 | cut -d' ' -f3`
		GPU_PWR=`echo ${GPU} | cut -d'|' -f6 | cut -d' ' -f5`
		GPU_MAX_PWR=`echo ${GPU} | cut -d'|' -f6 | cut -d' ' -f7`
		GPU_MEM=`echo ${GPU} | cut -d'|' -f7 | cut -d' ' -f2`
		GPU_MAX_MEM=`echo ${GPU} | cut -d'|' -f7 | cut -d' ' -f4`
		GPU_UTIL=`echo ${GPU} | cut -d '|' -f8 | cut -d' ' -f2`
		
		echo "node_gpu_metrics{instance=${GPU_NO}, content=\"GPU_FAN\"} ${GPU_FAN}"
		echo "node_gpu_metrics{instance=${GPU_NO}, content=\"GPU_TEMP\"} ${GPU_TEMP}"
		echo "node_gpu_metrics{instance=${GPU_NO}, content=\"GPU_MEM\"} ${GPU_MEM}"
		echo "node_gpu_metrics{instance=${GPU_NO}, content=\"GPU_MAX_MEM\"} ${GPU_MAX_MEM}"
		echo "node_gpu_metrics{instance=${GPU_NO}, content=\"GPU_PWR\"} ${GPU_PWR}"
		echo "node_gpu_metrics{instance=${GPU_NO}, content=\"GPU_MAX_PWR\"} ${GPU_MAX_PWR}"
		echo "node_gpu_metrics{instance=${GPU_NO}, content=\"GPU_UTIL\"} ${GPU_UTIL}"
	done
}

echo ${TIME}
echo ${VERSION}
gpu_parser
