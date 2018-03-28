#!/bin/bash

# Declare
FILE=/opt/central_monitor/txt/log
LOG=/opt/central_monitor/txt/gpu_metrics.prom
ETH=/opt/central_monitor/txt/gpu.log

# Parser
function gpu_parser {
	rm -f ${LOG} ${FILE}

	IP=`ifconfig | grep -A1 enp6s0 | grep -o inet.*Bcast | cut -d' ' -f2 | tr -d 'addr:'`
	MHS=`tac ${ETH} | head -n5 | grep ETH -m1 | cut -c26- | tr -d 'GPUMh/s' | tr -s ' '`
	REBOOT=`last reboot | grep ^reboot | tr -s ' ' | awk -F' ' '{print $6 $7}' | sort | uniq -c | grep $(LANG=en_us_88591 date +%b%d) | tr -s ' ' | cut -d ' ' -f2`
	if [ "${REBOOT}" = "" ]; then
		REBOOT=0
	fi
	echo "node_gpu_metrics{ip=\"${IP}\", content=\"DAILY_REBOOT_COUNT\"} ${REBOOT}" >> ${LOG}

	for LINE in 0 1 2 3 4 5 6 7
	do
		nvidia-smi -i ${LINE} > ${FILE} 

		TIME=`head -n1 ${FILE}`
		VERSION=`head -n3 ${FILE} | tail -n1 | cut -d' ' -f3`

		echo ${TIME}
		echo ${VERSION}
		echo ${IP}
		echo ${MHS}

		if [ "${VERSION}" != "384.111" ]; then
			GPU_NO=${LINE}
			echo "node_gpu_metrics{devid=\"${GPU_NO}\", ip=\"${IP}\", content=\"GPU_FAN\"} 0" >> ${LOG}
			echo "node_gpu_metrics{devid=\"${GPU_NO}\", ip=\"${IP}\", content=\"GPU_TEMP\"} 0" >> ${LOG}
			echo "node_gpu_metrics{devid=\"${GPU_NO}\", ip=\"${IP}\", content=\"GPU_MEM\"} 0" >> ${LOG}
			echo "node_gpu_metrics{devid=\"${GPU_NO}\", ip=\"${IP}\", content=\"GPU_MAX_MEM\"} 6075" >> ${LOG}
			echo "node_gpu_metrics{devid=\"${GPU_NO}\", ip=\"${IP}\", content=\"GPU_PWR\"} 0" >> ${LOG}
			echo "node_gpu_metrics{devid=\"${GPU_NO}\", ip=\"${IP}\", content=\"GPU_MAX_PWR\"} 120" >> ${LOG}
			echo "node_gpu_metrics{devid=\"${GPU_NO}\", ip=\"${IP}\", content=\"GPU_UTIL\"} 0" >> ${LOG}
			echo "node_gpu_metrics{devid=\"${GPU_NO}\", ip=\"${IP}\", content=\"GPU_STATUS\"} 0" >> ${LOG}
			echo "node_gpu_metrics{devid=\"${GPU_NO}\", ip=\"${IP}\", content=\"GPU_MHS\"} 0" >> ${LOG}
		else

			GPU=`head -n9  ${FILE} | tail -n2`
			GPU_NO=${LINE}
			GPU_FAN=`echo ${GPU} | cut -d'|' -f6 | cut -d' ' -f2 | sed 's/.$//'`
			GPU_TEMP=`echo ${GPU} | cut -d'|' -f6 | cut -d' ' -f3 | sed 's/.$//'`
			GPU_PWR=`echo ${GPU} | cut -d'|' -f6 | cut -d' ' -f5 | sed 's/.$//'`
			GPU_MAX_PWR=`echo ${GPU} | cut -d'|' -f6 | cut -d' ' -f7 | sed 's/.$//'`
			GPU_MEM=`echo ${GPU} | cut -d'|' -f7 | cut -d' ' -f2 | sed 's/...$//'`
			GPU_MAX_MEM=`echo ${GPU} | cut -d'|' -f7 | cut -d' ' -f4 | sed 's/...$//'`
			GPU_UTIL=`echo ${GPU} | cut -d '|' -f8 | cut -d' ' -f2 | sed 's/.$//'`
			GPU_MHS=`echo ${MHS} | cut -d ',' -f $((LINE+1)) | cut -c4-`

			if [ "${GPU_MHS}" = "" ];then
				GPU_MHS=0
			fi
			
			echo "node_gpu_metrics{devid=\"${GPU_NO}\", ip=\"${IP}\", content=\"GPU_FAN\"} ${GPU_FAN}" >> ${LOG}
			echo "node_gpu_metrics{devid=\"${GPU_NO}\", ip=\"${IP}\", content=\"GPU_TEMP\"} ${GPU_TEMP}" >> ${LOG}
			echo "node_gpu_metrics{devid=\"${GPU_NO}\", ip=\"${IP}\", content=\"GPU_MEM\"} ${GPU_MEM}" >> ${LOG}
			echo "node_gpu_metrics{devid=\"${GPU_NO}\", ip=\"${IP}\", content=\"GPU_MAX_MEM\"} ${GPU_MAX_MEM}" >> ${LOG}
			echo "node_gpu_metrics{devid=\"${GPU_NO}\", ip=\"${IP}\", content=\"GPU_PWR\"} ${GPU_PWR}" >> ${LOG}
			echo "node_gpu_metrics{devid=\"${GPU_NO}\", ip=\"${IP}\", content=\"GPU_MAX_PWR\"} ${GPU_MAX_PWR}" >> ${LOG}
			echo "node_gpu_metrics{devid=\"${GPU_NO}\", ip=\"${IP}\", content=\"GPU_UTIL\"} ${GPU_UTIL}" >> ${LOG}
			echo "node_gpu_metrics{devid=\"${GPU_NO}\", ip=\"${IP}\", content=\"GPU_STATUS\"} 1" >> ${LOG}
			echo "node_gpu_metrics{devid=\"${GPU_NO}\", ip=\"${IP}\", content=\"GPU_MHS\"} ${GPU_MHS}" >> ${LOG}

		fi
	done
}

gpu_parser
