# ex:set ts=2:

from random import uniform
import sys
from color import *
from debug import *

fnode_debug = False
#fnode_debug = True

# Introduction:
# ~~~~~~~~~~~~~
#
# For each step, first iterate through producers, then iterate through buffers and finally iterate through consumers.
#
# A node can no more than a single upstream. The only exception is the multiplexer which has a single active upstream.
#
# Restrictions related to buffer style nodes (battery, bassin ...):
# - They cannot share upstream with any node.
# - There cannot be two buffers on any line (e.g. lamp->battery->mux->battery->panel is not allowed).
#
#
# Production Case
# ~~~~~~~~~~~~~~~
#
# Consumer       Producer       Upstream
#                   |
#                   | step
#                   |
#
#
# Buffer Cases
# ~~~~~~~~~~~~
#
# Buffers act as consumers. The difference lies in the need for buffers to be iterated before the consumers.
#
#
# Consumption Case 1: Base Case
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Consumer       Producer       Upstream
#          \
#           \
#            \ register
#             \
#              \
#          \
#           \
#            \ request
#             \
#              \
#                   |
#                   | attempt
#                   |
#                   | accept
#                   |
#              /
#             /
#            / accept (one call per consumer)
#           /
#          /
#
#
# Consumption Case 2: Induction Step
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Consumer       Producer       Upstream
#          \
#           \
#            \ register
#             \
#              \
#          \
#           \
#            \ request
#             \
#              \
#                         \
#                          \
#                           \ request
#                            \
#                             \
#                  ...
#                             /
#                            /
#                           / accept (one call per consumer)
#                          /
#                         /
#              /
#             /
#            / accept (one call per consumer)
#           /
#          /
#


class FNode ():
  def __init__ (self, upstream):
    self.upstream = upstream
    if upstream != None: upstream.register(self)
    self.consumers = {}
    self.requests = {}
    self.accepted = 0.0
  def register (self, consumer):
    if fnode_debug: print "fnode.register("+str(consumer)+")"
    self.consumers[consumer] = False
    self.requests[consumer] = 0
  def request (self, consumer, amount):
    if fnode_debug: print "fnode.request("+str(consumer)+","+str(amount)+")"
    self.requests[consumer] = amount
    self.consumers[consumer] = True
    
    # check wether we are the last consumer
    ready = True
    for key in self.consumers.keys():
      if self.consumers[key] == False:
        ready = False
    
    # process requested amounts
    if ready:
      total = sum(map(lambda key: self.requests[key], self.requests.keys()))
      self.lasttotal = total # TODO: should be parsed through
      if self.upstream == None:
        if self.attempt(total):
          FNode.accept(self, total)
        else:
          FNode.accept(self, 0)
      else:
        self.upstream.request(self, total)
  def accept (self, amount):
    if fnode_debug: print "fnode.accept("+str(amount)+")"
    self.accepted = amount
    amounts = self.requests
    for consumer in self.consumers:
      self.consumers[consumer] = False
    for consumer in self.consumers:
      value = 0.0
      if amount > 0:
        value = amounts[consumer]
        self.requests[consumer] = 0
      consumer.accept(value)
  def get_value (self, key):
    return self.accepted
  

class FNodePanel (FNode):
  def __init__ (self, cnode, generaters=None, efficiency=0.001):
    upstream = None
    self.cnode = cnode
#    self.outflux = float(outflux)
    self.charge = float(0)
    self.generaters = generaters
    if generaters != None:
      generaters.append(self)
    self.efficiency = efficiency
    FNode.__init__(self, upstream)
  def attempt (self, total):
    if fnode_debug: print "panel.attempt("+str(total)+")"
    if total <= self.charge:
      self.charge -= total
      return True
    else:
      return False
  def request (self, consumer, amount):
    if fnode_debug: print "panel.request("+str(consumer)+","+str(amount)+")"
    if len(self.consumers) != 1:
      print textred("Err: A FNodePanel must have one consumer, and only one!")
      print textred("     Has the following consumers: "+str(self.consumers))
      dumpstack()
      sys.exit(10)
    consumer.accept(self.charge)
  def step (self, stepsize):
    if fnode_debug: print "panel.step("+str(stepsize)+")"
    self.charge = self.efficiency * self.cnode.get_value("output") * stepsize
  def get_value (self, key=None):
    if key==None or key=="output":
      return self.charge
    else:
      print textred("Err: Unknown key '"+key+"' for FNodePanel")
      dumpstack()
      sys.exit(10)

class FNodeBattery (FNode):
  def __init__ (self, capacity, charge, upstream = None, consumers=None):
    self.capacity = float(capacity)
    self.charge = float(charge)
    self.hiddenupstream = upstream
    if self.hiddenupstream != None: self.hiddenupstream.register(self)
    if consumers != None:
      consumers.append(self)
    FNode.__init__(self, None)
  def attempt (self, total):
    if fnode_debug: print "battery.attempt("+str(total)+") charge="+str(self.charge)
    # request!
    
    if total <= self.charge:
      self.charge -= total
      return True
    else:
      return False
  def step (self, stepsize):
    if fnode_debug: print "battery.step("+str(stepsize)+")"
    if self.hiddenupstream != None: self.hiddenupstream.request(self, self.capacity-self.charge)
  def accept (self, amount):
    if fnode_debug: print "battery.accept("+str(amount)+")"
    self.charge += amount
    self.accepted = amount
    if self.charge > self.capacity: self.charge = self.capacity
  def get_value (self, key=None):
    if key==None or key=="level":
      return self.charge
    elif key=="input":
      return self.accepted
    else:
      print textred("Err: Unknown key '"+key+"' for FNodeBattery")
      dumpstack()
      sys.exit(10)

class FNodeLamp (FNode):
  def __init__ (self, upstream, wattage, luminousity, initial=1.0, consumers=None, ocnode=None, state=1):
    self.wattage = float(wattage)
    self.lum = float(luminousity)
    self.gain = float(initial)
    self.state = state
#    self.consumers = consumers
    self.output_cnode = ocnode
    if consumers != None:
      consumers.append(self)
    FNode.__init__(self, upstream)
  def get_luminousity (self):
    if self.state == 1:
      return self.accepted/self.wattage*self.lum
    else:
#      print "returning ZERO"
      return 0.0
  def step (self, stepsize):
    if fnode_debug: print "lamp.step("+str(stepsize)+")"
    self.amount = self.wattage*self.gain*stepsize
    self.upstream.request(self, self.amount)
  def accept (self, amount):
    if fnode_debug: print "lamp.accept("+str(amount)+")"
    if amount == self.amount:
      self.state = 1
      self.accepted = self.amount
    else:
      self.state = 0
      self.accepted = 0.0
    if self.output_cnode != None: self.output_cnode.update("a", self.get_luminousity())
  def get_value (self, key=None):
    if key==None or key=="input":
      return self.accepted
    elif key=="output":
      return self.get_luminousity()
    elif key=="gain":
      return self.gain
    elif key=="state":
      return self.state
    else:
      print textred("Err: Unknown key '"+key+"' for FNodeLamp")
      dumpstack()
      sys.exit(10)
  def set_value (self, key=None, value=None):
    if key==None or key=="state":
      self.state = value
    if key=="ocnode":
      self.output_cnode = value
    if key=="gain":
      self.gain = value
    else:
      print textred("Err: Unknown key '"+key+"' for FNodeLamp")
      dumpstack()
      sys.exit(10)

# perhaps rephrase luminousity to output in FNodeLamp
class FNodeHeater (FNodeLamp):
  def __init__ (self, upstream, wattage, luminousity, initial=1.0, consumers=None, ocnode=None, state=1):
#    print "FNodeHeater upstream="+str(upstream)+" wattage="+str(wattage)+" luminousity="+str(luminousity)+" initial="+str(initial)+" consumers="+str(consumers)+" ocnode="+str(ocnode)+" state="+str(state)
    FNodeLamp.__init__(self, upstream, wattage, luminousity, initial, consumers, ocnode, state)
    pass

class FNodeAircon (FNodeHeater):
  pass

class FNodeMultiplexer (FNode):
  def __init__ (self, upstreams, sel=0):
    self.upstreams = upstreams
    self.sel = sel
    FNode.__init__(self, upstreams[0])
  def select (self, sel):
    if fnode_debug: print "multiplexer.select("+str(sel)+")"
    self.sel = sel
    self.upstream = self.upstreams[sel]
  def get_value (self, key=None):
    if key==None or key=="sel":
      return self.sel
    elif key=="accepted":
      return self.accepted
    else:
      print textred("Err: Unknown key '"+key+"' for FNodeMultiplexer")
      dumpstack()
      sys.exit(10)
  def set_value (self, key=None, value=None):
    if key==None or key=="sel":
      self.sel = value
    else:
      print textred("Err: Unknown key '"+key+"' for FNodeMultiplexer")
      dumpstack()
      sys.exit(10)
    
  

class FNodeSourceModel:
  def __init__ (self, pushfun, tlist=None, maxup=60*60*24*365/12*3, maxdown=60*60*24*7):
    self.pushfun = pushfun
    self.maxup = maxup
    self.maxdown = maxdown
    self.state = 1
    self.schedule_change(0)
    if tlist != None: tlist.append(self)
  def flipstate (self):
    self.state = 0 if self.state==1 else 1
  def set_time (self, time):
    if time > self.changetime:
      self.flipstate()
      self.schedule_change(time)
      self.pushfun(self.state)
  def schedule_change (self, time):
    limit = self.maxup if self.state==1 else self.maxdown
    self.changetime = time + uniform(1, limit)
  def rerun (self):
    pass
  

class FNodeSource (FNode):
  def __init__ (self, state = 1):
    self.state = state
    FNode.__init__(self, None)
  def attempt (self, total):
    if fnode_debug: print "source.attempt("+str(total)+")"
    if self.state == 1:
      return True
    else:
      return False
  def get_value (self, key=None):
    if key==None or key=="output":
      return self.charge
    elif key=="state":
      return self.state
    else:
      print textred("Err: Unknown key '"+key+"' for FNodeSource")
      dumpstack()
      sys.exit(10)
  def set_value (self, key=None, value=None):
    if key==None or key=="state":
      self.state = value
    else:
      print textred("Err: Unknown key '"+key+"' for FNodeSource")
      dumpstack()
      sys.exit(10)

class FNodeSourceDynamic (FNode):
  def __init__ (self, cnode):
    self.cnode = cnode
    FNode.__init__(self, None)
  def attempt (self, total):
    if fnode_debug: print "sourcedyn.attempt("+str(total)+")"
    if total <= self.cnode.value:
      return True
    else:
      return False
  def get_value (self, key=None):
    if key==None or key=="output":
      return self.cnode.value
    else:
      print textred("Err: Unknown key '"+key+"' for FNodeSourceDynamic")
      dumpstack()
      sys.exit(10)


# could be derived from FNodePanel?
class FNodeGenerator (FNodePanel):
  def __init__ (self, upstream, capacity, efficiency, state = 1, primed = True, generators = None):
    self.capacity = float(capacity)
    self.efficiency = float(efficiency)
    self.state = state
    self.primed = primed
    FNodePanel.__init__(self, efficiency)
    self.upstream = upstream
    if upstream != None: upstream.register(self)
    self.generators = generators
    if generators != None:
      generators.append(self)
  def set_state (self, state):
    if state == 1:
      if self.primed:
        self.primed = False
        self.state = state
      else:
        return
  def set_primed (self, value):
    self.primed = value
  def step (self, stepsize):
    if fnode_debug: print "generator.step("+str(stepsize)+")"
    if self.state == 1:
      self.upstream.request(self, self.capacity/self.efficiency)
    else:
      self.charge = 0.0
  def accept (self, amount):
    if fnode_debug: print "generator.accept("+str(amount)+")"
    if amount < 1/self.efficiency:
      self.state = 0
      self.charge = 0.0
    else:
      self.charge = amount*self.efficiency
  def get_value (self, key=None):
    if key==None or key=="output":
      return self.charge
    elif key=="state":
      return self.state
    elif key=="primed":
      return 1.0 if self.primed else 0.0
    else:
      print textred("Err: Unknown key '"+key+"' for FNodeGenerator")
      dumpstack()
      sys.exit(10)
  def set_value (self, key=None, value=None):
    if key==None or key=="state":
      self.state = value
    elif key=="primed":
      self.primed = True if value == 1.0 else False
    else:
      print textred("Err: Unknown key '"+key+"' for FNodeGenerator")
      dumpstack()
      sys.exit(10)

# Essentially a battery
class FNodeTank (FNodeBattery):
  pass

class FNodeTap (FNodeLamp):
  def __init__ (self, upstream, wattage=1.0, initial=1.0, consumers=None, ocnode=None):
    FNodeLamp.__init__(self, upstream, wattage, luminousity=wattage, consumers=consumers, ocnode=ocnode)

class FNodeMains (FNodeSource):
  pass

class FNodeRain (FNodePanel):
  pass

# wraps a CNode
class FNodeBlinds (FNode):
  def __init__ (self, upstream, speed=9.83, efficiency=10.34, consumers=None, ocnode=None):
    self.setpoint = 1.0
    self.value = self.setpoint
    self.speed = float(speed)
    self.efficiency = float(efficiency)
    
    if consumers != None:
      consumers.append(self)
    self.output_cnode = ocnode
    FNode.__init__(self, upstream)
  def step (self, stepsize):
    if fnode_debug: print "blinds.step("+str(stepsize)+")"
    ideal = abs(self.setpoint-self.value)
    idealtime = ideal/self.speed
    self.amount = (idealtime if idealtime <= stepsize else self.speed)*self.efficiency
    self.upstream.request(self, self.amount)
  def accept (self, amount):
    if fnode_debug: print "blinds.accept("+str(amount)+")"
    if amount == self.amount:
      self.accepted = self.amount
      time = amount/self.efficiency
      diff = time*self.speed
      self.value = self.value+diff if self.setpoint>self.value else self.value-diff
    if self.output_cnode != None: self.output_cnode.update("a", self.value)
  def get_value (self, key=None):
    if key==None or key=="value":
      return self.value
    elif key=="setpoint":
      return self.setpoint
    else:
      print textred("Err: Unknown key '"+key+"' for FNodeBlinds")
      dumpstack()
      sys.exit(10)
  def set_value (self, key=None, value=None):
    if key==None or key=="value":
      self.state = value
    elif key=="setpoint":
      self.setpoint = value
    else:
      print textred("Err: Unknown key '"+key+"' for FNodeBlinds")
      dumpstack()
      sys.exit(10)
    
  

class FNodeList:
  def __init__ (self):
    self.l = []
  def append (self, node):
    self.l.append(node)
  def step (self, stepsize=0.1):
    for node in self.l:
      node.step(stepsize)
    
  

