import sys, os
import redis
import uuid

def main():
#  try:
      miner, opt = sys.argv[1], sys.argv[2]
      r = redis.StrictRedis()
      outcome = r.hgetall(miner)

      if outcome:
          if opt == "reboot":
              re_cnt = outcome['reboot_count']
              PLC_NO = int(outcome['PLC_NO'])
              REG_ADDR = int(outcome['REG_ADDR'])
              r.hmset(miner, {"reboot_count": int(re_cnt)+1})
              # reboot command
              reboot(PLC_NO, REG_ADDR)

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
              cmd = 'scp /tmp/'+random_name+' ethos@'+miner+':/home/ethos/freq.csv && rm /tmp/'+random_name
              #cmd = "ssh "+miner+" sh /opt/central_monitor/script/setFreq.sh "+devid+" "+str(dev_freq)
              os.system(cmd)

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
              cmd = 'scp /tmp/'+random_name+' ethos@'+miner+':/home/ethos/freq.csv && rm /tmp/'+random_name
              #cmd = "ssh "+miner+" sh /opt/central_monitor/script/setFreq.sh "+devid+" "+str(dev_freq)
              os.system(cmd)
      else:
        print "[WARN] " + miner + " not found!"
#  except:
#      print "[WARN] Wrong Commands"


def reboot(PLC_NO, REG_ADDR):
	import serial
	import pymodbus
	from pymodbus.client.sync import ModbusSerialClient as ModbusClient
        import time

        #PLC_NO=10
        #REG_ADDR=2048

	client = ModbusClient(method="ascii", port="/dev/ttyUSB0", stopbits=1, bytesize=8, parity="N", baudrate=9600, timeout=20)
	client.write_register(0x1000, 600, unit=PLC_NO)
        status = client.read_coils(2048, 1, unit=PLC_NO)
        if status.bits[0]:
            client.write_coil(REG_ADDR, False, unit=PLC_NO)
        else:
          client.write_coil(REG_ADDR, True, unit=PLC_NO)
	client.close()



if __name__=="__main__":
    main()
