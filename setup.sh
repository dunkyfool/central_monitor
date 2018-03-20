#!/bin/bash


if [ "$1" = "ini" ]; then
  echo "Make binary file executable!!"
  chmod +x bin/node_exporter bin/prometheus 
  echo "##################"
  echo "#     CHECK      #"
  echo "##################"
  ls -l bin

elif [ "$1" = "shortlist" ]; then
  echo "ini pro node gui remove"
  
elif [ "$1" = "pro" ]; then
  # prometheus.service
  read -p "Please Enter User Password: " PASS
  echo "[Info] Setup prometheus"
  echo $PASS | sudo -S cp conf/prometheus.service /etc/systemd/system/
  echo $PASS | sudo -S systemctl enable prometheus
  echo $PASS | sudo -S systemctl daemon-reload
  echo $PASS | sudo -S systemctl start prometheus
  echo $PASS | sudo -S crontab -l > mycron
  echo $PASS | sudo -S echo "* * * * * sh /opt/central_monitor/script/node_exp.sh pro" >> mycron
  echo $PASS | sudo -S crontab mycron
  echo $PASS | sudo -S rm mycron
  echo "##################"
  echo "#     CHECK      #"
  echo "##################"
  echo $PASS | sudo -S systemctl status prometheus
  echo $PASS | sudo -S crontab -l

elif [ "$1" = "node" ]; then
  # node_exporter.service
  read -p "Please Enter User Password: " PASS
  echo "[Info] Setup node exporter"
  echo $PASS | sudo -S cp conf/node_exporter.service /etc/systemd/system/
  echo $PASS | sudo -S systemctl enable node_exporter
  echo $PASS | sudo -S systemctl daemon-reload
  echo $PASS | sudo -S systemctl start node_exporter
  echo $PASS | sudo -S crontab -l > mycron
  echo $PASS | sudo -S echo "* * * * * sh /opt/central_monitor/script/node_exp.sh opt" >> mycron
  echo $PASS | sudo -S echo "* * * * * bash /opt/central_monitor/script/gpu_scrap.sh" >> mycron
  echo $PASS | sudo -S crontab mycron
  echo $PASS | sudo -S rm mycron
  echo "##################"
  echo "#     CHECK      #"
  echo "##################"
  echo $PASS | sudo -S systemctl status node_exporter
  echo $PASS | sudo -S crontab -l

elif [ "$1" = "gui" ]; then
  # grafana-server.service
  read -p "Please Enter User Password: " PASS
  echo "[Info] Setup Grafana"
  echo $PASS | sudo -S dpkg -i grafana/adduser_3.113+nmu3ubuntu4_all.deb
  echo $PASS | sudo -S dpkg -i grafana/fontconfig-config_2.11.94-0ubuntu1.1_all.deb
  echo $PASS | sudo -S dpkg -i grafana/grafana_5.0.1_amd64.deb
  echo $PASS | sudo -S cp conf/grafana.ini /etc/grafana/
  echo $PASS | sudo -S cp conf/grafana-server.service /usr/lib/systemd/system/
  echo $PASS | sudo -S systemctl enable grafana-server
  echo $PASS | sudo -S systemctl daemon-reload
  echo $PASS | sudo -S systemctl start grafana-server
  echo "##################"
  echo "#     CHECK      #"
  echo "##################"
  echo $PASS | sudo -S systemctl status grafana-server

elif [ "$1" = "remove" ]; then
  # remove central monitor
  read -p "Please Enter User Password: " PASS
  echo $PASS | sudo -S systemctl stop node_exporter -f
  echo $PASS | sudo -S systemctl stop prometheus -f
  echo $PASS | sudo -S systemctl stop grafana-server -f
  echo $PASS | sudo -S rm /etc/systemd/system/node_exporter.service
  echo $PASS | sudo -S rm /etc/systemd/system/prometheus.service
  echo $PASS | sudo -S dpkg -P grafana
  echo $PASS | sudo -S rm -rf /etc/grafana
  echo $PASS | sudo -S systemctl daemon-reload
  echo $PASS | sudo -S rm -rf /opt/central_monitor 
  echo $PASS | sudo -S crontab -l > tmp
  echo $PASS | sudo -S cat tmp | grep -v node_exp  > mycron
  echo $PASS | sudo -S cat mycron | grep -v gpu_scrap  > tmp
  echo $PASS | sudo -S crontab tmp
  echo $PASS | sudo -S rm mycron tmp
  echo "##################"
  echo "#     CHECK      #"
  echo "##################"
  echo $PASS | sudo -S systemctl status grafana-server
  echo $PASS | sudo -S systemctl status node_exporter
  echo $PASS | sudo -S systemctl status prometheus
  echo $PASS | sudo -S crontab -l

elif [ "$1" = "" ]; then
  echo "[INFO] ./setup.sh [ini|node|pro|gui|remove]"
  echo "[INFO] Option ini attempts to initialize the binary file. Please run it before installing!"
  echo "[INFO] Option node is for miner"
  echo "[INFO] Option pro & gui are both for central monitor"
  echo "[INFO] Option remove will remove all central monitor program"
fi
