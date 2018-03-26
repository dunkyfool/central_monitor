#!/bin/bash

URL="localhost:3000/api/dashboards/db"
USER="admin"
PASS="admin"
JSON="Content-type: application/json"

PAGEONE=`cat ../conf/grafana_dashboard_template/curl/page_one.json `
curl -s -X POST ${URL} -u ${USER}:${PASS} -H "${JSON}" -d "${PAGEONE}" | python -m json.tool

for ID in $(seq 1 3);
do
	MINER=`cat ../conf/grafana_dashboard_template/curl/miner_status.json | sed "s/Miner 1/Miner ${ID}/g"`
	curl -s -X POST ${URL} -u ${USER}:${PASS} -H "${JSON}" -d "${MINER}" | python -m json.tool
done
