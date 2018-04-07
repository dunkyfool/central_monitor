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
              chasis_no = int(outcome['chasis_no'])
              server_no = int(outcome['server_no'])
              r.hmset(miner, {"reboot_count": int(re_cnt)+1})
              # reboot command
              reboot(chasis_no, server_no)

          elif opt == "decreaseFreq":
              devid = sys.argv[3]
              dev_freq = int(outcome["dev_"+devid+"_freq"]) - 50
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
              cmd = 'scp /tmp/'+random_name+' ryan@'+miner+':/home/ryan/freq.csv && rm /tmp/'+random_name
              #cmd = "ssh "+miner+" sh /opt/central_monitor/script/setFreq.sh "+devid+" "+str(dev_freq)
              os.system(cmd)

          elif opt == "increaseFreq":
              devid = sys.argv[3]
              dev_freq = int(outcome["dev_"+devid+"_freq"]) + 50
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
              cmd = 'scp /tmp/'+random_name+' ryan@'+miner+':/home/ryan/freq.csv && rm /tmp/'+random_name
              #cmd = "ssh "+miner+" sh /opt/central_monitor/script/setFreq.sh "+devid+" "+str(dev_freq)
              os.system(cmd)
      else:
        print "[WARN] " + miner + " not found!"
#  except:
#      print "[WARN] Wrong Commands"


def reboot(chasis_no, server_no):
	import serial
	import pymodbus
	from pymodbus.client.sync import ModbusSerialClient as ModbusClient
        import time

        #chasis_no=10
        #server_no=2048

	client = ModbusClient(method="ascii", port="/dev/ttyUSB0", stopbits=1, bytesize=8, parity="N", baudrate=9600, timeout=20)
	client.write_register(0x1000, 600, unit=chasis_no)
        status = client.read_coils(2048, 1, unit=chasis_no)
        if status.bits[0]:
            client.write_coil(server_no, False, unit=chasis_no)
        else:
          client.write_coil(server_no, True, unit=chasis_no)
	client.close()



if __name__=="__main__":
    main()
