'''
Building - Architectural representation of a Building

Created on Jan 16, 2013

@author: Javier Gonzalez
'''

#from building.impl import room
import room
import floor
#from building.impl import floor
import networkx as nx

'''
We consider the building as a graph where rooms are nodes.

We keep the classic Floor-Room distribution to make it easier
to keep track of where a room is located.
'''
class Building():
    
    '''
        ##############################################
        Public Methods 
        ##############################################
    '''  
    
    def __init__(self, buildingID):
        self.building=buildingID
        self.NumFloors=0
        self.floors=[]
        self.rooms=[]
        #create graph to represent Rooms
        self.buildingG=nx.Graph()

        
    def getBuildingID(self):
        return self.building
        
    def addFloor(self, floorLevel):
        newFloor=floor.Floor(floorLevel)
        self.floors.append(newFloor)
        self.NumFloors+=1
    
    def addRoomsToFloor(self, rooms, floorID):
        for i in range (len(rooms)):
            self.rooms.append(rooms[i])
            self.floors[floorID].addRoom(rooms[i])
            self.buildingG.add_node(rooms[i], roomID=(("Room")+str(i)))
        
            
    def setAdjacentRooms(self, room1ID, room2ID):
        #We create an edge between these two rooms
        self.buildingG.add_edge(self.rooms[room1ID], self.rooms[room2ID], edgeID=(("Room"+str(room1ID)+"-Room")+str(room2ID)))
      
      
    ##Building Service Information
    #Heating
    def getNumHeatersRoom(self, roomID):
        return self.rooms[roomID].getNumHeaters()
        
    def getNumHeatersFloor(self,floorID):    
        rooms=self.floors[floorID].getRooms()
        numHeaters=0
        for i in range (len(rooms)):
            numHeaters+=rooms[i].getNumHeaters()        
        return numHeaters 
       
    def getNumHeaters(self):
        numHeaters=0
        for i in range (len(self.rooms)):
            numHeaters+=self.rooms[i].getNumHeaters()        
        return numHeaters 
    
    def getHeater(self, heaterID):
        roomHeaters=[]
        heaters=[]
        for i in range (len(self.rooms)):
            roomHeaters=self.rooms[i].getHeaters()
            for j in range (len(roomHeaters)):
                heaters.append(roomHeaters[j])
            roomHeaters=[]
        for i in range (len(heaters)): 
            if ((heaters[i]).getHeaterID() == heaterID):
                return heaters[i]

        return -1
    
    def getHeaterIDs(self):
        roomHeaters=[]
        heaters=[]
        for i in range (len(self.rooms)):
            roomHeaters=self.rooms[i].getHeaters()
            for j in range (len(roomHeaters)):
                heaters.append((roomHeaters[j]).getHeaterID())
            roomHeaters=[]
        return heaters
    
    def getHeaterIDsFloor(self, floorID):
        rooms=self.floors[floorID].getRooms()
        roomHeaters=[]
        heaters=[]
        for i in range (len(rooms)):
            roomHeaters=rooms[i].getHeaters() 
            for j in range (len(roomHeaters)):
                heaters.append((roomHeaters[j]).getHeaterID()) 
            roomHeaters=[]
        return heaters      

        
    def getHeaterIDsRoom(self, roomID):
        roomHeaters=self.rooms[roomID].getHeaters()
        heaters=[]
        for j in range (len(roomHeaters)):
                heaters.append((roomHeaters[j]).getHeaterID()) 
        return heaters  
    
    #Blinds
    def getNumBlindersRoom(self, roomID):
        return self.rooms[roomID].getNumBlinders()
        
    def getNumBlindersFloor(self,floorID):    
        rooms=self.floors[floorID].getRooms()
        numBlinders=0
        for i in range (len(rooms)):
            numBlinders+=rooms[i].getNumBlinders()        
        return numBlinders 
       
    def getNumBlinders(self):
        numBlinders=0
        for i in range (len(self.rooms)):
            numBlinders+=self.rooms[i].getNumBlinders()        
        return numBlinders 
    
    def getBlinder(self, blinderID):
        roomBlinders=[]
        blinders=[]
        for i in range (len(self.rooms)):
            roomBlinders=self.rooms[i].getBlinders()
            for j in range (len(roomBlinders)):
                blinders.append(roomBlinders[j])
            roomBlinders=[]
        for i in range (len(blinders)): 
            if ((blinders[i]).getBlindID() == blinderID):
                return blinders[i]

        return -1
    
    def getBlinderIDs(self):
        roomBlinders=[]
        blinders=[]
        for i in range (len(self.rooms)):
            roomBlinders=self.rooms[i].getBlinders()
            for j in range (len(roomBlinders)):
                blinders.append((roomBlinders[j]).getBlindID())
            roomBlinders=[]
        return blinders
    
    def getBlinderIDsFloor(self, floorID):
        rooms=self.floors[floorID].getRooms()
        roomBlinders=[]
        blinders=[]
        for i in range (len(rooms)):
            roomBlinders=rooms[i].getBlinders() 
            for j in range (len(roomBlinders)):
                blinders.append((roomBlinders[j]).getBlindID()) 
            roomBlinders=[]
        return blinders      

        
    def getBlinderIDsRoom(self, roomID):
        roomBlinders=self.rooms[roomID].getBlinders()
        blinders=[]
        for j in range (len(roomBlinders)):
                blinders.append((roomBlinders[j]).getBlindID()) 
        return blinders    
    
    #Air-Condition
    def getNumACsRoom(self, roomID):
        return self.rooms[roomID].getNumAcs()
        
    def getNumACsFloor(self,floorID):    
        rooms=self.floors[floorID].getRooms()
        numACs=0
        for i in range (len(rooms)):
            numACs+=rooms[i].getNumAcs()        
        return numACs 
       
    def getNumACs(self):
        numACs=0
        for i in range (len(self.rooms)):
            numACs+=self.rooms[i].getNumAcs()       
        return numACs 
    
    def getAC(self, ACID):
        roomACs=[]
        acs=[]
        for i in range (len(self.rooms)):
            roomACs=self.rooms[i].getAcs()
            for j in range (len(roomACs)):
                acs.append(roomACs[j])
            roomACs=[]
        for i in range (len(acs)): 
            if ((acs[i]).getAcID() == ACID):
                return acs[i]

        return -1
    
    def getACIDs(self):
        roomACs=[]
        acs=[]
        for i in range (len(self.rooms)):
            roomACs=self.rooms[i].getAcs()
            for j in range (len(roomACs)):
                acs.append((roomACs[j]).getAcID())
            roomACs=[]
        return acs
    
    def getACIDsFloor(self, floorID):
        rooms=self.floors[floorID].getRooms()
        roomACs=[]
        acs=[]
        for i in range (len(rooms)):
            roomACs=rooms[i].getAcs() 
            for j in range (len(roomACs)):
                acs.append((roomACs[j]).getAcID()) 
            roomACs=[]
        return acs      

        
    def getACIDsRoom(self, roomID):
        roomACs=self.rooms[roomID].getAcs()
        acs=[]
        for j in range (len(roomACs)):
                acs.append((roomACs[j]).getAcID()) 
        return acs    
        
    #WaterAPs
    def getNumWaterAPsRoom(self, roomID):
        return self.rooms[roomID].getNumWaterAPs()
        
    def getNumWaterAPsFloor(self,floorID):    
        rooms=self.floors[floorID].getRooms()
        numWaterAPs=0
        for i in range (len(rooms)):
            numWaterAPs+=rooms[i].getNumWaterAPs()        
        return numWaterAPs 
       
    def getNumWaterAPs(self):
        numWaterAPs=0
        for i in range (len(self.rooms)):
            numWaterAPs+=self.rooms[i].getNumWaterAPs()        
        return numWaterAPs
    
    def getWater(self, waterAPID):
        roomWaterAPs=[]
        waterAPs=[]
        for i in range (len(self.rooms)):
            roomWaterAPs=self.rooms[i].getWaterAPs()
            for j in range (len(roomWaterAPs)):
                waterAPs.append(roomWaterAPs[j])
            roomWaterAPs=[]
        for i in range (len(waterAPs)): 
            if ((waterAPs[i]).getWaterAPID() == waterAPID):
                return waterAPs[i]

        return -1
    
    def getWaterIDs(self):
        roomWaterAPs=[]
        waterAPs=[]
        for i in range (len(self.rooms)):
            roomWaterAPs=self.rooms[i].getWaterAPs()
            for j in range (len(roomWaterAPs)):
                waterAPs.append((roomWaterAPs[j]).getWaterAPID())
            roomWaterAPs=[]
        return waterAPs
    
    def getWaterIDsFloor(self, floorID):
        rooms=self.floors[floorID].getRooms()
        roomWaterAPs=[]
        waterAPs=[]
        for i in range (len(rooms)):
            roomWaterAPs=rooms[i].getWaterAPs() 
            for j in range (len(roomWaterAPs)):
                waterAPs.append((roomWaterAPs[j]).getWaterAPID()) 
            roomWaterAPs=[]
        return waterAPs      

        
    def getWaterIDsRoom(self, roomID):
        roomWaterAPs=self.rooms[roomID].getWaterAPs()
        waterAPs=[]
        for j in range (len(roomWaterAPs)):
                waterAPs.append((roomWaterAPs[j]).getWaterAPID()) 
        return waterAPs   
    
    #Lights
    def getLightsRoom(self,roomID):
        return self.rooms[roomID].getLights()
        
    def getNumLightsRoom(self, roomID):
        return self.rooms[roomID].getNumLights()
        
    def getNumLightsFloor(self,floorID):    
        rooms=self.floors[floorID].getRooms()
        numLights=0
        for i in range (len(rooms)):
            numLights+=rooms[i].getNumLights()        
        return numLights 
        
    def getNumLights(self):
        numLights=0
        for i in range (len(self.rooms)):
            numLights+=self.rooms[i].getNumLights()        
        return numLights 
    
    def getLight(self, lightID):
        roomLights=[]
        lights=[]
        for i in range (len(self.rooms)):
            roomLights=self.rooms[i].getLights()
            for j in range (len(roomLights)):
                lights.append(roomLights[j])
            roomLights=[]
        for i in range (len(lights)):
            if ((lights[i]).getLampID() == lightID):
                return lights[i]
        
        return -1
    
    def getLightIDs(self):
        roomLights=[]
        lightIDs=[]
        for i in range (len(self.rooms)):
            roomLights=self.rooms[i].getLights()
            for j in range (len(roomLights)):
                lightIDs.append((roomLights[j]).getLampID())
            roomLights=[]
        return lightIDs
    
    def getLightIDsFloor(self, floorID):
        rooms=self.floors[floorID].getRooms()
        roomLights=[]
        lightIDs=[]
        for i in range (len(rooms)):
            roomLights=rooms[i].getLights() 
            for j in range (len(roomLights)):
                lightIDs.append((roomLights[j]).getLampID()) 
            roomLights=[]
        return lightIDs      

        
    def getLightIDsRoom(self, roomID):
        roomLights=self.rooms[roomID].getLights()
        lightIDs=[]
        for j in range (len(roomLights)):
                lightIDs.append((roomLights[j]).getLampID()) 
        return lightIDs  
    
    ## Building Architectural Information 
    
    def getRoomFloor(self, roomID):
        return self.rooms[roomID].getFloor()
      
    def getRoom(self, roomID):
        return self.rooms[roomID]    
        
    def getAdjacentRooms(self, roomID):
        #Returns a list of the IDs of the adjacent rooms
        room=self.rooms[roomID]
        neighbors=self.buildingG.neighbors(room)
        neighborIDs=[]
        for i in range (len(neighbors)):
            neighborIDs.append(neighbors[i].getID())
        return sorted(neighborIDs, key=int)
    
    def getRoomPairs(self):
        return self.buildingG.edges()
    
    def getRooms(self):
        return self.buildingG.nodes()
    
    def getNumFloors(self):
        return self.NumFloors
    
    def getNumRooms(self):
        return len(self.rooms)
    
    ## Test
    def _printRooms(self):
        print("ROOMS: ")
        for i in range (len(self.rooms)):
            print(self.rooms[i].getID())
            print(self.rooms[i])
    
    '''
        ##############################################
        Private Methods 
        ##############################################
    '''  
        
    def _printNodes(self):
        print("NODES: ")
        print(self.buildingG.nodes(data=True))
        print("\n")   
        
    def _printEdges(self):
        print("EDGES: ")
        print(self.buildingG.edges(data=True))  
        print("\n")
    
    def _printNumNodes(self):
        print("Number of nodes: ")
        print(self.buildingG.number_of_nodes())
        print("\n")
    
    def _printNumEdges(self):
        print("Number of edges: ")
        print(self.buildingG.number_of_edges())
        print("\n")    
        
    def _printNeibors(self, node):
        print("Neighbors of: "+str(node))
        print(self.buildingG.neighbors(node))
        print("\n")