#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ex:set ts=2:

from math import sin, pi

import sys
sys.path.append("../..")
from sim.thermo import *
from sim.fnode import *
from sim.cnode import *
from sim.occupancy import *
from sim.siminterface import *
from sim.simplot import *

TIME_PER_DAY = 3600*24
TIME_PER_YEAR = TIME_PER_DAY*365

class Simulator:
  pass

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
#    print self.value
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
#    print self.value
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
    self.value = math.sin(self.inputs["a"])

class SimulatorDemo (Simulator):
  def __init__ (self, logfilename, yearlimit=2):
    self.time = 0.0
    self.nodelist = TNodeList()
    self.edgelist = TEdgeList()
    tlist = CNodeList()
    self.timelist = tlist
    
    # light layer: sun, blinds, lamps
    self.cnodelist = CNodeList()
    self.room0lightsum = CNodeSum([], 2) # "hallway.light"
    self.room0lightlamp = CNodeConst([(self.room0lightsum, "1")], 0, self.cnodelist)
    self.room0lightblinds = CNodeMul([(self.room0lightsum, "2")])
    self.room0lightblindsfactor = CNodeConst([(self.room0lightblinds, "a")], 0, self.cnodelist) # not really const, disregard initial value
    self.room0lightwindow = CNodeMul([(self.room0lightblinds, "b")])
    self.room0lightwindowfactor = CNodeConst([(self.room0lightwindow, "a")], 1.07, self.cnodelist) # size of window
    self.room1lightsum = CNodeSum([], 2) # "room1.light"
    self.room1lightlamp = CNodeConst([(self.room1lightsum, "1")], 0, self.cnodelist)
    self.room1lightblinds = CNodeMul([(self.room1lightsum, "2")])
    self.room1lightblindsfactor = CNodeConst([(self.room1lightblinds, "a")], 0, self.cnodelist) # not really const, disregard initial value
    self.room1lightwindow = CNodeMul([(self.room1lightblinds, "b")])
    self.room1lightwindowfactor = CNodeConst([(self.room1lightwindow, "a")], 3.46, self.cnodelist) # size of window
    self.room2lightsum = CNodeSum([], 2) # "room2.light"
    self.room2lightlamp = CNodeConst([(self.room2lightsum, "1")], 0, self.cnodelist)
    self.room2lightblinds = CNodeMul([(self.room2lightsum, "2")])
    self.room2lightblindsfactor = CNodeConst([(self.room2lightblinds, "a")], 0, self.cnodelist) # not really const, disregard initial value
    self.room2lightwindow = CNodeMul([(self.room2lightblinds, "b")])
    self.room2lightwindowfactor = CNodeConst([(self.room2lightwindow, "a")], 5.12, self.cnodelist) # size of window
    self.lightscale = CNodeMul([(self.room0lightwindow, "b"), (self.room1lightwindow, "b"), (self.room2lightwindow, "b")]) # "environment.light"
    self.lightscalefactor = CNodeConst([(self.lightscale, "a")], 11.43, self.cnodelist) # scaling "from" temperature "to" light
# TODO: scale to stepsize
    
    # environment
    self.cloud = TCloud(yearlimit*365, yearlimit*130)
    self.cnoutside = CNodeSun([(self.lightscale, "b")], self.cloud, tlist)
    self.cnrain = CNodeRain([], self.cloud, tlist)
    self.rainmodel = TNodeExposed(0, self.nodelist, self.cnrain, True)
    
    # occupancy
    self.occupancy = OccupancySimple(yearlimit*365, 2, somelist=tlist)
    self.consumption_pusher = CNodePush(lambda e: self.tap.set_value("gain", e), updatelist=self.cnodelist)
    self.consumption = CNodeAdd([(self.consumption_pusher, "a")]) # TODO: need a push node!
    self.consumptionstatic = CNodeConst([(self.consumption, "a")], 1.03, self.cnodelist) # static water consumption
    self.occupancyconsumption = CNodeMul([(self.consumption, "b")])
    self.occupancyscale = CNodeConst([(self.occupancyconsumption, "a")], 0.0056, self.cnodelist) # occupancy -> water consumption scale
    self.occupancycnode = CNodePull(lambda: self.occupancy.index(), [(self.occupancyconsumption, "b")], updatelist=self.cnodelist) # link to OccupancySimple object
    
    # thermal layer
    self.world = TWorld(self.nodelist, self.edgelist)
    self.outside = TNodeExposed(27, self.nodelist, self.cnoutside, True)
    self.hallway = TNode(21, self.nodelist)
    self.room1   = TNode(23, self.nodelist)
    self.room2   = TNode(22.3, self.nodelist)
    self.hallwayheater = TNode(21, self.nodelist)
    self.room1heater = TNode(21, self.nodelist)
    self.room2heater = TNode(21, self.nodelist)
    self.hallwayaircon = TNode(21, self.nodelist)
    self.room1aircon = TNode(21, self.nodelist)
    self.room2aircon = TNode(21, self.nodelist)
    TEdge(self.outside, self.hallway, 0.0002, self.edgelist)
    TEdge(self.outside, self.room1, 0.00015, self.edgelist)
    TEdge(self.outside, self.room2, 0.00013, self.edgelist)
    TEdge(self.room1, self.hallway, 0.00008, self.edgelist)
    TEdge(self.room2, self.hallway, 0.00007, self.edgelist)
    TEdge(self.room1, self.room2, 0.00006, self.edgelist)
    TEdge(self.hallwayheater, self.hallway, 0.00075, self.edgelist)
    TEdge(self.room1heater, self.room1, 0.00028, self.edgelist)
    TEdge(self.room2heater, self.room2, 0.00017, self.edgelist)
    TEdge(self.hallwayaircon, self.hallway, 0.00075, self.edgelist)
    TEdge(self.room1aircon, self.room1, 0.00028, self.edgelist)
    TEdge(self.room2aircon, self.room2, 0.00017, self.edgelist)
    
    # hydro layer
    self.generators = FNodeList()
    self.buffers  = FNodeList()
    self.consumers  = FNodeList()
    self.mains = FNodeMains()
    self.mainsmodel = FNodeSourceModel(lambda e: self.mains.set_value("state", e), tlist, 60*60*24*4, 60*60*12)
    self.rainsource = FNodeSourceDynamic(self.cnrain)
    self.rain = FNodeRain(self.rainsource, self.generators)
    self.htank = FNodeTank(100, 10, self.rain, self.buffers)
    self.hmux = FNodeMultiplexer([self.mains, self.htank], 0)
    self.tap  = FNodeTap(self.hmux, consumers=self.consumers)
    
    # energy layer
    self.etank1 = FNodeTank(20, 12)
    self.etank2 = FNodeTank(20, 12)
    self.grid = FNodeMains()
    self.gridmodel = FNodeSourceModel(lambda e: self.grid.set_value("state", e), tlist, 60*60*24*3, 60*60*24)
    self.generator1 = FNodeGenerator(self.etank1, 1.1, 0.5, 0, True, self.generators)
    self.generator2 = FNodeGenerator(self.etank2, 2.1, 0.55, 0, True, self.generators)
    self.panelsource = FNodeSourceDynamic(self.lightscale)
    self.panel = FNodePanel(self.panelsource, self.generators, 0.001)
    self.battery1 = FNodeBattery(100, 1, self.generator1, self.buffers)
    self.battery2 = FNodeBattery(100, 2, self.generator2, self.buffers)
    self.battery3 = FNodeBattery(100, 3, self.panel, self.buffers)
    self.emux = FNodeMultiplexer([self.grid, self.battery1, self.battery2, self.battery3], 0)
    self.lamp0 = FNodeLamp(self.emux, 60, 30, consumers=self.consumers, ocnode=self.room0lightlamp)
    self.lamp1 = FNodeLamp(self.emux, 60, 30, consumers=self.consumers, ocnode=self.room1lightlamp)
    self.lamp2 = FNodeLamp(self.emux, 60, 30, consumers=self.consumers, ocnode=self.room2lightlamp)
    self.blinds0 = FNodeBlinds(self.emux, consumers=self.consumers, ocnode=self.room0lightblindsfactor)
    self.blinds1 = FNodeBlinds(self.emux, consumers=self.consumers, ocnode=self.room1lightblindsfactor)
    self.blinds2 = FNodeBlinds(self.emux, consumers=self.consumers, ocnode=self.room2lightblindsfactor)
    self.heater0 = FNodeHeater(self.emux, 1000, 20, initial=0.002, consumers=self.consumers)
    self.heater1 = FNodeHeater(self.emux, 1000, 20, initial=0.0, consumers=self.consumers)
    self.heater2 = FNodeHeater(self.emux, 1000, 20, initial=0.00011, consumers=self.consumers)
    self.aircon0 = FNodeAircon(self.emux, 1000, 20, initial=0.0, consumers=self.consumers)
    self.aircon1 = FNodeAircon(self.emux, 1000, 20, initial=0.013, consumers=self.consumers)
    self.aircon2 = FNodeAircon(self.emux, 1000, 20, initial=0.0, consumers=self.consumers)
    
    # stitching
    self.heater0thermo = CNodePullPush(lambda: self.hallway.get_value()+self.heater0.get_value("output"), lambda v: self.hallwayheater.set_value(v), updatelist=self.cnodelist)
    self.heater1thermo = CNodePullPush(lambda: self.hallway.get_value()+self.heater1.get_value("output"), lambda v: self.room1heater.set_value(v), updatelist=self.cnodelist)
    self.heater2thermo = CNodePullPush(lambda: self.hallway.get_value()+self.heater2.get_value("output"), lambda v: self.room2heater.set_value(v), updatelist=self.cnodelist)
    self.aircon0thermo = CNodePullPush(lambda: self.hallway.get_value()-self.aircon0.get_value("output"), lambda v: self.hallwayaircon.set_value(v), updatelist=self.cnodelist)
    self.aircon1thermo = CNodePullPush(lambda: self.hallway.get_value()-self.aircon1.get_value("output"), lambda v: self.room1aircon.set_value(v), updatelist=self.cnodelist)
    self.aircon2thermo = CNodePullPush(lambda: self.hallway.get_value()-self.aircon2.get_value("output"), lambda v: self.room2aircon.set_value(v), updatelist=self.cnodelist)
    
    # datapoints
    interface = SimInterface()
    self.interface = interface
    interface.register_get("time", self.cnoutside, CNodeSun.get_value)
    interface.register_get("environment.cloudiness", self.cnoutside, lambda obj: CNodeSun.get_value(obj, "cloudiness"))
    interface.register_get("environment.rain", self.cnrain, lambda obj: CNodeRain.get_value(obj, "rain"))
    interface.register_get("environment.light", self.lightscale, lambda obj: obj.value)
    interface.register_get("occupancy", self.occupancy, OccupancySimple.index)
    interface.register_get("outside.temp", self.outside, TNodeExposed.get_value)
    interface.register_get("hallway.temp", self.hallway, TNode.get_value)
    interface.register_get("room1.temp", self.room1, TNode.get_value)
    interface.register_get("room2.temp", self.room2, TNode.get_value)
    interface.register_get("fuel[1].level", self.etank1, lambda obj: FNodeTank.get_value(obj, "level"))
    interface.register_get("fuel[1].input", self.etank1, lambda obj: FNodeTank.get_value(obj, "input"))
    interface.register_get("fuel[2].level", self.etank2, lambda obj: FNodeTank.get_value(obj, "level"))
    interface.register_get("fuel[2].input", self.etank2, lambda obj: FNodeTank.get_value(obj, "input"))
    interface.register_get("grid.state", self.grid, lambda obj: FNodeSource.get_value(obj, "state"))
    interface.register_set("grid.state", self.grid, lambda obj,value: FNodeSource.set_value(obj, "state", value))
    interface.register_get("generator[1].production", self.generator1, lambda obj: FNodeGenerator.get_value(obj, "output"))
    interface.register_get("generator[1].state", self.generator1, lambda obj: FNodeGenerator.get_value(obj, "state"))
    interface.register_set("generator[1].state", self.generator1, lambda obj,value: FNodeGenerator.set_value(obj, "state", value))
    interface.register_get("generator[2].production", self.generator2, lambda obj: FNodeGenerator.get_value(obj, "output"))
    interface.register_get("generator[2].state", self.generator2, lambda obj: FNodeGenerator.get_value(obj, "state"))
    interface.register_set("generator[2].state", self.generator2, lambda obj,value: FNodeGenerator.set_value(obj, "state", value))
    interface.register_get("panel.production", self.panel, lambda obj: FNodePanel.get_value(obj, "output"))
    interface.register_get("battery[1].level", self.battery1, FNodeBattery.get_value)
    interface.register_get("battery[2].level", self.battery2, FNodeBattery.get_value)
    interface.register_get("battery[3].level", self.battery3, FNodeBattery.get_value)
    interface.register_get("emux.select", self.emux, lambda obj: FNodeMultiplexer.get_value(obj, "sel"))
    interface.register_set("emux.select", self.emux, lambda obj,value: FNodeMultiplexer.set_value(obj, "sel", value))
    interface.register_get("hallway.light", self.room0lightsum, lambda obj: obj.value)
    interface.register_get("hallway.blinds.setpoint", self.blinds0, lambda obj: FNodeBlinds.get_value(obj, "setpoint"))
    interface.register_set("hallway.blinds.setpoint", self.blinds0, lambda obj,value: FNodeBlinds.set_value(obj, "setpoint", value))
    interface.register_get("hallway.blinds.value", self.blinds0, lambda obj: FNodeBlinds.get_value(obj, "value"))
    interface.register_set("hallway.blinds.value", self.blinds0, lambda obj,value: FNodeBlinds.set_value(obj, "value", value))
    interface.register_get("hallway.lamp.production", self.lamp0, lambda obj: FNodeLamp.get_value(obj, "output"))
    interface.register_get("hallway.lamp.state", self.lamp0, lambda obj: FNodeLamp.get_value(obj, "state"))
    interface.register_get("hallway.lamp.gain", self.lamp0, lambda obj: FNodeLamp.get_value(obj, "gain"))
    interface.register_set("hallway.lamp.gain", self.lamp0, lambda obj,value: FNodeLamp.set_value(obj, "gain", value))
    interface.register_get("hallway.heater.production", self.heater0, lambda obj: FNodeHeater.get_value(obj, "output"))
    interface.register_get("hallway.heater.state", self.heater0, lambda obj: FNodeHeater.get_value(obj, "state"))
    interface.register_get("hallway.heater.gain", self.heater0, lambda obj: FNodeHeater.get_value(obj, "gain"))
    interface.register_set("hallway.heater.gain", self.heater0, lambda obj,value: FNodeHeater.set_value(obj, "gain", value))
    interface.register_get("hallway.aircon.production", self.aircon0, lambda obj: FNodeAircon.get_value(obj, "output"))
    interface.register_get("hallway.aircon.state", self.aircon0, lambda obj: FNodeAircon.get_value(obj, "state"))
    interface.register_get("hallway.aircon.gain", self.aircon0, lambda obj: FNodeAircon.get_value(obj, "gain"))
    interface.register_set("hallway.aircon.gain", self.aircon0, lambda obj,value: FNodeAircon.set_value(obj, "gain", value))
    interface.register_get("room1.light", self.room1lightsum, lambda obj: obj.value)
    interface.register_get("room1.blinds.setpoint", self.blinds1, lambda obj: FNodeBlinds.get_value(obj, "setpoint"))
    interface.register_set("room1.blinds.setpoint", self.blinds1, lambda obj,value: FNodeBlinds.set_value(obj, "setpoint", value))
    interface.register_get("room1.blinds.value", self.blinds1, lambda obj: FNodeBlinds.get_value(obj, "value"))
    interface.register_set("room1.blinds.value", self.blinds1, lambda obj,value: FNodeBlinds.set_value(obj, "value", value))
    interface.register_get("room1.lamp.production", self.lamp1, lambda obj: FNodeLamp.get_value(obj, "output"))
    interface.register_get("room1.lamp.state", self.lamp1, lambda obj: FNodeLamp.get_value(obj, "state"))
    interface.register_get("room1.lamp.gain", self.lamp1, lambda obj: FNodeLamp.get_value(obj, "gain"))
    interface.register_set("room1.lamp.gain", self.lamp1, lambda obj,value: FNodeLamp.set_value(obj, "gain", value))
    interface.register_get("room1.heater.production", self.heater1, lambda obj: FNodeHeater.get_value(obj, "output"))
    interface.register_get("room1.heater.state", self.heater1, lambda obj: FNodeHeater.get_value(obj, "state"))
    interface.register_get("room1.heater.gain", self.heater1, lambda obj: FNodeHeater.get_value(obj, "gain"))
    interface.register_set("room1.heater.gain", self.heater1, lambda obj,value: FNodeHeater.set_value(obj, "gain", value))
    interface.register_get("room1.aircon.production", self.aircon1, lambda obj: FNodeAircon.get_value(obj, "output"))
    interface.register_get("room1.aircon.state", self.aircon1, lambda obj: FNodeAircon.get_value(obj, "state"))
    interface.register_get("room1.aircon.gain", self.aircon1, lambda obj: FNodeAircon.get_value(obj, "gain"))
    interface.register_set("room1.aircon.gain", self.aircon1, lambda obj,value: FNodeAircon.set_value(obj, "gain", value))
    interface.register_get("room2.light", self.room2lightsum, lambda obj: obj.value)
    interface.register_get("room2.blinds.setpoint", self.blinds2, lambda obj: FNodeBlinds.get_value(obj, "setpoint"))
    interface.register_set("room2.blinds.setpoint", self.blinds2, lambda obj,value: FNodeBlinds.set_value(obj, "setpoint", value))
    interface.register_get("room2.blinds.value", self.blinds2, lambda obj: FNodeBlinds.get_value(obj, "value"))
    interface.register_set("room2.blinds.value", self.blinds2, lambda obj,value: FNodeBlinds.set_value(obj, "value", value))
    interface.register_get("room2.lamp.production", self.lamp2, lambda obj: FNodeLamp.get_value(obj, "output"))
    interface.register_get("room2.lamp.state", self.lamp2, lambda obj: FNodeLamp.get_value(obj, "state"))
    interface.register_get("room2.lamp.gain", self.lamp2, lambda obj: FNodeLamp.get_value(obj, "gain"))
    interface.register_set("room2.lamp.gain", self.lamp2, lambda obj,value: FNodeLamp.set_value(obj, "gain", value))
    interface.register_get("room2.heater.production", self.heater2, lambda obj: FNodeHeater.get_value(obj, "output"))
    interface.register_get("room2.heater.state", self.heater2, lambda obj: FNodeHeater.get_value(obj, "state"))
    interface.register_get("room2.heater.gain", self.heater2, lambda obj: FNodeHeater.get_value(obj, "gain"))
    interface.register_set("room2.heater.gain", self.heater2, lambda obj,value: FNodeHeater.set_value(obj, "gain", value))
    interface.register_get("room2.aircon.production", self.aircon2, lambda obj: FNodeAircon.get_value(obj, "output"))
    interface.register_get("room2.aircon.state", self.aircon2, lambda obj: FNodeAircon.get_value(obj, "state"))
    interface.register_get("room2.aircon.gain", self.aircon2, lambda obj: FNodeAircon.get_value(obj, "gain"))
    interface.register_set("room2.aircon.gain", self.aircon2, lambda obj,value: FNodeAircon.set_value(obj, "gain", value))
    interface.register_get("mains.state", self.mains, lambda obj: FNodeSource.get_value(obj, "state"))
    interface.register_set("mains.state", self.mains, lambda obj,value: FNodeSource.set_value(obj, "state", value))
    interface.register_get("rain.production", self.rain, lambda obj: FNodeRain.get_value(obj, "output"))
    interface.register_get("bassin.level", self.htank, lambda obj: FNodeTank.get_value(obj, "level"))
    interface.register_get("bassin.input", self.htank, lambda obj: FNodeTank.get_value(obj, "input"))
    interface.register_get("hydro.consumption", self.consumption, lambda obj: obj.value)
    interface.register_get("hmux.accepted", self.hmux, lambda obj: FNodeMultiplexer.get_value(obj, "accepted"))
    interface.register_get("hmux.select", self.hmux, lambda obj: FNodeMultiplexer.get_value(obj, "sel"))
    interface.register_set("hmux.select", self.hmux, lambda obj,value: FNodeMultiplexer.set_value(obj, "sel", value))
    interface.register_get("tap.production", self.tap, lambda obj: FNodeTap.get_value(obj, "output"))
    interface.register_get("tap.state", self.tap, lambda obj: FNodeTap.get_value(obj, "state"))
    interface.register_set("tap.state", self.tap, lambda obj,value: FNodeTap.set_value(obj, "state", value))
    interface.attach_log(logfilename)
  
  def step (self, stepsize=0.1, stepcount=1):
    for _ in range(stepcount):
      self.timelist.map(lambda e:e.set_time(self.time))
      self.timelist.rerun()
      self.cnodelist.rerun()
      self.world.step(stepsize)
      self.generators.step(stepsize)
      self.buffers.step(stepsize)
      self.consumers.step(stepsize)
      self.time += stepsize
    self.interface.log()
  
  def get_interface (self):
    return self.interface
  

if __name__ == '__main__':
  filename = "demo.py.csv"
  print "Building Demo"
  print " - Log: '"+filename+"'"
  print ""
  building = SimulatorDemo(filename)
  
  # print info
  print "Datapoints:"
  datapoints = sorted(building.interface.get_union())
  for i in range(len(datapoints)):
    point = datapoints[i]
    actions = []
    if building.interface.has_getter(point): actions.append(textblue("get"))
    else: actions.append("   ")
    if building.interface.has_setter(point): actions.append(textblue("set"))
    else: actions.append("   ")
    print " "+("%2d"%(i+1))+" "+str(point)+(" "*(max(map(lambda e: len(e), datapoints))-len(point)))+" "+(" ".join(actions))
  print ""
  
  # run simulation
  print "Running simulation ..."
  simlength = 60*24*7
  for i in range(simlength):
    if i in map(lambda e: (simlength/100)*e, range(10, 101, 10)): print str(i/(simlength/100))+"%"
    building.step(60.0)
  print ""
  
  # processing results
  print "Processing results ..."
  log = building.interface.l
  graph = SimPlot("demo_temp", "png", "size 1680,1050")
  graph.append("Time", "Temperature/°C",
               [log, log, log, log],
               ["time", "time", "time", "time"],
               ["outside.temp", "hallway.temp", "room1.temp", "room2.temp"],
               "lines",
               ["Outside", "Hallway", "Room 1", "Room 2"])
  graph.append("Time", "Light",
               [log, log, log],
               ["time", "time", "time"],
               ["hallway.light", "room1.light", "room2.light"],
               "lines",
               ["Hallway", "Room 1", "Room 2"])
  graph.append("Time", "Occupancy",
               [log],
               ["time"],
               ["occupancy"],
               "lines",
               ["General"])
  graph.append("Time", "Water",
               [log, log, log],
               ["time", "time", "time"],
               ["bassin.input", "bassin.level", "hmux.accepted"],
               "lines",
               ["Rain", "Bassin", "Consumption"],
               yaxisscale="log")
  graph.generate("seconds")
  

