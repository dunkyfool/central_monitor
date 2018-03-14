#!/bin/sh

# Logging wanted directory
if [ "$1" = "" ]; then
  echo "[Info] (opt|pro|ngx|docker)"

elif [ "$1" = "opt" ]; then
  echo 'mimimi123' | sudo -S mkdir -p data
  du -sb /data /var/log /opt/* | grep -v pem | \
  sed -ne 's/^\([0-9]\+\)\t\(.*\)$/node_directory_size_bytes{directory="\2"} \1/p' \
  > /opt/central_monitor/txt/directory_size_bytes.prom

elif [ "$1" = "pro" ]; then
  # Logging prometheus cpu, mem
  ps -p `pgrep prometheus` -o %cpu | grep '[0-9.]'| \
  sed -ne 's/^ /node_prometheus_usage{content="cpu"} /p' \
  > /opt/central_monitor//txt/prometheus_usage.prom && \
  ps -p `pgrep prometheus` -o %mem | grep '[0-9.]'| \
  sed -ne 's/^ /node_prometheus_usage{content="mem"} /p' \
  >> /opt/central_monitor/txt/prometheus_usage.prom

elif [ "$1" = "ngx" ]; then
  # Logging nginx cpu, mem
  ps -p `pgrep -a nginx|grep sbin|cut -d' ' -f1` -o %cpu | grep '[0-9.]'| \
  sed -ne 's/^ /node_nginx_usage{content="cpu"} /p' \
  > /opt/central_monitor//txt/nginx_usage.prom && \
  ps -p `pgrep -a nginx|grep sbin|cut -d' ' -f1` -o %mem | grep '[0-9.]'| \
  sed -ne 's/^ /node_nginx_usage{content="mem"} /p' \
  >> /opt/central_monitor/txt/nginx_usage.prom

elif [ "$1" = "docker" ]; then
  # Logging 
  docker info | grep -v 'WARN' | grep 'Data Space' | \
  sed -ne 's/ Data Space \([a-zA-Z]\+\): \([0-9.]\+\) GB/node_docker_disk_usage{content="\1"} \2/p' \
  > /opt/central_monitor/txt/docker_disk_usage.prom

fi
