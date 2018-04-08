#!/bin/bash

PASS=digitalespacio

echo $PASS | sudo -S echo "* * * * * sh /opt/central_monitor/script/node_exp.sh opt" >> mycron
echo $PASS | sudo -S echo "* * * * * bash /opt/central_monitor/script/gpu_scrap.sh" >> mycron
echo $PASS | sudo -S crontab mycron
echo $PASS | sudo -S rm mycron
