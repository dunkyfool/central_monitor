###################################################
# Purpose: Create prometheus.yml Dynamic Config   #
# Date: 2018/03/15                                #
# Author: Jackie                                  #
###################################################
import os
import pprint as pp
import subprocess as sp

#######################################
# Load current node & bidagent status #
#######################################
pwd        = os.environ.get('PASSWORD') if('PASSWORD' in os.environ) else 'ryan'
configFile = os.environ.get('CONFIG_FILE') if('CONFIG_FILE' in os.environ) else '/opt/central_monitor/bin/prometheus.yml'
hostsFile  = os.environ.get('HOSTS_FILE') if('HOSTS_FILE' in os.environ) else '/etc/hosts'
print '[info] pwd set, prefix == ' + prefix + ' configFile == ' + configFile + ' hostsFile == ' + hostsFile
ctr = 0           # ctr is flag for checking whether process runs first time (0:Y)
oldDict = {}      # last time bidagent config
wrFlag = 0        # rewrite nginx config

def validateIP(s):
    splits = s.split('.')
    if splits[0] != '10':
        return False
    if not len(splits) == 4:
        return False
    for numStr in splits:
        num = int(numStr)
        if num > 255 or num < 0:
            return False
    return True

def takeLast(hostlist):
    ip2host = {}
    for hostIp in hostlist:
        if hostIp[0] != 'localhost':
            host = hostIp[0]
            ip = hostIp[1]
            ip2host[ip] = host

    tmpHostList = []
    for ip in ip2host:
        tmpHostList.append([ip2host[ip], ip])
    return tmpHostList
    

while True:
    ################
    # Get Nodelist #
    ################
    nodeDict = {}               # name of nodes w/ bidagent
    hostlist = []               # for mapping hostname to ip
    totalnodeAgentNum = 0       # Num of all agents
    nodeNum = 0                 # Num of all nodes  w/ bidagent

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


    print '[info] nodeDict ==', nodeDict
    nodeNum = len(nodeDict)

    ####################
    # Check Difference #
    ####################
    if ctr==0:  # At beginning
        oldDict = nodeDict
        wrFlag=1
    elif ctr==1:
        # seems like dictionary comparsison is guaranteed (recursively)
        # ref: http://stackoverflow.com/questions/1911273/is-there-a-better-way-to-compare-dictionary-values
        if oldDict == nodeDict:
            wrFlag=0
        else:
            wrFlag=1
            oldDict = nodeDict# change oldDict

    #################
    # Create config #
    #################
    if wrFlag==1:
        with open(configFile, 'w') as f:
            f.write('global:\n')
            f.write('  scrape_interval:     15s\n')
            f.write('  evaluation_interval: 15s\n')
            f.write('  external_labels:\n')
            f.write('      monitor: \'CENTRAL MONITOR\':\n\n')
            f.write('rule_files:\n')
            f.write('   - alert.rules\n\n')
            f.write('scrape_configs:\n')
            f.write('  - job_name: \'node-exporter\'\n')
            f.write('    static_configs:\n')
            f.write('            - targets: [\'localhost:9100\']\n\n')
            f.write('  - job_name: \'prometheus\'\n')
            f.write('    static_configs:\n')
            f.write('            - targets: [\'localhost:9090\']\n')

            for host in nodeDict:
                if len(nodeDict[host]['ports']) > 0:
                    ip = nodeDict[host]['Address']
                    f.write('  location /w/'+ip+'/ {\n')

        ################
        # Reload Nginx #
        ################
        if ctr==0:
            cmd = '/usr/sbin/nginx -t && sleep 1'
            os.system(cmd)
            cmd = 'systemctl reload nginx'
            os.system(cmd)
            ctr=1
        else:
            cmd = '/usr/sbin/nginx -t && sleep 1'
            os.system(cmd)
            #cmd = '/usr/sbin/nginx -s reload'
            cmd = 'systemctl reload nginx'
            os.system(cmd)

    cmd = 'sleep 10'
    print '[info]: ' + cmd + ' secs now'
    os.system(cmd)

