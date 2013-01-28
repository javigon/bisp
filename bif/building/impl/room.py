'''
Room - Architectural representation of a Room

Created on Jan 16, 2013

@author: Javier Gonzalez
'''

class Room():

    def __init__(self, roomID, floorID):
        ##Architecture
        self.roomID = roomID
        self.floorID = floorID

        ##Services
        self.lights=[]
        self.waterAPs=[]
        self.acs=[]
        self.blinders=[]
        self.heaters=[]

    '''
        ##############################################
        Public Methods
        ##############################################
    '''

    def getID(self):
        return self.roomID

    def getFloor(self):
        return self.floorID

    def addLight(self, light):
        light.setRoom(self.roomID)
        self.lights.append(light)

    def addWaterAP(self, water):
        water.setRoom(self.roomID)
        self.waterAPs.append(water)

    def addAc(self, ac):
        ac.setRoom(self.roomID)
        self.acs.append(ac)

    def addBlinder(self, blind):
        blind.setRoom(self.roomID)
        self.blinders.append(blind)

    def addHeater(self, heater):
        heater.setRoom(self.roomID)
        self.heaters.append(heater)

    def getLights(self):
        return self.lights

    def getNumLights(self):
        return len(self.lights)

    def getWaterAPs(self):
        return self.waterAPs

    def getNumWaterAPs(self):
        return len(self.waterAPs)

    def getAcs(self):
        return self.acs

    def getNumAcs(self):
        return len(self.acs)

    def getBlinders(self):
        return self.blinders

    def getNumBlinders(self):
        return len(self.blinders)

    def getHeaters(self):
        return self.heaters

    def getNumHeaters(self):
        return len(self.heaters)

    def hasLights(self):
        return len(self.lights) > 0

    def hasWater(self):
        return len(self.waterAPs) > 0

    def hasAC(self):
        return len(self.acs) > 0

    def hasBlinds(self):
        return len(self.blinders) > 0

    def hasHeaters(self):
        return len(self.heaters) > 0

    def getInContextRepresentation(self):
        r = dict()
        r['ID'] = self.getLogicalID()
        r['numLights'] = self.getNumLights()
        r['numWater'] = self.getNumWaterAPs()
        r['numAC'] = self.getNumAcs()
        r['numBlinds'] = self.getNumBlinders()
        r['numHeaters'] = self.getNumHeaters()
        return r

    def getFullRepresentation(self):

        lamps = dict()
        heater = dict()
        water = dict()
        ac = dict()
        blind = dict()

        roomDef = self.getInContextRepresentation()

        for l in self.getLights():
            lamps[l.getLogicalID()] = l.getInContextRepresentation()

        roomDef['lights'] = lamps

        for h in self.getHeaters():
            heater['heater'] = h.getInContextRepresentation()

        roomDef['heaters'] = heater

        for w in self.getWaterAPs():
            water['water'] = w.getInContextRepresentation()

        roomDef['waters'] = water

        for a in self.getAcs():
            ac['ac'] = a.getInContextRepresentation()

        roomDef['acs'] = ac

        for b in self.getBlinders():
            blind['blind'] = b.getInContextRepresentation()

        roomDef['blinds'] = blind

        return roomDef

    def getLogicalID(self):
        return 'floor-' + str(self.getFloor()) + '-room-' + str(self.roomID) + ''
