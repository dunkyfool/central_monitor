import redis
from config import CHASIS_NO


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
        if hostIp[0] != 'localhost':
            host = hostIp[0]
            ip = hostIp[1]
            ip2host[ip] = host

    tmpHostList = []
    for ip in ip2host:
        tmpHostList.append([ip2host[ip], ip])
    return tmpHostList

def main():
  r = redis.StrictRedis()
  hostlist = []

  with open('/etc/hosts', 'r') as f:
        hostlist = [(line.split()[1],line.split()[0]) for line in f if line.strip()]
        hostlist = filter(lambda hostIp: validateIP(hostIp[1]), hostlist)
        hostlist = takeLast(hostlist)
        print '[info] hostlist ==', hostlist
    
  for pair in hostlist:
    default = {
      "reboot_count": 0,
      "dev_0_freq": 650,
      "dev_1_freq": 650,
      "dev_2_freq": 650,
      "dev_3_freq": 650,
      "dev_4_freq": 650,
      "dev_5_freq": 650,
      "dev_6_freq": 650,
      "dev_7_freq": 650,
      "ip": pair[1],
      "chasis_no": CHASIS_NO[pair[0]][0],
      "server_no": CHASIS_NO[pair[0]][1],
    }
    r.hmset(pair[0], default)

if __name__=="__main__":
  main()
