# ex:set ts=2:

from random import random, uniform, normalvariate

class TNode ():
  def __init__ (self, initial, nodelist, static = False):
    self.value = float(initial)
    self.nodelist = nodelist
    nodelist.append(self)
    self.static = static
  def get_value (self, key=None):
    return self.value
  def set_value (self, value):
    self.value = value
  def read (self):
    self.copy = self.get_value()
  def modify (self, value):
    if not self.static:
      self.copy += value
  def write (self):
    self.set_value(self.copy)
  

class TNodeExposed (TNode):
  def __init__ (self, initial, nodelist, control, static = False):
    self.control = control
    control.register(self)
    TNode.__init__(self, initial, nodelist, static)
  

class TNodeList ():
  def __init__ (self):
    self.l = []
  def append (self, node):
    self.l.append(node)
  def read (self):
    for node in self.l:
      node.read()
  def write (self):
    for node in self.l:
      node.write()
    
  

class TEdge ():
  def __init__ (self, nodeA, nodeB, translator, edgelist):
    self.nodeA = nodeA
    self.nodeB = nodeB
    self.translator = translator
    self.edgelist = edgelist
    edgelist.append(self)
  def relax (self, stepsize):
    a = self.nodeA.get_value()
    b = self.nodeB.get_value()
    value = (b-a)/2*self.translator*stepsize
    self.nodeA.modify(value)
    self.nodeB.modify(-1*value)
  

class TEdgeList ():
  def __init__ (self):
    self.l = []
  def append (self, edge):
    self.l.append(edge)
  def relax (self, stepsize):
    for edge in self.l:
      edge.relax(stepsize)
    
  

secsperday = 60*60*24

class TCloud ():
  def __init__ (self, days, count, daycount=secsperday, mu=4, sigma=3, sigmamod=12):
    self.map = [0]*days
    self.daycount = daycount
    self.mu = mu
    self.sigma = sigma
    self.sigmamod = sigmamod
    self.lastday = None
    self.daymap = [0]*secsperday
    
    for i in range(count):
      index = int(uniform(0,days))
      size = normalvariate(mu, sigma*uniform(0,sigmamod))
      
      for s in range(int(size)):
        self.map[(index+s) % len(self.map)] += 1
  def index (self, time):
    day    = int(time/(secsperday))
    subday = int(time%(secsperday))
    
    if day != self.lastday:
      lastvalue = self.daymap[-1]
      self.daymap = [0]*secsperday
      
      # attempt to make it line up with previous day. TODO: move it down and make it adaptive to what has been filled out
      for i in range(lastvalue):
        self.daymap[i] = lastvalue - i
      
      # fill out
      for i in range(self.daycount):
        index = int(uniform(0, secsperday))
        size = normalvariate(self.mu, self.sigma*uniform(0,self.sigmamod))
        
        for s in range(int(size)):
          if index+s < len(self.daymap):
            self.daymap[index+s] += 1
      
      self.lastday = day
    
    return self.map[day]*10+self.daymap[subday]+random()

class TWorld ():
  stepsize = 0.1
  def __init__ (self, nodelist, edgelist):
    self.nodelist = nodelist
    self.edgelist = edgelist
  def step (self, stepsize):
    while stepsize > 0.0:
      if stepsize > TWorld.stepsize:
        step = TWorld.stepsize
        stepsize -= TWorld.stepsize
      else:
        step = stepsize
        stepsize = 0.0
      self.nodelist.read()
      self.edgelist.relax(step)
      self.nodelist.write()
    
  

