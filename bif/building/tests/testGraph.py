import networkx as nx
from bif.impl import room
from bif.impl import floor
from bif.impl import building

def _createBuilding(myBuilding):
        #Definitions
        rooms=[]
        nRooms=0
        
        #Add 3 floors to the building. We assume that 
        myBuilding.addFloor(0)
        myBuilding.addFloor(1)
        myBuilding.addFloor(2)
        
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

        for j in range (3):
            
            #Rooms - Room0 to Room4
            for i in range (5):
                newRoom=room.Room(nRooms)
                #Room attributes
                newRoom.addLight()
                newRoom.addBlinder()
                newRoom.addBlinder()    #2 Blinders per rooms
                newRoom.addAc()
                rooms.append(newRoom)
                nRooms+=1
            
            #BathRoom - Room5
            newRoom=room.Room(nRooms)
            newRoom.addLight()
            newRoom.addAc()
            newRoom.addWaterAP()
            rooms.append(newRoom)
            nRooms+=1
            
            #Hall - Room6
            newRoom=room.Room(nRooms)
            for i in range(5):      #Halls have 5 lights
                newRoom.addLight()
            newRoom.addAc()
            rooms.append(newRoom)
            nRooms+=1
            
        
            myBuilding.addRoomsToFloor(rooms, j)
         
            ##We define which rooms are neighbors 
            #For Room0 to Room5
            for i in range(0,5):
                myBuilding.setAdjacentRooms(rooms[i].roomID, rooms[i+1].roomID)
                
            #All Rooms in Floor0 with Room6
            for i in range(0,6):
                myBuilding.setAdjacentRooms(rooms[i].roomID, rooms[6].roomID)
     
            rooms=[]

        
        
        
        #myBuilding.printRooms()
        #myBuilding._printNodes()
        #For Room7 to Room12
        #for i in range(7,12):
            #myBuilding.setAdjacentRooms(rooms[i].roomID, rooms[i+1].roomID)
            
        #All Rooms in Floor1 with Room6
        #for i in range(7,13):
            #myBuilding.setAdjacentRooms(rooms[i].roomID, rooms[13].roomID)
       
       
       
        #TEST: Retrieving Edges and giving nodes in the edge
        myRoomNodes=[]
        myRoomNodeIDs=[]
        
        #myBuilding._printEdges()
        myEdges=myBuilding.getRoomPairs()
        #print((myEdges[0][1]).getID())
        for i in range (len(myEdges)):
            myRoomNodeIDs.append([(myEdges[i][0]).getID(),(myEdges[i][1]).getID()])
        
        print(myRoomNodeIDs)
        #print(myRoomNodes)
        #print(myRoomNodes[0][0].getID())
        
        #TEST: Retrieving Rooms and giving IDs
        myRoomIDs=[]        
        myRooms=myBuilding.getRooms() 
        for i in range (len(myRooms)):
            myRoomIDs.append(myRooms[i].getID())
            
        print(myRoomIDs)
                
                
        ###TESTING ROOM GRAPH###
        #myBuilding._printNodes()
        #myBuilding._printEdges()
        myBuilding._printNumNodes()
        myBuilding._printNumEdges()
        #myBuilding._printNeibors(rooms[6])
        #print(myBuilding.getAdjacentRooms(rooms[6]))

simBuilding = building.Building()
_createBuilding(simBuilding)

