import sys, os
import redis
import uuid
import time
from datetime import datetime

MAX_REBOOT_NUM = 10

def main():
#  try:
      miner, opt = sys.argv[1], sys.argv[2]
      r = redis.StrictRedis()
      outcome = r.hgetall(miner)

      if outcome:
          if opt == "reboot":
              CHASIS_NO = int(outcome['CHASIS_NO'])
              REG_ADDR = int(outcome['REG_ADDR'])
              flag, outcome = rebootCheck(outcome)
              r.hmset(miner, outcome)
              # reboot command
              if flag:
                  reboot(CHASIS_NO, REG_ADDR)

          elif opt == "decreaseFreq":
              devid = sys.argv[3]
              dev_freq = int(outcome["dev_"+devid+"_freq"]) - 50
              if dev_freq < 1700:
                dev_freq = 1700
              r.hmset(miner, {"dev_"+devid+"_freq": dev_freq})
              # decreaseFreq command
              random_name = uuid.uuid4().hex
              freq = r.hgetall(miner)
              with open('/tmp/'+random_name, 'w') as f:
                  f.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" %  (0, freq['dev_0_freq'],
                                                                                1, freq['dev_1_freq'],
                                                                                2, freq['dev_2_freq'],
                                                                                3, freq['dev_3_freq'],
                                                                                4, freq['dev_4_freq'],
                                                                                5, freq['dev_5_freq'],
                                                                                6, freq['dev_6_freq'],
                                                                                7, freq['dev_7_freq']))
              cmd = 'sshpass -p digitalespacio scp -o StrictHostKeyChecking=no /tmp/'+random_name+' ethos@'+miner+':/home/ethos/freq.csv && rm /tmp/'+random_name
              #cmd = "ssh "+miner+" sh /opt/central_monitor/script/setFreq.sh "+devid+" "+str(dev_freq)
              os.system(cmd)
              time.sleep(10)
              CHASIS_NO = int(outcome['CHASIS_NO'])
              REG_ADDR = int(outcome['REG_ADDR'])
              flag, outcome = rebootCheck(outcome)
              if flag:
                  reboot(CHASIS_NO, REG_ADDR)

          elif opt == "increaseFreq":
              devid = sys.argv[3]
              dev_freq = int(outcome["dev_"+devid+"_freq"]) + 50
              if dev_freq > 2000:
                dev_freq = 2000
              r.hmset(miner, {"dev_"+devid+"_freq": dev_freq})
              # increaseFreq command
              random_name = uuid.uuid4().hex
              freq = r.hgetall(miner)
              with open('/tmp/'+random_name, 'w') as f:
                  f.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" %  (0, freq['dev_0_freq'],
                                                                                1, freq['dev_1_freq'],
                                                                                2, freq['dev_2_freq'],
                                                                                3, freq['dev_3_freq'],
                                                                                4, freq['dev_4_freq'],
                                                                                5, freq['dev_5_freq'],
                                                                                6, freq['dev_6_freq'],
                                                                                7, freq['dev_7_freq']))
              cmd = 'sshpass -p digitalespacio scp -o StrictHostKeyChecking=no /tmp/'+random_name+' ethos@'+miner+':/home/ethos/freq.csv && rm /tmp/'+random_name
              #cmd = "ssh "+miner+" sh /opt/central_monitor/script/setFreq.sh "+devid+" "+str(dev_freq)
              os.system(cmd)
              time.sleep(10)
              CHASIS_NO = int(outcome['CHASIS_NO'])
              REG_ADDR = int(outcome['REG_ADDR'])
              flag, outcome = rebootCheck(outcome)
              if flag:
                  reboot(CHASIS_NO, REG_ADDR)
      else:
        print "[WARN] " + miner + " not found!"
#  except:
#      print "[WARN] Wrong Commands"


def get_current_date():
    return str(datetime.now()).split(' ')[0]


def rebootCheck(outcome):
    current_date = get_current_date()
    if "current_date" not in outcome:
        outcome['current_date'] = current_date
        if 'daily_reboot_count' not in outcome:
            outcome['daily_reboot_count'] = 0
        if int(outcome['daily_reboot_count']) < MAX_REBOOT_NUM:
            outcome['daily_reboot_count'] = int(outcome['daily_reboot_count']) + 1
            outcome['reboot_count'] = int(outcome['reboot_count']) + 1
            return True, outcome
        else:
            outcome['reboot_count'] = int(outcome['reboot_count']) + 1
            return False, outcome
    else:
        if current_date == outcome['current_date']:
            if 'daily_reboot_count' not in outcome:
                outcome['daily_reboot_count'] = 0
            if int(outcome['daily_reboot_count']) < MAX_REBOOT_NUM:
                outcome['daily_reboot_count'] = int(outcome['daily_reboot_count']) + 1
                outcome['reboot_count'] = int(outcome['reboot_count']) + 1
                return True, outcome
            else:
                outcome['reboot_count'] = int(outcome['reboot_count']) + 1
                return False, outcome
        else:
            outcome['current_date'] = current_date
            outcome['daily_reboot_count'] = 0
            outcome['reboot_count'] = int(outcome['reboot_count']) + 1
            return True, outcome



def reboot(CHASIS_NO, REG_ADDR):
	import serial
	import pymodbus
	from pymodbus.client.sync import ModbusSerialClient as ModbusClient
        import time

        #CHASIS_NO=10
        #REG_ADDR=2048

	client = ModbusClient(method="ascii", port="/dev/ttyUSB0", stopbits=1, bytesize=8, parity="N", baudrate=9600, timeout=20)
	#client.write_register(0x1000, 600, unit=CHASIS_NO)
        status = client.read_coils(REG_ADDR, 1, unit=CHASIS_NO)
        if status.bits[0]:
            client.write_coil(REG_ADDR, False, unit=CHASIS_NO)
        else:
          client.write_coil(REG_ADDR, True, unit=CHASIS_NO)
	client.close()



if __name__=="__main__":
    main()
