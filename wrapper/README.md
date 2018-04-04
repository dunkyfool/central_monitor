# Requirement

1. Install docker, docker-compose, python, pypi, nodejs 4.2.6, npm 3.5.2 
2. pip install -r requrement.txt
3. npm install -g express body-parser
4. cd docker && docker build -t redis:backup .

# RUN

1. Set up Redis

```
./cmd.sh up
```
2. Create Config & initialize redis

```
python create\_config.py && python ini\_redis.py
```

3. Start Wrapper

```
systemctl start wrapper.service
#node index.js
```

# Note

Grafana has to set notification channel as webhook

REBOOT\_URL: localhost:8080/reboot

DECREASEFREQ\_URL: localhost:8080/decreaseFreq

INCREASEFREQ\_URL: localhost:8080/increaseFreq
