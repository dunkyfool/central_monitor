# Requirement

1. Install docker, docker-compose, python, pypi, nodejs 4.2.6, npm 3.5.2 
2. pip install -r requrement.txt
3. npm install express body-parser
4. cd docker && docker build -t redis:backup .

# RUN

1. ./cmd.sh up
2. node index.js

# Note

Grafana has to set notification channel as webhook
REBOOT\_URL: localhost:8080/reboot
DECREASEFREQ\_URL: localhost:8080/decreaseFreq
INCREASEFREQ\_URL: localhost:8080/increaseFreq
