# ex:set ts=4:

from BlueprintSupport import *

from sim.thermo import *
from sim.fnode import *
from sim.cnode import *
from sim.occupancy import *
from sim.siminterface import *
from sim.simplot import *

class BluePrint():
    def __init__(self, yearlimit=2, building=None):
        self.adj = []
        self.rooms = {}
        self.yearlimit = yearlimit
        self.building = building

    def prettyprint (self):
        print "room count = " + str(len(self.rooms))
        print "adj:"
        for i in range(len(self.adj)): print " " + str(self.adj[i][0]) + " <-> " + str(self.adj[i][1])

    def construct (self, starttime=0.0, dumpkeys=False, dumpkeysfile="/tmp/bisp_keys.txt"):
        DAYS_PER_YEAR = 365
        TEMPARATURE_OUTSIDE = 27

        self.time = starttime
        self.interface = interface = SimInterface()

        # lists
        self.nodelist = TNodeList()
        self.edgelist = TEdgeList()
        self.generators = FNodeList()
        self.buffers = FNodeList()
        self.consumers = FNodeList()
        self.cnodelist = CNodeList()
        self.timelist = tlist = CNodeList()
        
        lightwindows = []
        nodeRooms = dict()

        # Set environmental light
        self.lightscale = CNodeMul(map(lambda e: (e, "b"), lightwindows))  # "environment.light"
        self.lightscalefactor = CNodeConst([(self.lightscale, "a")], 11.43, self.cnodelist)  # scaling "from" temperature "to" light
        interface.register_get("environment-light", self.lightscale, lambda obj: obj.value)

        # environment
        self.cloud = TCloud(self.yearlimit * DAYS_PER_YEAR, self.yearlimit * 130)
        self.cnoutside = CNodeSun([(self.lightscale, "b")], self.cloud, tlist)
        self.cnrain = CNodeRain([], self.cloud, tlist)
        self.rainmodel = TNodeExposed(0, self.nodelist, self.cnrain, True)
        interface.register_get("environment-time", self.cnoutside, CNodeSun.get_value)
        interface.register_get("environment-cloudiness", self.cnoutside, lambda obj: CNodeSun.get_value(obj, "cloudiness"))
        interface.register_get("environment-rain", self.cnrain, lambda obj: CNodeRain.get_value(obj, "rain"))

        # occupancy
        self.occupancy = OccupancySimple(self.yearlimit * DAYS_PER_YEAR, 2, somelist=tlist)
        self.consumption = CNodeAdd([])
        self.consumptionstatic = CNodeConst([(self.consumption, "a")], 1.03, self.cnodelist)  # static water consumption
        self.occupancyconsumption = CNodeMul([(self.consumption, "b")])
        self.occupancyscale = CNodeConst([(self.occupancyconsumption, "a")], 0.0056, self.cnodelist)  # occupancy -> water consumption scale
        self.occupancycnode = CNodePull(lambda: self.occupancy.index(), [(self.occupancyconsumption, "b")], updatelist=self.cnodelist)  # link to OccupancySimple object
        interface.register_get("environment-occupancy", self.occupancy, OccupancySimple.index)

        # hydro layer
        self.generators = FNodeList()
        self.buffers = FNodeList()
        self.consumers = FNodeList()
        self.mains = FNodeMains()
        self.mainsmodel = FNodeSourceModel(lambda e: self.mains.set_value("state", e), tlist, 60 * 60 * 24 * 4, 60 * 60 * 12)
        self.rainsource = FNodeSourceDynamic(self.cnrain)
        self.rain = FNodeRain(self.rainsource, self.generators)
        self.htank = FNodeTank(100, 10, self.rain, self.buffers)
        self.hmux = FNodeMultiplexer([self.mains, self.htank], 0)
        self.tap = FNodeTap(self.hmux, 100, 60, self.consumers)
        interface.register_get("hydro-mains-state", self.mains, lambda obj: FNodeSource.get_value(obj, "state"))
        interface.register_set("hydro-mains-state", self.mains, lambda obj, value: FNodeSource.set_value(obj, "state", value))
        interface.register_get("hydro-rain-production", self.rain, lambda obj: FNodeRain.get_value(obj, "output"))
        interface.register_get("hydro-bassin-level", self.htank, lambda obj: FNodeTank.get_value(obj, "level"))
        interface.register_get("hydro-bassin-input", self.htank, lambda obj: FNodeTank.get_value(obj, "input"))
        interface.register_get("hydro-consumption", self.consumption, lambda obj: obj.value)
        interface.register_get("hydro-mux-accepted", self.hmux, lambda obj: FNodeMultiplexer.get_value(obj, "accepted"))
        interface.register_get("hydro-mux-select", self.hmux, lambda obj: FNodeMultiplexer.get_value(obj, "sel"))
        interface.register_set("hydro-mux-select", self.hmux, lambda obj, value: FNodeMultiplexer.set_value(obj, "sel", value))
        interface.register_get("hydro-tap-production", self.tap, lambda obj: FNodeTap.get_value(obj, "output"))
        interface.register_get("hydro-tap-state", self.tap, lambda obj: FNodeTap.get_value(obj, "state"))
        interface.register_set("hydro-tap-state", self.tap, lambda obj, value: FNodeTap.set_value(obj, "state", value))

        # energy layer
        self.etank1 = FNodeTank(20, 12)
        self.etank2 = FNodeTank(20, 12)
        self.grid = FNodeMains()
        self.gridmodel = FNodeSourceModel(lambda e: self.grid.set_value("state", e), tlist)
        self.generator1 = FNodeGenerator(self.etank1, 1.1, 0.5, 0, True, self.generators)
        self.generator2 = FNodeGenerator(self.etank2, 2.1, 0.55, 0, True, self.generators)
        self.panelsource = FNodeSourceDynamic(self.lightscale)
        self.panel = FNodePanel(self.panelsource, self.generators, 0.001)
        self.battery1 = FNodeBattery(100, 1, self.generator1, self.buffers)
        self.battery2 = FNodeBattery(100, 2, self.generator2, self.buffers)
        self.battery3 = FNodeBattery(100, 3, self.panel, self.buffers)
        self.emux = FNodeMultiplexer([self.grid, self.battery1, self.battery2, self.battery3], 0)
        interface.register_get("energy-fuel-1-level", self.etank1, lambda obj: FNodeTank.get_value(obj, "level"))
        interface.register_get("energy-fuel-1-input", self.etank1, lambda obj: FNodeTank.get_value(obj, "input"))
        interface.register_get("energy-fuel-2-level", self.etank2, lambda obj: FNodeTank.get_value(obj, "level"))
        interface.register_get("energy-fuel-2-input", self.etank2, lambda obj: FNodeTank.get_value(obj, "input"))
        interface.register_get("energy-grid-state", self.grid, lambda obj: FNodeSource.get_value(obj, "state"))
        interface.register_set("energy-grid-state", self.grid, lambda obj, value: FNodeSource.set_value(obj, "state", value))
        interface.register_get("energy-generator-1-production", self.generator1, lambda obj: FNodeGenerator.get_value(obj, "output"))
        interface.register_get("energy-generator-1-state", self.generator1, lambda obj: FNodeGenerator.get_value(obj, "state"))
        interface.register_set("energy-generator-1-state", self.generator1, lambda obj, value: FNodeGenerator.set_value(obj, "state", value))
        interface.register_get("energy-generator-1-primed", self.generator1, lambda obj: FNodeGenerator.get_value(obj, "primed"))
        interface.register_set("energy-generator-1-primed", self.generator1, lambda obj, value: FNodeGenerator.set_value(obj, "primed", value))
        interface.register_get("energy-generator-2-production", self.generator2, lambda obj: FNodeGenerator.get_value(obj, "output"))
        interface.register_get("energy-generator-2-state", self.generator2, lambda obj: FNodeGenerator.get_value(obj, "state"))
        interface.register_set("energy-generator-2-state", self.generator2, lambda obj, value: FNodeGenerator.set_value(obj, "state", value))
        interface.register_get("energy-generator-2-primed", self.generator2, lambda obj: FNodeGenerator.get_value(obj, "primed"))
        interface.register_set("energy-generator-2-primed", self.generator2, lambda obj, value: FNodeGenerator.set_value(obj, "primed", value))
        interface.register_get("energy-panel-production", self.panel, lambda obj: FNodePanel.get_value(obj, "output"))
        interface.register_get("energy-battery-1-level", self.battery1, FNodeBattery.get_value)
        interface.register_get("energy-battery-2-level", self.battery2, FNodeBattery.get_value)
        interface.register_get("energy-battery-3-level", self.battery3, FNodeBattery.get_value)
        interface.register_get("energy-mux-select", self.emux, lambda obj: FNodeMultiplexer.get_value(obj, "sel"))
        interface.register_set("energy-mux-select", self.emux, lambda obj, value: FNodeMultiplexer.set_value(obj, "sel", value))
        interface.register_get("energy-mux-energy", self.emux, lambda obj: FNodeMultiplexer.get_value(obj, "accepted"))

        # environment
        self.world = TWorld(self.nodelist, self.edgelist)
        self.outside = TNodeExposed(TEMPARATURE_OUTSIDE, self.nodelist, self.cnoutside, True)
        interface.register_get("environment.temp", self.outside, TNode.get_value)

        # half-iteration to initialize indoor temperature to outdoor temperature
        self.step()
        TEMPARATURE_INSIDE = self.outside.get_value()

        # room dynamic
        for room in self.building.getRooms():

            nodeRoom = nodeRooms[str(room.getLogicalID())] = TNode(TEMPARATURE_INSIDE, self.nodelist)

            interface.register_get(str(room.getLogicalID()) + ".temp", nodeRoom, TNode.get_value)
            #interface.register_get(str(room.getLogicalID()) + ".floor", self.rooms[room], lambda obj: obj["floor"])

            for (r1, r2) in self.adj: TEdge(self.rooms[r1]["roomnode"], self.rooms[r2]["roomnode"], 0.0002, self.edgelist) # ?

            # lamps
            lightSum = CNodeSum([], len(room.getLights()) + len(room.getBlinders()))
            interface.register_get(str(room.getLogicalID()) + "-light", lightSum, lambda obj: obj.value)
            i = 0
            for lamp in room.getLights():
                i += 1
                wattage = lamp.getWattage()
                lum = 0 #lamp.getIllu?
                initial = 0.0
                lightLamp = CNodeConst([(lightSum, str(i))], initial, self.cnodelist)
                nodeLamp =  FNodeLamp(self.emux, wattage, lum, consumers=self.consumers, ocnode=lightLamp) #?
                
                interface.register_get(str(lamp.getLogicalID()) + "-lightlamp", lightLamp, lambda obj: obj.value)

                interface.register_get(str(lamp.getLogicalID()) + "-production",  nodeLamp, lambda obj: FNodeLamp.get_value(obj, "output"))
                interface.register_get(str(lamp.getLogicalID()) + "-state", nodeLamp, lambda obj: FNodeLamp.get_value(obj, "state"))
                interface.register_get(str(lamp.getLogicalID()) + "-gain", nodeLamp, lambda obj: FNodeLamp.get_value(obj, "gain"))

                interface.register_set(str(lamp.getLogicalID()) + "-gain", nodeLamp, lambda obj, value: FNodeLamp.set_value(obj, "gain", value))

            # blinds
            for blind in room.getBlinders():
                size = blind.getSize()
                initial = 0.0
                i += 1

                nodeLightBlind = CNodeMul([(lightSum, str(i))])
                nodeLightBlindFactor = CNodeConst([(nodeLightBlind, "a")], initial, self.cnodelist)  # not really const, disregard initial value
                nodeBlind = FNodeBlinds(self.emux, consumers=self.consumers, ocnode=nodeLightBlindFactor) #?

                nodeLightWindow = CNodeMul([(nodeLightBlind, "b")])
                lightwindows.append(nodeLightWindow)

                nodeLightWindowSize = CNodeConst([(nodeLightWindow, "a")], size, self.cnodelist)  # size of window
                
                interface.register_get(str(blind.getLogicalID()) + "-nodelightBlind", nodeLightBlind, lambda obj: obj.value)
                interface.register_get(str(blind.getLogicalID()) + "-nodeLightBlindFactor", nodeLightBlindFactor, lambda obj: obj.value)
                interface.register_get(str(blind.getLogicalID()) + "-nodeLightWindow", nodeLightWindow, lambda obj: obj.value)
                interface.register_get(str(blind.getLogicalID()) + "-nodeLightWindowSize", nodeLightWindowSize, lambda obj: obj.value)

                interface.register_get(str(blind.getLogicalID()) + "-setpoint", nodeBlind, lambda obj: FNodeBlinds.get_value(obj, "setpoint"))
                interface.register_get(str(blind.getLogicalID()) + "-value", nodeBlind, lambda obj: FNodeBlinds.get_value(obj, "value"))

                interface.register_set(str(blind.getLogicalID()) + "-setpoint", nodeBlind, lambda obj, value: FNodeBlinds.set_value(obj, "setpoint", value))
                interface.register_set(str(blind.getLogicalID()) + "-value", nodeBlind, lambda obj, value: FNodeBlinds.set_value(obj, "value", value))

            # heaters
            for heater in room.getHeaters():
                nodeHeater = FNodeHeater(self.emux, heater.getWattage(), heater.getEfficiency(), initial = 0.0, consumers=self.consumers)
                heatNode = TNode(21, self.nodelist)

                CNodePullPush(lambda: nodeRoom.get_value() + nodeHeater.get_value("output"), lambda v: heatNode.set_value(v), updatelist=self.cnodelist)

                interface.register_get(str(heater.getLogicalID()) + "-production", nodeHeater, lambda obj: FNodeHeater.get_value(obj, "output"))
                interface.register_get(str(heater.getLogicalID()) + "-state", nodeHeater, lambda obj: FNodeHeater.get_value(obj, "state"))
                interface.register_get(str(heater.getLogicalID()) + "-gain", nodeHeater, lambda obj: FNodeHeater.get_value(obj, "gain"))

                interface.register_set(str(heater.getLogicalID()) + "-gain", nodeHeater, lambda obj, value: FNodeHeater.set_value(obj, "gain", value))

            # aircon
            for ac in room.getAcs():
                nodeAc = FNodeAircon(self.emux, ac.getWattage(), ac.getEfficiency(), initial = 0.0, consumers=self.consumers)
                heatNode = TNode(TEMPARATURE_INSIDE, self.nodelist)

                CNodePullPush(lambda: nodeRoom.get_value() + nodeAc.get_value("output"), lambda v: heatNode.set_value(v), updatelist=self.cnodelist)

                interface.register_get(str(ac.getLogicalID()) + "-production", nodeAc, lambda obj: FNodeHeater.get_value(obj, "output"))
                interface.register_get(str(ac.getLogicalID()) + "-state", nodeAc, lambda obj: FNodeHeater.get_value(obj, "state"))
                interface.register_get(str(ac.getLogicalID()) + "-gain", nodeAc, lambda obj: FNodeHeater.get_value(obj, "gain"))

                interface.register_set(str(ac.getLogicalID()) + "-gain", nodeAc, lambda obj, value: FNodeHeater.set_value(obj, "gain", value))

       
        # Tighten up dependencies
        for room in self.building.getRooms():
            TEdge(self.outside, nodeRooms[str(room.getLogicalID())], 0.0002, self.edgelist)

        # dump all valid keys to a file
        if dumpkeys:
            lines = []
            lines.append("Datapoints:\n")
            datapoints = sorted(interface.get_union())
            for i in range(len(datapoints)):
                point = datapoints[i]
                actions = []
                if interface.has_getter(point): actions.append("get")
                else: actions.append("   ")
                if interface.has_setter(point): actions.append("set")
                else: actions.append("   ")
                lines.append(" "+("%4d"%(i+1))+" "+str(point)+(" "*(max(map(lambda e: len(e), datapoints))-len(point)))+" "+(" ".join(actions))+"\n")

            fo = open(dumpkeysfile, "w")
            fo.writelines(lines)
            fo.close()

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

