'''
Light - Representation of a lamp

Created on Jan 18, 2013

@author: Javier Gonzalez
'''
import service

class Lamp(service.Service):

    def __init__(self,lampID):
        #Parent __init__
        super(Lamp, self).__init__()

        self.lampID = lampID
    def getLampID(self):
        return self.lampID

    def setLuminosity(self, luminosity):
        self.luminosity = luminosity

    def getLuminosity(self):
        return self.luminosity

    def getInContextRepresentation(self):
        r = dict()
        r['ID'] = self.getLogicalID()
        r['wattage'] = self.getWattage()
        r['input'] =  {'wattage': 'Electric power of a lamp measured in Watts','efficiency': 'Performance of a lamp', 'luminosity': 'Maximum amount of luminosity that a lamp can produce','gain': 'Scale (0-1) in which a lamp operates'}
        r['output'] = {'production': 'Amount of luminosity produced by a lamp', 'state': 'On/Off','gain': 'Scale (0-1) in which a lamp operates'}
        return r

    def getLogicalID(self):
        #return str('L' + str(self.getLampID()))
        return 'room-' + str(self.getRoomID()) + '-light-' + str(self.getLampID())
