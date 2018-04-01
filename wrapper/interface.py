import sys
import redis

def main():
  try:
      miner, opt = sys.argv[1:]
      r = redis.StrictRedis()
      outcome = r.hgetall(miner)

      if outcome:
          if opt == "reboot":
              re_cnt = outcome['reboot_count']
              chasis_no = hex(int(outcome['chasis_no']))
              server_no = int(outcome['server_no'])
              r.hmset(miner, {"reboot_count": int(re_cnt)+1})
              # reboot command
              reboot(chasis_no, server_no)

          elif opt == "decreaseFreq":
              devid = sys.argv[3]
              dev_freq = int(outcome["dev_"+devid+"freq"]) - 50
              r.hmset(miner, {"dev_"+devid+"freq": dev_freq})
              # decreaseFreq command
              cmd = "ssh "+miner+"/opt/central_monitor/script/setFreq.sh "+devid+" "+str(dev_freq)
              os.system(cmd)

          elif opt == "increaseFreq":
              devid = sys.argv[3]
              dev_freq = int(outcome["dev_"+devid+"freq"]) + 50
              r.hmset(miner, {"dev_"+devid+"freq": dev_freq})
              # increaseFreq command
              cmd = "ssh "+miner+"/opt/central_monitor/script/setFreq.sh "+devid+" "+str(dev_freq)
              os.system(cmd)
      else:
      print "[WARN] " + miner + " not found!"
  except:
      print "[WARN] Wrong Commands"


def reboot(chasis_no, server_no):
	import serial
	import pymodbus
	from pymodbus.client.sync import ModbusSerialClient as ModbusClient
        import time

	client = ModbusClient(method="ascii", port="/dev/ttyUSB0", stopbits=1, bytesize=8, parity="N", baudrate=9600, timeout=20)
	client.write_coil(server_no, True, unit=chasis_no)
        time.sleep(60)
	client.write_coil(server_no, False, unit=chasis_no)
	client.close()



if __name__=="__main__":
    main()
