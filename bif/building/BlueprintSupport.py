# ex:set ts=4:
from math import sin, pi
#from sim.cnode import CNode
#from sim.color import textred
#from sim.debug import dumpstack
from sim.cnode import CNode
from sim.color import textred
from sim.debug import dumpstack
import sys

TIME_PER_DAY = 3600*24
TIME_PER_YEAR = TIME_PER_DAY*365

class CNodeSun (CNode):
    def __init__ (self, outputs=[], cloud=None, somelist=None):
        self.cloud = cloud
        if somelist != None: somelist.append(self)
        CNode.__init__(self, {"time": -1}, outputs)
    def register (self, tnode):
        self.tnode = tnode
    def recalculate (self):
        cloudiness = 0
        if self.cloud != None: cloudiness = self.cloud.index(self.inputs["time"])
        self.value = 0
        self.value += 31.0
        self.value += 5.3*sin(self.inputs["time"]/TIME_PER_YEAR*(2*pi)-.5*pi)
        self.value += 3.2*sin(self.inputs["time"]/TIME_PER_DAY*(2*pi)-.5*pi)
        self.value -= cloudiness/4
        self.tnode.set_value(self.value)
#        print self.value
    def set_time (self, time):
        self.inputs["time"] = time
        self.rerun()
    def get_value (self, key=None):
        if key==None or key=="time":
            return self.inputs["time"]
        if key=="cloudiness":
            cloudiness = 0
            if self.cloud != None: cloudiness = self.cloud.index(self.inputs["time"])
            return cloudiness
        else:
            print textred("Err: Unknown key '"+key+"' for FNodeGenerator")
            dumpstack()
            sys.exit(10)
        
    

class CNodeRain (CNode):
    def __init__ (self, outputs=[], cloud=None, somelist=None, cutoff=50.1, scale=0.003):
        self.cloud = cloud
        self.cutoff = cutoff
        self.scale = scale
        if somelist != None: somelist.append(self)
        CNode.__init__(self, {"time": -1}, outputs)
    def register (self, tnode):
        self.tnode = tnode
    def recalculate (self):
        cloudiness = self.cloud.index(self.inputs["time"])
        self.value = cloudiness - self.cutoff
        self.value *= self.scale
        if self.value < 0: self.value = 0
        self.tnode.set_value(self.value)
#        print self.value
    def set_time (self, time):
        self.inputs["time"] = time
        self.rerun()
    def get_value (self, key=None):
        if key==None or key=="time":
            return self.inputs["time"]
        if key=="rain":
            return self.value
        if key=="cloudiness":
            cloudiness = 0
            if self.cloud != None: cloudiness = self.cloud.index(self.inputs["time"])
            return cloudiness
        else:
            print textred("Err: Unknown key '"+key+"' for FNodeGenerator")
            dumpstack()
            sys.exit(10)
        
    

class CNodeCloud (CNode):
    def __init__ (self, outputs=[]):
        CNode.__init__(self, {"a": -1}, outputs)
    def recalculate (self):
        self.value = sin(self.inputs["a"])
    

