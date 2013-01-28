# ex:set ts=2:

import math
import sys
from sim.color import textred
from sim.debug import dumpstack

# Interfacing:
# ~~~~~~~~~~~~
#
# The "right way" to interface a CNode graph is through nodes of types CNodePush, CNodePull and CNodePullPush.
#

# Calculation node
class CNode:
  def __init__ (self, inputs, outputs, ifilter = None, ofilter = None):
    self.inputs = inputs
    self.outputs = outputs
    if ifilter == None:
      ifilter = {}
      for i in inputs:
        ifilter[i] = True
    if ofilter == None:
      ofilter = {}
      for o in outputs:
        ofilter[o] = True
    self.ifilter = ifilter
    self.ofilter = ofilter
  def add_output (self, host, port):
    self.outputs.append((host, port))
  def remove_output (self, host, port):
    new = []
    for thost, tport in self.outputs:
      if host != thost or port != tport:
        new.append((thost, tport))
    self.outputs = new
  def update (self, port, value):
    if not self.inputs.has_key(port):
      print textred("Err: Invalid port '"+str(port)+"' for node input.")
      print textred("     Affected node: "+str(self))
      print textred("     Valid ports:"+("".join(map(lambda e: " "+str(e), self.inputs))))
      dumpstack()
      sys.exit(5)
    if not self.ifilter.has_key(port):
      print textred("Err: Invalid port '"+str(port)+"' for node ifilter")
      print textred("     Affected node: "+str(self))
      dumpstack()
      sys.exit(6)
    if not self.ifilter[port]: return
    self.inputs[port] = value
    self.rerun()
  def rerun (self):
    self.recalculate()
    for output, port in self.outputs:
      if not self.ofilter.has_key((output,port)):
        print textred("Err: Invalid output, port '"+str(output)+","+str(port)+"' for node ofilter")
        print textred("     Affected node: "+str(self))
        dumpstack()
        sys.exit(7)
      if self.ofilter[(output, port)]:
        output.update(port, self.value)
  def recalculate(self): pass

class CNodeSource (CNode):
  def __init__ (self, outputs=[], value=None):
    CNode.__init__(self, {"a": value}, outputs)
  def recalculate (self):
    self.value = self.inputs["a"]
  def update (self):
    CNode.update(self, "a", 42)

class CNodeDrain (CNode):
  def __init__ (self, outputs=[], value=None):
    CNode.__init__(self, {"a": value}, outputs)
  def recalculate (self):
    pass
  def value (self):
    return self.inputs["a"]

class CNodeConst (CNode):
  def __init__ (self, outputs=[], value=None, updatelist=None):
    if updatelist != None: updatelist.append(self)
    CNode.__init__(self, {"a": value}, outputs)
    self.recalculate()
  def recalculate (self):
    self.value = self.inputs["a"]

class CNodeAdd (CNode):
  def __init__ (self, outputs=[]):
    CNode.__init__(self, {"a": -1, "b": -1}, outputs)
  def recalculate (self):
    self.value = self.inputs["a"] + self.inputs["b"]

class CNodeSub (CNode):
  def __init__ (self, outputs=[]):
    CNode.__init__(self, {"a": -1, "b": -1}, outputs)
  def recalculate (self):
    self.value = self.inputs["a"] - self.inputs["b"]

class CNodeMul (CNode):
  def __init__ (self, outputs=[]):
    CNode.__init__(self, {"a": -1, "b": -1}, outputs)
  def recalculate (self):
    self.value = self.inputs["a"] * self.inputs["b"]

class CNodeDiv (CNode):
  def __init__ (self, outputs=[]):
    CNode.__init__(self, {"a": -1, "b": -1}, outputs)
  def recalculate (self):
    self.value = self.inputs["a"] / self.inputs["b"]

class CNodeMod (CNode):
  def __init__ (self, outputs=[]):
    CNode.__init__(self, {"a": -1, "b": -1}, outputs)
  def recalculate (self):
    self.value = self.inputs["a"] % self.inputs["b"]

class CNodeSqrt (CNode):
  def __init__ (self, outputs=[]):
    CNode.__init__(self, {"a": -1}, outputs)
  def recalculate (self):
    self.value = math.sqrt(self.inputs["a"])

class CNodeSum (CNode):
  def __init__ (self, outputs=[], count=1):
    inputs = {}
    for i in range(1,count+1):
      inputs[str(i)] = -1
    CNode.__init__(self, inputs, outputs)
  def recalculate (self):
    self.value = 0
    for key in self.inputs.keys():
      self.value += self.inputs[key]

class CNodeCutoff (CNode):
  def __init__ (self, outputs=[]):
    CNode.__init__(self, {"a": -1, "b": -1}, outputs)
  def recalculate (self):
    value = self.inputs["a"] - self.inputs["b"]
    self.value = 0 if value < 0.0 else value

class CNodePull (CNode):
  def __init__ (self, func, outputs=[], updatelist=None):
    self.func = func
    if updatelist != None: updatelist.append(self)
    CNode.__init__(self, {"a": -1}, outputs)
  def recalculate (self):
    self.value = self.func()

class CNodePush (CNode):
  def __init__ (self, func, value=0, outputs=[], updatelist=None):
    self.func = func
    self.value = value
    if updatelist != None: updatelist.append(self)
    CNode.__init__(self, {"a": value}, outputs)
  def recalculate (self):
    self.func(self.inputs["a"])

class CNodePullPush (CNode):
  def __init__ (self, funcPull, funcPush, outputs=[], updatelist=None):
    self.funcPull = funcPull
    self.funcPush = funcPush
    if updatelist != None: updatelist.append(self)
    CNode.__init__(self, {"a": -1}, outputs)
  def recalculate (self):
    self.value = self.funcPull()
#    print "pull-push-ing "+str(self.value)
    self.funcPush(self.value)

class CNodeFunc (CNodePull):
  pass

class CNodeList ():
  def __init__ (self):
    self.l = []
  def append (self, node):
    self.l.append(node)
  def rerun (self):
    for node in self.l:
      node.rerun()
  def map (self, fun):
    map(fun, self.l)
  

