#!/bin/bash

curl -XPOST -H 'content-type: application/json' localhost:8080/REBOOT -d '{"commonLabels": {"instance":"miner12:9100", "alertname":"LoseGPU", "devid": "0"}}'
curl -XPOST -H 'content-type: application/json' localhost:8080/REBOOT -d '{"commonLabels": {"instance":"miner12:9100", "alertname":"LoseGPU", "devid": "0"}}'

nvidia-settings -q all |grep -i GPUCurrentClockFreqsString
