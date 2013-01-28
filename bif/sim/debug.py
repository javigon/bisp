# ex:set ts=2:

import traceback

def dumpstack():
  stack = traceback.extract_stack()
  for line in stack[:len(stack)-1]:
    print line[0]+":"+str(line[1])+" "+line[2]
    print "  "+line[3]
