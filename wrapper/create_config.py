import sys, subprocess
from pprint import pprint

def main():
#  try:
    #num_node = int(sys.argv[1])
    num_node = int(subprocess.check_output(['grep','-c','miner','/etc/hosts']))
    num_chasis = num_node / 36 + 1
    num_reg = num_node / 6 + 1
    ctr, curr_chasis, curr_reg = 1, 1, 11

    with open('config.py', 'w') as f:
      f.write("CHASIS_NO = {\n")
      for i in range(1,num_node+1):

        f.write("    \"miner"+str(i)+"\": ["+str(curr_chasis)+", "+str(curr_reg)+"],\n")

        # chasis
        #print "miner" + str(i) + ": "+ str(curr_chasis)

        # reg
        #print "miner" + str(i) + ": "+ str(curr_reg)

        if ctr % 6 == 0:
          curr_reg += 5
        else:
          curr_reg += 1

        if ctr % 36 == 0:
          curr_chasis += 1
          curr_reg = 11

        ctr += 1
      f.write("}\n")

#  except:
#    print "No argument! python create_config.py 200 >\"<"
#    sys.exit(0)

if __name__=="__main__":
  main()
