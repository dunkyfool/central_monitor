import os, subprocess, redis
from pprint import pprint


def getRemoteMAC(ip):
  try:
    cmd="/bin/sh getIP.sh "+str(ip)
    MAC = subprocess.check_output(cmd,shell=True)
  except:
    MAC = None
  return MAC


def readConfig():
  miner_dict, mac_list, mac2miner = {}, [], {}
  idx = 1
  with open('mac_list.csv') as f:
    for line in f.readlines():
      NO, _, _, MAC, TEAMVIEWERID, PLC_NO, REG_ADDR, CHASIS_NO = line.split(',')
      MAC = MAC.lower().replace('-',':')
      mac_list += [MAC]
      miner_dict['miner'+str(idx)] = {\
                                   "NO": NO,
                                   "MAC": MAC,
                                   "TEAMVIEWERID": TEAMVIEWERID,
                                   "PLC_NO": PLC_NO[1:],
                                   "REG_ADDR": REG_ADDR.rstrip(),
                                   "CHASIS_NO": CHASIS_NO,
				   "reboot_count": 0,
				   "dev_0_freq": 1900,
				   "dev_1_freq": 1900,
				   "dev_2_freq": 1900,
				   "dev_3_freq": 1900,
				   "dev_4_freq": 1900,
				   "dev_5_freq": 1900,
				   "dev_6_freq": 1900,
				   "dev_7_freq": 1900,
      }
      mac2miner[MAC] = 'miner'+str(idx) 
      idx += 1
      
  return miner_dict, mac_list, mac2miner


def push2Redis(miner,miner_dict):
  r = redis.StrictRedis()
  r.hmset(miner,miner_dict)
  r.set(miner_dict["MAC"], miner)
  r.set(miner_dict["IP"], miner)


def write2Hosts(ip, miner):
  with open('hosts','a') as f:
    f.write(str(ip)+'\t'+miner+'\n')


if __name__=="__main__":
  miner_dict, mac_list, mac2miner = readConfig()
  for ip in range(2,255):
    _MAC = getRemoteMAC(ip)
    try: 
      _MAC = [ x.rstrip() for x in _MAC.split('\n') if x != '']
      pprint(_MAC)
    except:
      continue

    match = list(set(mac_list) & set(_MAC))
    pprint(match)
    if match:
      origin_dict = miner_dict[mac2miner[match[0]]]
      origin_dict["IP"] = '192.168.88.'+str(ip)
      miner_dict[mac2miner[match[0]]] = origin_dict

      push2Redis(mac2miner[match[0]], origin_dict)
      write2Hosts('192.168.88.'+str(ip),mac2miner[match[0]])      

      for _mac in _MAC:
        try:
          mac_list.remove(_mac)
        except:
          continue
