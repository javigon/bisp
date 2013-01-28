'''
Heater - Representation of a Heater

Created on Jan 18, 2013

@author: Javier Gonzalez
'''

import service

class Heater(service.Service):

    def __init__(self,heaterID):
        #Parent __init__
        super(Heater, self).__init__()
        
        self.heaterID = heaterID

    def getHeaterID(self):
        return self.heaterID

    def getInContextRepresentation(self):
        r = dict()
        r['ID'] = self.getLogicalID()
        r['wattage'] = self.getWattage()
        r['input'] = dict()
        r['input'] = {'wattage': 'Electric power of a heater measured in Watts', 'efficiency': 'Performance of a heater', 'gain': 'Scale (0-1) in which a heater operates'}
        r['output'] = {'production': 'Amount of heating produced by a heater', 'state': 'On/Off', 'gain': 'Scale (0-1) in which a heater operates'}
        return r

    def getLogicalID(self):
        return 'room-' + str(self.getRoomID()) + '-heater-' + str(self.getHeaterID())