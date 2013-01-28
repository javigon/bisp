from building.impl import building
import buildingCreator
from building import bif


class DummyBif(bif.BifBase):
    "Dummy implementation of the bif interface"


    def __init__(self, buildingID):
        '''
        We add the building services this implementation of bif implements
        Any service implemented in this interface MUST be added here.

        buildingIDs can be an integer (int) if only one building is needed,
        or a list of integers list[int] if more buildinggs (only one is possible too)
        are needed

        '''
        super(DummyBif, self).__init__()
        super(DummyBif, self).implService("LIGHT")
        super(DummyBif, self).implService("WATER")
        super(DummyBif, self).implService("AIR") #Air Condition
        super(DummyBif, self).implService("BLINDS") #Roller Blinders
        super(DummyBif, self).implService("HEATING") #Roller Blinders

        ############## DEFINITIONS ###############
        self.buildingID = buildingID
        self.simBuilding = building.Building(buildingID)

        #Create building instance
        buildingCreator.buildingCreator(self.simBuilding)
            


    '''
        #######################################
        Public Methods
        #######################################
    '''
    ##Implementation of abstract methods common to all services

    ##Building Architecture
    def getNumFloors(self):
        '''
                    int getNumFloors(self)

                    Returns the number of floors in the building 
        '''
        #We find out the name of the private method implementing the service
        method_name = bif.BifBase.getNumFloors(self)
        #We get the method itself
        servMethod = getattr(self,method_name)
        #We call the method with the necessary parameters and return its return
        return servMethod()

    def getNumRooms(self):
        '''
                    int getNumRooms(self)

                    Returns the number of rooms in a building
        '''
        #We find out the name of the private method implementing the service
        method_name = bif.BifBase.getNumRooms(self)
        #We get the method itself
        servMethod = getattr(self,method_name)
        #We call the method with the necessary parameters and return its return
        return servMethod()

    def getRoomFloor(self, roomID):
        '''
                    int getRoomFloor(self, roomID)

                    Returns the floor in which a room (roomID) is located in a building 
        '''
        #We find out the name of the private method implementing the service
        method_name = bif.BifBase.getRoomFloor(self, roomID)
        #We get the method itself
        servMethod = getattr(self,method_name)
        #We call the method with the necessary parameters and return its return
        return servMethod(roomID)


    def getAdjacentRooms(self, roomID):
        '''
                    list getAdjacentRooms(self, roomID)

                    Returns the adjacent rooms to a given room (roomID) in a building 
        '''
        return self._getAdjacentRooms(roomID)

    def getNumRoomPairs(self):
        '''
                    int getAdjacentRooms(self, roomID)

                    Returns the number of room adjacencies in a building.
        '''
        #We find out the name of the private method implementing the service
        method_name = bif.BifBase.getNumRoomPairs(self)
        #We get the method itself
        servMethod = getattr(self,method_name)
        #We call the method with the necessary parameters and return its return
        return servMethod()

    def getRoomPairList(self):
        '''
                    getRoomPairList(self)

                    Returns all the room adjacencies in pairs (sorted by int ID) in a building .
        '''
        #We find out the name of the private method implementing the service
        method_name = bif.BifBase.getRoomPairList(self)
        #We get the method itself
        servMethod = getattr(self,method_name)
        #We call the method with the necessary parameters and return its return
        return servMethod()

    def getRoomList(self):
        '''
                    getRoomList(self)

                    Returns all the rooms in a building (sorted by int ID).
        '''
        #We find out the name of the private method implementing the service
        method_name = bif.BifBase.getRoomList(self)
        #We get the method itself
        servMethod = getattr(self,method_name)
        #We call the method with the necessary parameters and return its return
        return servMethod()

    def getRooms(self):
        '''
                    getRoomList(self)

                    Returns all the rooms in a building (sorted by int ID).
        '''
        #We find out the name of the private method implementing the service
        method_name = bif.BifBase.getRooms(self)
        #We get the method itself
        servMethod = getattr(self,method_name)
        #We call the method with the necessary parameters and return its return
        return servMethod()

    ##Services
    def getRoomHasServ(self, service, roomID):
        '''
                    getRoomServ(self, service, roomID)

                    Returns if a room (roomID) has at least 1 occurrence of a given service (boolean).

                    service in ['light', 'water', 'air', 'blinds', 'heating'] which are the services implemented
                    in this instantiation of the building. This services might vary.
        '''
        #We find out the name of the private method implementing the service
        method_name = bif.BifBase.getRoomHasServ(self, service, roomID)
        #We get the method itself
        servMethod = getattr(self,method_name)
        #We call the method with the necessary parameters and return its return
        return servMethod(roomID)

    def getNumBuildingServ(self, service):
        '''
                    getNumBuildingServ(self, service)

                    Returns number of instances of a service are in a building.

                    service in ['light', 'water', 'air', 'blinds', 'heating'] which are the services implemented
                    in this instantiation of the building. This services might vary.
        '''
        #We find out the name of the private method implementing the service
        method_name = bif.BifBase.getNumBuildingServ(self, service)
        #We get the method itself
        servMethod = getattr(self,method_name)
        #We call the method with the necessary parameters and return its return
        return servMethod()

    def getNumFloorServ(self, service, floorID):
        '''
                    getNumFloorServ(self, service, floorID)

                    Returns number of instances of a service are in a building-floor (floorID).

                    service in ['light', 'water', 'air', 'blinds', 'heating'] which are the services implemented
                    in this instantiation of the building. This services might vary.
        '''
        #We find out the name of the private method implementing the service
        method_name = bif.BifBase.getNumFloorServ(self, service, floorID)
        #We get the method itself
        servMethod = getattr(self,method_name)
        #We call the method with the necessary parameters and return its return
        return servMethod(floorID)

    def getNumRoomServ(self, service, roomID):
        '''
                    getNumRoomServ(self, service, roomID)

                    Returns number of instances of a service are in a building-room ( roomID).

                    service in ['light', 'water', 'air', 'blinds', 'heating'] which are the services implemented
                    in this instantiation of the building. This services might vary.
        '''
        #We find out the name of the private method implementing the service
        method_name = bif.BifBase.getNumRoomServ(self, service, roomID)
        #We get the method itself
        servMethod = getattr(self,method_name)
        #We call the method with the necessary parameters and return its return
        return servMethod(roomID)


    def getBuildingServ(self, service):
        '''
                    getBuildingServ(self, service)

                    Returns the list of a service instances in a building.

        '''
        #We find out the name of the private method implementing the service
        method_name = bif.BifBase.getBuildingServ(self, service)
        #We get the method itself
        servMethod = getattr(self,method_name)
        #We call the method with the necessary parameters and return its return
        return servMethod()

    def getFloorServ(self, service, floorID):
        '''
                    getFloorServ(self, service, floorID)

                    Returns the list of a service instances in a building-floor (floorID)

        '''
        #We find out the name of the private method implementing the service
        method_name = bif.BifBase.getFloorServ(self, service, floorID)
        #We get the method itself
        servMethod = getattr(self,method_name)
        #We call the method with the necessary parameters and return its return
        return servMethod(floorID)

    def getRoomServ(self, service, roomID):
        '''
                    getRoomServ(self, service, roomID)

                    Returns the list of a service instances in a building-room (roomID)

        '''
        #We find out the name of the private method implementing the service
        method_name = bif.BifBase.getRoomServ(self, service, roomID)
        #We get the method itself
        servMethod = getattr(self,method_name)
        #We call the method with the necessary parameters and return its return
        return servMethod(roomID)

    def getEfficiencyServ(self, service, serviceID):
        '''
                    getEfficiencyServ(self, service, serviceID)

                    Returns the efficiency of a service instance (serviceID) in a building

        '''
        #We find out the name of the private method implementing the service
        method_name = bif.BifBase.getEfficiencyServ(self, service, serviceID)
        #We get the method itself
        servMethod = getattr(self,method_name)
        #We call the method with the necessary parameters and return its return
        return servMethod(serviceID)

    def getExpenditureServ(self, service, serviceID):
        '''
                    getEfficiencyServ(self, service, serviceID)

                    Returns the expenditure of a service instance (serviceID) in a building 
                    Expenditure is e.g. Wattage in terms of Electric Power


        '''
        #We find out the name of the private method implementing the service
        method_name = bif.BifBase.getExpenditureServ(self, service, serviceID)
        #We get the method itself
        servMethod = getattr(self,method_name)
        #We call the method with the necessary parameters and return its return
        return servMethod(serviceID)

    #Only for those services in which this makes sense.
    def getSizeServ(self, service, serviceID):
        '''
                    getSizeServ(self, service, serviceID)

                    Returns the size of a service instance (serviceID) in a building

        '''
        #We find out the name of the private method implementing the service
        method_name = bif.BifBase.getSizeServ(self, service, serviceID)
        #We get the method itself
        servMethod = getattr(self,method_name)
        #We call the method with the necessary parameters and return its return
        return servMethod(serviceID)




    '''
        ##############################################
        Private Methods - Architectural Implementation
        ##############################################
    '''

    def _getNumFloors(self):
        '''
                    _getNumFloors(self)
        '''
        return self.simBuilding.getNumFloors()

    def _getNumRooms(self):
        '''
                    _getNumRooms(self)
        '''
        return self.simBuilding.getNumRooms()

    def _getRoomFloor(self, roomID):
        '''
                    _getRoomFloor(self, roomID)
        '''
        return self.simBuilding.getRoomFloor(roomID)

    '''
        ##############################################
        Private Methods - Architectural Implementation
        ##############################################
    '''

    def _getAdjacentRooms(self, roomID):
        '''
                    _getAdjacentRooms(self, roomID)
        '''
        #Returns number of room connections (edges)
        return self.simBuilding.getAdjacentRooms(roomID)



    def _getNumRoomPairs(self):
        '''
                    _getNumRoomPairs(self)
        '''
        #Returns number of room connections (edges)
        return len(self.simBuilding.getRoomPairs())

    def _getRoomPairList(self):
        '''
                    _getRoomPairList(self)
        '''
        myRoomNodeIDs=[]
        roomPair=[]

        myEdges=self.simBuilding.getRoomPairs()
        for i in range (len(myEdges)):
            roomPair=[(myEdges[i][0]).getID(),(myEdges[i][1]).getID()]
            roomPair.sort(key=int)
            myRoomNodeIDs.append(roomPair)

        return myRoomNodeIDs

    def _getRoomList(self):
        '''
                    _getRoomList(self)
        '''
        myRoomIDs=[]
        myRooms=self.simBuilding.getRooms()
        for i in range (len(myRooms)):
            myRoomIDs.append(myRooms[i].getID())

        return sorted(myRoomIDs, key=int)

    def _getRooms(self):
        '''
            _getRooms(self)
        '''
        return self.simBuilding.getRooms()

    '''
        #######################################
        Private Methods - Service Implementation
        #######################################
    '''
    ##Lightning Services

    def _servEfficiency_light(self, lightID):
        '''
                    _servEfficiency_light(self, lightID)
        '''
        light =self.simBuilding.getLight(lightID)
        return light.getEfficiency()

    def _servExpenditure_light(self, lightID):
        '''
                    _servEfficiency_light(self, lightID)
        '''
        light =self.simBuilding.getLight(lightID)
        return light.getWattage()

    def _servSize_light(self, lightID):
        '''
                    _servSize_light(self, lightID)

        '''
        #Light has no size
        return 0

    def _servListBuilding_light(self):
        '''
                    _servListBuilding_light(self)
        '''
        return self.simBuilding.getLightIDs()

    def _servListFloor_light(self, floorID):
        '''
                   _servListFloor_light(self, floorID)
        '''
        return self.simBuilding.getLightIDsFloor(floorID)

    def _servListRoom_light(self, roomID):
        '''
                   _servListRoom_light(self, roomID)
        '''
        return self.simBuilding.getLightIDsRoom(roomID)


    def _servRoomHas_light(self, roomID):
        '''
                    _servRoomHas_light(self, roomID)
        '''
        room=self.simBuilding.getRoom(roomID)
        if room.hasLights:
            return True
        else:
            return False

    def _servNumBuilding_light(self):
        '''         _servNumBuilding_light(self)

        '''
        return self.simBuilding.getNumLights()


    def _servNumFloor_light(self, floorID):
        '''         _servNumFloor_light(self, floorID)

        '''
        return self.simBuilding.getNumLightsFloor(floorID)

    def _servNumRoom_light(self, roomID):
        '''         _servNumRoom_light(self, roomID)

        '''
        return self.simBuilding.getNumLightsRoom(roomID)


    ##Watering Services

    def _servEfficiency_water(self, waterAPID):
        '''
                    _servEfficiency_water(self, waterAPID)
        '''
        waterAP =self.simBuilding.getWater(waterAPID)
        return waterAP.getEfficiency()

    def _servExpenditure_water(self, waterAPID):
        '''
                    _servEfficiency_water(self, waterAPID)
        '''
        waterAP =self.simBuilding.getWater(waterAPID)
        return waterAP.getFlow()

    def _servSize_water(self, waterID):
        '''
                    _servSize_light(self, waterID)

        '''
        #WaterAPs has no size
        return 0

    def _servListBuilding_water(self):
        '''
                    _servListBuilding_water(self)
        '''
        return self.simBuilding.getWaterIDs()

    def _servListFloor_water(self, floorID):
        '''
                   _servListFloor_light(self, floorID)
        '''
 

        return self.simBuilding.getWaterIDsFloor(floorID)

    def _servListRoom_water(self, roomID):
        '''
                   _servListRoom_light(self, roomID)
        '''
        return self.simBuilding.getWaterIDsRoom(roomID)

    def _servRoomHas_water(self, roomID):
        '''
                    _servRoomHas_water(self, roomID)
        '''
        room=self.simBuilding.getRoom(roomID)
        if room.hasWater():
            return True
        else:
            return False

    def _servNumBuilding_water(self):
        '''          _servNumBuilding_water(self)


        '''
        return self.simBuilding.getNumWaterAPs()


    def _servNumFloor_water(self, floorID):
        '''         _servNumFloor_water(self, floorID)


        '''
        return self.simBuilding.getNumWaterAPsFloor(floorID)


    def _servNumRoom_water(self, roomID):
        '''         _servNumRoom_water(self, roomID)

        '''
        return self.simBuilding.getNumWaterAPsRoom(roomID)


    ##Air Conditioning Services

    def _servEfficiency_air(self, ACID):
        '''
                    _servEfficiency_air(self, ACID)
        '''
        AC =self.simBuilding.getAC(ACID)
        return AC.getEfficiency()

    def _servExpenditure_air(self, ACID):
        '''
                    _servEfficiency_light(self, airID)
        '''
        AC =self.simBuilding.getAC(ACID)
        return AC.getWattage()

    def _servSize_air(self, airID):
        '''
                    _servSize_light(self, airID)

        '''
        #Air-Condition has no size
        return 0

    def _servListBuilding_air(self):
        '''
                    _servListBuilding_water(self)
        '''
        return self.simBuilding.getACIDs()

    def _servListFloor_air(self, floorID):
        '''
                   _servListFloor_light(self, floorID)
        '''
        return self.simBuilding.getACIDsFloor(floorID)

    def _servListRoom_air(self, roomID):
        '''
                   _servListRoom_light(self, roomID)
        '''
        return self.simBuilding.getACIDsRoom(roomID)

    def _servRoomHas_air(self, roomID):
        '''
                    _servRoomHas_air(self, roomID)
        '''
        room=self.simBuilding.getRoom(roomID)
        if room.hasAC():
            return True
        else:
            return False

    def _servNumBuilding_air(self):
        '''          _servNumBuilding_air(self)

        '''
        return self.simBuilding.getNumACs()

    def _servNumFloor_air(self, floorID):
        '''         _servNumFloor_air(self, floorID)

        '''
        return self.simBuilding.getNumACsFloor(floorID)


    def _servNumRoom_air(self, roomID):
        '''         _servNumRoom_air(self, roomID)

        '''
        return self.simBuilding.getNumACsRoom(roomID)

    ##Roller Blinder Services
    def _servEfficiency_blinds(self, blindID):
        '''
                    _servEfficiency_water(self, blindID)
        '''
        blind =self.simBuilding.getBlinder(blindID)
        return blind.getEfficiency()

    def _servExpenditure_blinds(self, blindID):
        '''
                    _servEfficiency_water(self, blindID)
        '''
        blind =self.simBuilding.getBlinder(blindID)
        return blind.getSpeed()

    def _servSize_blinds(self, blindID):
        '''
                    _servSize_light(self, blindID)

        '''
        blind =self.simBuilding.getBlinder(blindID)
        return blind.getSize()

    def _servListBuilding_blinds(self):
        '''
                    _servListBuilding_water(self)
        '''
        return self.simBuilding.getBlinderIDs()

    def _servListFloor_blinds(self, floorID):
        '''
                   _servListFloor_light(self, floorID)
        '''
        return self.simBuilding.getBlinderIDsFloor(floorID)

    def _servListRoom_blinds(self, roomID):
        '''
                   _servListRoom_light(self, roomID)
        '''
        return self.simBuilding.getBlinderIDsRoom(roomID)


    def _servRoomHas_blinds(self, roomID):
        '''         _servRoomHas_blinds(self, roomID)

        '''
        room=self.simBuilding.getRoom(roomID)
        if room.hasBlinds():
            return True
        else:
            return False

    def _servNumBuilding_blinds(self):
        '''         _servNumBuilding_blinds(self)

        '''
        return self.simBuilding.getNumBlinders()

    def _servNumFloor_blinds(self, floorID):
        '''         _servNumFloor_blinds(self, floorID)

        '''
        return self.simBuilding.getNumBlindersFloor(floorID)

    def _servNumRoom_blinds(self, roomID):
        '''         _servNumRoom_blinds(self, roomID)

        '''
        return self.simBuilding.getNumBlindersRoom(roomID)

    ##Heating Services

    def _servEfficiency_heating(self, heaterID):
        '''
                    _servEfficiency_air(self, heaterID)
        '''
        heater =self.simBuilding.getHeater(heaterID)
        return heater.getEfficiency()

    def _servExpenditure_heating(self, heaterID):
        '''
                    _servEfficiency_light(self, heaterID)
        '''
        heater =self.simBuilding.getHeater(heaterID)
        return heater.getWattage()

    def _servSize_heating(self, heaterID):
        '''
                    _servSize_light(self, heaterID)

        '''
        #Air-Condition has no size
        return 0

    def _servListBuilding_heating(self):
        '''
                    _servListBuilding_water(self)
        '''
        return self.simBuilding.getHeaterIDs()

    def _servListFloor_heating(self, floorID):
        '''
                   _servListFloor_light(self, floorID)
        '''
        return self.simBuilding.getHeaterIDsFloor(floorID)

    def _servListRoom_heating(self, roomID):
        '''
                   _servListRoom_light(self, roomID)
        '''
        return self.simBuilding.getHeaterIDsRoom(roomID)

    def _servRoomHas_heating(self, roomID):
        '''         _servRoomHas_heating(self, roomID)

        '''
        room=self.simBuilding.getRoom(roomID)
        if room.hasHeaters():
            return True
        else:
            return False

    def _servNumBuilding_heating(self):
        '''         _servNumBuilding_heating(self)

        '''
        return self.simBuilding.getNumHeaters()

    def _servNumFloor_heating(self, floorID):
        '''         _servNumFloor_heating(self, floorID)

        '''
        return self.simBuilding.getNumHeatersFloor(floorID)

    def _servNumRoom_heating(self, roomID):
        '''         _servNumRoom_heating(self, roomID)

        '''
        return self.simBuilding.getNumHeatersRoom(roomID)

if __name__ == '__main__':
    print 'SubClass: ', issubclass(DummyBif, bif.BifBase)
    print 'Instance: ', isinstance(DummyBif(), bif.BifBase)
