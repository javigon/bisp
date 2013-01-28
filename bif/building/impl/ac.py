'''
Air Condition - Representation of an air-condition system

Created on Jan 18, 2013

@author: Javier Gonzalez
'''
import service

class AC(service.Service):

    def __init__(self,acID):
        #Parent __init__
        super(AC, self).__init__()
        
        self.acID = acID

    def getAcID(self):
        return self.acID

    def getInContextRepresentation(self):
        r = dict()
        r['ID'] = self.getLogicalID()
        r['wattage'] = self.getWattage()
        r['input'] = [['wattage','Electric power of an ac measured in Watts'],['efficiency','Performance of an ac'], ['gain', 'Scale (0-1) in which an ac operates']]
        r['output'] = [['production', 'Amount of heating produced by an ac'],['state', 'On/Off'],['gain', 'Scale (0-1) in which an ac operates']]
        return r

    def getLogicalID(self):
        return 'room-' + str(self.getRoomID()) + '-ac-' + str(self.getAcID())