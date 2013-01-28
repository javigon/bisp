'''
Room - Architectural representation of a Floor

Created on Jan 16, 2013

@author: Javier Gonzalez
'''

class Floor():

    def __init__(self, floorID):
        self.floorID = floorID
        self.rooms = []

    def addRoom(self, room):
        self.rooms.append(room)

    def getRooms(self):
        return self.rooms

    def getInContextRepresentation(self):
        r = dict()
        r['ID'] = self.getLogicalID()
        r['numRooms'] = self.getRooms().count()
        return r

    def getLogicalID(self):
        return 'floor[' + self.floorID + ']'