# Central Monitor

## Set up /etc/hosts

Please make sure the /etc/hosts as below:

```
127.0.0.1 localhost
10.0.0.1  miner1
10.0.0.2  miner2
10.0.0.3  miner3
```

## How to install

This program is based on Ubuntu 16.04 and will install three items, including node_exporter, prometheus, and grafana.

1. Put central_monitor folder to directory: '/opt/'

```
sudo cp -r central_monitor /opt/
```

2. Go to '/opt/central_monitor/' and run setup.sh to check the information

```
cd /opt/central_monitor
./setup.sh
```

3. Make all binary executable 

```
./setup.sh ini
```

4. Install node_exporter

```
./setup.sh node
```

5. Install alertmanager and wrapper

```
./setup.sh alert
```

6. Install proemtheus

```
./setup.sh pro
```

7. Install grafana

```
./setup.sh gui
```

8. Update prometheus.yml (make sure /etc/hosts is correct)

```
python bin/fresher.py
```

9. Update & import dashboard (make sure /etc/hosts is correct)

```
python script/transform_panel.py && ./script/batch_impot.sh
```

10. Go to wrapper and follow readme to install

## How to remove

1. Go to '/opt/central_monitor/' and copy setup.sh to parent folder 

```
cp setup.sh ../
```

2. Go to parent folder and run setup.sh remove

```
./setup.sh remove
```

3. Clean up cronjob

```
crontab -e
```

## Configure

1. [Prometheus] It will keep the data one year by default
2. [Prometheus] The configure is at /opt/central_monitor/bin/prometheus.yml
3. [Prometheus] The alert rule is at /opt/central_monitor/bin/alert.rules
4. [Prometheus] It listens to the 9090 port
5. [Node\_exporter] To customize the required output, it has to modify the /opt/central_monitor/script/node_exp.sh
6. [Node\_exporter] It listens to the 9100 port
7. [Grafana] The default account and password is admin/admin
8. [Grafana] The data source is prometheus and access by proxy http://localhost:9090
9. [Grafana] It listens to 3000 port
