# ex:set ts=2:

from color import *
from debug import *
import sys
import traceback

class SimLog:
  def __init__ (self, filename, flags="w", sep=","):
    self.filename = filename
    self.fo = open(filename, flags)
    self.sep = sep
    self.key = []
  def legend (self, legend):
    self.key = legend
    self.fo.writelines("#"+self.sep+(self.sep.join(legend))+"\n")
  def append (self, data):
    if len(self.key) == 0:
      print textred("Err: Append called before legend on "+self.filename)
      dumpstack()
      sys.exit(1)
    if len(data) != len(self.key):
      print textred("Err: Trying to append dataset of wrong dimention to "+self.filename)
      dumpstack()
      sys.exit(2)
    self.fo.writelines(self.sep+(self.sep.join(map(lambda e: str(e), data)))+"\n")
  def comment (self, comment):
    self.fo.writelines("#"+comment+"\n")
  def index (self, name):
    for i in range(len(self.key)):
      if name == self.key[i]: return i
    print textred("Err: Name '"+name+"' not found in legend '"+str(self.key)+"'")
    dumpstack()
    sys.exit(4)
  

