###################################################
# Purpose: Create prometheus.yml Dynamic Config   #
# Date: 2018/03/15                                #
# Author: Jackie                                  #
###################################################
import os
from pprint import pprint
import subprocess as sp

#######################################
# Load current node & bidagent status #
#######################################
configFile = os.environ.get('CONFIG_FILE') if('CONFIG_FILE' in os.environ) else '/opt/central_monitor/bin/prometheus.yml'
hostsFile  = os.environ.get('HOSTS_FILE') if('HOSTS_FILE' in os.environ) else '/etc/hosts'
ctr = 0           # ctr is flag for checking whether process runs first time (0:Y)
oldlist = []      # last time host in /etc/hosts
wrFlag = 0        # rewrite nginx config

def validateIP(s):
    splits = s.split('.')
    try:
        if not len(splits) == 4:
            return False
        for numStr in splits:
            num = int(numStr)
            if num > 255 or num < 0:
                return False
    except:
        print("Error! Due to "+s)
        return False
    return True

def takeLast(hostlist):
    ip2host = {}
    for hostIp in hostlist:
            host = hostIp[0]
            ip = hostIp[1]
            ip2host[ip] = host

    tmpHostList = []
    for ip in ip2host:
        tmpHostList.append([ip2host[ip], ip])
    return tmpHostList


################
# Get hostlist #
################
hostlist = []               # for mapping hostname to ip
nodeNum = 0                 # Num of all nodes

with open(hostsFile, 'r') as f:
    # hostlist = [
    #   (hostname, ip), 
    #   ...
    # ]
    hostlist = [(line.split()[1],line.split()[0]) for line in f if line.strip()]

    # filter those dont have valid ip
    hostlist = filter(lambda hostIp: validateIP(hostIp[1]), hostlist)

    # take last pair of the same ip (to avoid some ill-defined /etc/hosts)
    hostlist = takeLast(hostlist)
    print '[info] hostlist ==', hostlist

    nodeNum = len(hostlist)


####################
# Check Difference #
####################
if ctr == 0:  # At beginning
    oldlist = hostlist
    wrFlag=1
elif ctr == 1:
    # seems like dictionary comparsison is guaranteed (recursively)
    # ref: http://stackoverflow.com/questions/1911273/is-there-a-better-way-to-compare-dictionary-values
    if oldlist == hostlist:
        print '[info] /etc/hosts is the same'
        wrFlag=0
    else:
        print '[info] /etc/hosts is different from last time'
        wrFlag=1
        oldlist = hostlist# change oldlist

##################################
# Create string of listened host #
##################################
str_hostlist = ''
if nodeNum > 0:
    for pair in hostlist:
        str_hostlist += '\''+pair[0]+':9100\','
    str_hostlist = str_hostlist[:-1]
else:
    str_hostlist = '\'localhost:9100\''

#################
# Create config #
#################
if wrFlag==1:
    with open(configFile, 'w') as f:
    #with open('tmpCFG', 'w') as f:
        f.write('global:\n')
        f.write('  scrape_interval:     15s\n')
        f.write('  evaluation_interval: 15s\n')
        f.write('  external_labels:\n')
        f.write('      monitor: \'CENTRAL MONITOR\'\n\n')
        f.write('rule_files:\n')
        f.write('   - alert.rules\n\n')
        f.write('scrape_configs:\n')
        f.write('  - job_name: \'node-exporter\'\n')
        f.write('    static_configs:\n')
        f.write('            - targets: ['+str_hostlist+']\n\n')
        f.write('  - job_name: \'prometheus\'\n')
        f.write('    static_configs:\n')
        f.write('            - targets: [\'localhost:9090\']\n')

cmd = 'systemctl restart prometheus'
os.system(cmd)

