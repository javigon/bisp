'''
Windows/Blinders - Representation of a Blind

Created on Jan 18, 2013

@author: Javier Gonzalez
'''
import service

class Blind(service.Service):

    def __init__(self,blindsID):
        #Parent __init__
        super(Blind, self).__init__()
        
        self.blindsID = blindsID

        self.speed = 0
        self.size = 5
        self.setpoint = 0

    def setSpeed(self, speed):
        self.speed = speed

    def setSize(self, size):
        self.size = size
        
    def setSetPoint(self, setpoint):
        self.setpoint = setpoint
        
    def getSpeed(self):
        return self.speed
        
    def getSize(self):
        return self.size
    
    def getSetPoint(self):
        return self.setpoint

    def getBlindID(self):
        return self.blindsID

    def getInContextRepresentation(self):
        r = dict()
        r['ID'] = self.getLogicalID()
        r['size'] = self.getSize()
        r['speed'] = self.getSpeed()
        r['input'] = [['setpoint','Requested state of the blind. Scale [0,1]'], ['size','Window/Blinder size'], ['speed','Speed at which the window can go up and down']]
        r['output'] = [['state', 'Continuous value between Up and Down. Scale [0,1]'],['setpoint', 'Requested state of the blind. Scale [0,1]']]
        return r

    def getLogicalID(self):
        return 'room-' + str(self.getRoomID()) + '-blind-' + str(self.getBlindID())