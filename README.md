# Central Monitor

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

5. Install proemtheus

```
./setup.sh pro
```

6. Install grafana

```
./setup.sh gui
```

7. Update prometheus.yml (make sure /etc/hosts is correct)

```
python bin/fresher.py
```

8. Update & import dashboard (make sure /etc/hosts is correct)

```
python script/transform_panel.py && ./script/batch_impot.sh
```

## How to remove

1. Go to '/opt/central_monitor/' and copy setup.sh to parent folder 

```
cp setup.sh ../
```

2. Go to parent folder and run setup.sh remove

```
./setup.sh remove
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
10. [/etc/hosts] Define like this 10.0.0.1 miner1.
