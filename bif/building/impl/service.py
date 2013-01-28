'''
Service - Abstract representation of a service

Created on Jan 18, 2013

@author: Javier Gonzalez
'''

import abc

class Service(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.roomID = 0

        #Initialized
        self. wattage = 60.0 #Watts
        self.efficiency = 0


        #Produced - Initialized to 0, False or Null. They are retrieved from the simulator
        self.gain = 0
        self.production = 0 #How much X a service produces
        self.state = False  #On=True, Off=False
    
    def setRoom(self, roomID):
        self.roomID = roomID    

    def setProduction(self, production):
        self.production = production
        
    def setGain(self, gain):
        self.gain = gain
    
    def setState(self, state):
        self.state = state

    def setEfficiency(self, efficiency):
        self.efficiency = efficiency

    def setWattage(self, wattage):
        self.wattage = wattage
        
    def getProduction(self):
        return self.production

    def getGain(self):
        return self.gain

    def getState(self):
        return self.state
    
    def getEfficiency(self):
        return self.efficiency

    def getWattage(self):
        return self.wattage

    def getRoomID(self):
        return self.roomID

    
    @abc.abstractmethod
    def getInContextRepresentation(self):
        return
    
    @abc.abstractmethod
    def getLogicalID(self):
        return