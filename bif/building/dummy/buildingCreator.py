'''
Building Creator

Created on Jan 23, 2013

@author: Javier Gonzalez
'''
from building.impl import room
from building.impl import lamp
from building.impl import blinder
from building.impl import heater
from building.impl import ac
from building.impl import waterAP

class buildingCreator():
    
    def __init__(self, simbuilding):
        self.simBuilding = simbuilding
        
        #Create building
        self._createBuilding(self.simBuilding)
    
    def _createBuilding(self, simBuilding):
        #Definitions
        NFLOORS=3
        rooms=[]
        nRooms=0

        #Lamps - Each room has 2 lamps, except for the hall, which has 10 lamps.
        #2lamps*6rooms*3floors = 36lamps
        #5lamps*1halls*3floors = 15lamps
        #Total Lamps= 51Lamps (0-50)
        nLamps=0
        nBlinds=0
        nHeaters=0
        nACs=0
        nWaterAPs=0

        lamps=[]
        blinds=[]
        heaters=[]
        acs=[]
        waterAPs=[]

        #Add 3 floors to the building. We assume that
        simBuilding.addFloor(0)
        simBuilding.addFloor(1)
        simBuilding.addFloor(2)

        ###
        #### Floor0: 5 rooms (0-4) + 1 bathroom(5) + 1 Hall ###
        ###

        #    ------------------------------------------------------------
        #    |    Room5    |         Room4        |           Room3      |
        #    | --------------------------------------------------        |
        #    |                                                   |       |
        #    |                       Room6                       |-------|
        #    |                                                   |       |
        #    | --------------------------------------------------        |
        #    |    Room0    |         Room1        |           Room2      |
        #    ------------------------------------------------------------
        #
        #    Note: The three floors look the same and follow the same enumerating pattern

        ##Create Services


        for floorID in range (NFLOORS):

            ##Rooms - Room0+(7*j) to Room4+(7*j)
            for i in range (5):
                newRoom=room.Room(nRooms, floorID)
                #Room attributes

                #lamps - 2 lamps per room
                #Blinds - 2 blinds per room
                for j in range (2):
                    myLamp = lamp.Lamp(nLamps)
                    lamps.append(myLamp)
                    newRoom.addLight(myLamp)
                    nLamps+=1

                    myBlind = blinder.Blind(nBlinds)
                    blinds.append(myBlind)
                    newRoom.addBlinder(myBlind)
                    nBlinds+=1

                #Air Condition - 1 per room
                myAc = ac.AC(nACs)
                acs.append(myAc)
                newRoom.addAc(myAc)
                nACs+=1

                #Heater - 1 per room
                myHeater = heater.Heater(nHeaters)
                heaters.append(myHeater)
                newRoom.addHeater(myHeater)
                nHeaters+=1

                #Add a new Room
                rooms.append(newRoom)
                nRooms+=1




            ##BathRoom - Room5+(7*j)
            newRoom=room.Room(nRooms, floorID)

            #lamps
            for j in range(2):
                myLamp = lamp.Lamp(nLamps)
                lamps.append(myLamp)
                newRoom.addLight(myLamp)
                nLamps+=1

            #Heater - 1 in the bathroom
            #myHeater = heater.Heater(nHeaters)
            #heaters.append(myHeater)
            #newRoom.addHeater(myHeater)
            #nHeaters+=1

            #WaterAP - 1 in the bathroom
            myWaterAP = waterAP.WaterAP(nWaterAPs)
            waterAPs.append(myWaterAP)
            newRoom.addWaterAP(myWaterAP)
            nWaterAPs+=1

            #Add a new room (bathroom)
            rooms.append(newRoom)
            nRooms+=1


            #Hall - Room6+(7*j)
            newRoom=room.Room(nRooms, floorID)

            for i in range(5):      #Halls have 5 lights
                #newRoom.addLight()
                #lamps
                myLamp = lamp.Lamp(nLamps)
                lamps.append(myLamp)
                newRoom.addLight(myLamp)
                nLamps+=1

            #Halls have 2 Heaters
            for i in range(2):
                myHeater = heater.Heater(nHeaters)
                heaters.append(myHeater)
                newRoom.addHeater(myHeater)
                nHeaters+=1

            #Halls have 2 Air-Condition machines
            for i in range(2):
                myAc = ac.AC(nACs)
                acs.append(myAc)
                newRoom.addAc(myAc)
                nACs+=1

            #Add new room (Hall)
            rooms.append(newRoom)
            nRooms+=1

            #We add rooms[] to Floor0
            simBuilding.addRoomsToFloor(rooms, floorID)


            ##We define which rooms are neighbors
            #For Room0+(7*j)  to Room5+(7*j)
            for i in range(0,5):
                simBuilding.setAdjacentRooms(rooms[i].roomID, rooms[i+1].roomID)

            #All Rooms with Room6+(7*j)
            for i in range(0,6):
                simBuilding.setAdjacentRooms(rooms[i].roomID, rooms[6].roomID)

            rooms=[]

        #We add inter-floor neighbors
        for i in range(7,21):
            simBuilding.setAdjacentRooms(i, i-7)
