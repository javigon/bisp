# ex:set ts=4:

import sys
if "../" not in sys.path: sys.path.append("../")
if "../../" not in sys.path: sys.path.append("../../")
if "../../../" not in sys.path: sys.path.append("../../../")
from Blueprint import *

class BlueprintBuilder:
    def __init__ (self, building):
        self.building = building

    def build (self, years=20):
        self.blueprint = BluePrint(yearlimit=years, building=self.building)
#        from bif.impl import dummy2 as Dummy
#        self.building = BluePrint(yearlimit=years)
#        dummy = Dummy.DummyBif(self.building)
#        
#        # adding rooms-related stuff
#        for room in range(dummy.getNumRooms(self.building)):
#            # add room
#            floor  = dummy.getRoomFloor(self.building, room)
#            self.building.addRoom(room, floor)
#            
#            # add lamps
#            for lamp in dummy.getRoomServ("light", self.building, room):
#                wattage     = float(dummy.getExpenditureServ(self.building, "light", lamp))
#                luminousity = float(dummy.getEfficiencyServ(self.building, "light", lamp))
#                initial     = 0.0
#                self.building.addLamp(room, lamp, wattage, luminousity, initial)
#                
#            # add heaters
#            for heater in dummy.getRoomServ("heating", self.building, room):
#                wattage    = float(dummy.getExpenditureServ(self.building, "heating", heater))
#                efficiency = float(dummy.getEfficiencyServ(self.building, "heating", heater))
#                initial    = 0.0
#                self.building.addHeater(room, heater, wattage, efficiency, initial)
#                
#            # add acs
#            for ac in dummy.getRoomServ("air", self.building, room):
#                wattage    = float(dummy.getExpenditureServ(self.building, "air", ac))
#                efficiency = float(dummy.getEfficiencyServ(self.building, "air", ac))
#                initial    = 0.0
#                self.building.addAc(room, ac, wattage, efficiency, initial)
#                
#            # add blinds
#            for blind in dummy.getRoomServ("blinds", self.building, room):
#                wattage    = float(dummy.getExpenditureServ(self.building, "blinds", blind))
#                speed      = 9.83
#                efficiency = float(dummy.getEfficiencyServ(self.building, "blinds", blind))
#                size       = float(dummy.getSizeServ(self.building, "blinds", blind))
#                initial    = 0.0
#                self.building.addBlinds(room, blind, speed, efficiency, size, initial)
#                
#        
#        # adding edges
#        for e in dummy.getRoomPairList(self.building):
#            self.building.addEdge(e[0], e[1])
            
        # tie together building
        self.blueprint.construct()
    
if __name__ == '__main__':
    bb = BlueprintBuilder(0)
    bb.build()
    building = bb.building
    
    def textblue(arg1):
        return arg1
    
    print "Datapoints:"
    datapoints = sorted(building.interface.get_union())
    for i in range(len(datapoints)):
        point = datapoints[i]
        actions = []
        if building.interface.has_getter(point): actions.append(textblue("get"))
        else: actions.append("   ")
        if building.interface.has_setter(point): actions.append(textblue("set"))
        else: actions.append("   ")
        print " "+("%3d"%(i+1))+" "+str(point)+(" "*(max(map(lambda e: len(e), datapoints))-len(point)))+" "+(" ".join(actions))
    print ""
    
    building.step(stepcount=600)

