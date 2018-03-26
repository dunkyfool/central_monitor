#!/bin/bash

URL="localhost:3000"
USER="admin"
PASS="admin"
JSON="Content-type: application/json"

PAGEONE="/conf/grafana_dashboard_template/UI/page_one.json"
MINER="/conf/grafana_dashboard_template/UI/miner_status.json"

curl -s ${URL} -u ${USER}:${PASS} -H ${JSON} -d @${PAGEONE} | python -m json.tool
curl -s ${URL} -u ${USER}:${PASS} -H ${JSON} -d @${MINER} | python -m json.tool
