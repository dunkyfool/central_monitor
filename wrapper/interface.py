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
              r.hmset(miner, {"reboot_count": int(re_cnt)+1})
              # reboot command

          elif opt == "decreaseFreq":
              freq_cnt, freq = outcome['freq_count'], outcome['freq']
              r.hmset(miner, {"freq_count": int(freq_cnt)+1, "freq": int(freq)-1})
              # decreaseFreq command

          elif opt == "increaseFreq":
              freq_cnt, freq = outcome['freq_count'], outcome['freq']
              r.hmset(miner, {"freq_count": int(freq_cnt)+1, "freq": int(freq)+1})
              # increaseFreq command
      else:
          default = {
              "reboot_count": 0,
              "freq_count": 0,
              "ip": "localhost",
              "freq": 0,
              "plc": 0
          }
          r.hmset(miner, default)
  except:
      print "[WARN] Wrong Commands"


if __name__=="__main__":
    main()
