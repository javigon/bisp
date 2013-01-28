'''
Water Access Point - Representation of a waterAP

Created on Jan 18, 2013

@author: Javier Gonzalez
'''
import service

class WaterAP(service.Service):

    def __init__(self,waterAPID):
        #Parent __init__
        super(WaterAP, self).__init__()
        
        self.waterAPID = waterAPID

        self.flow = 0

    def setFlow(self, flow):
        self.flow = flow

    def getFlow(self):
        return self.flow

    def getWaterAPID(self):
        return self.waterAPID

    def getInContextRepresentation(self):
        r = dict()
        r['ID'] = self.getLogicalID()
        r['flow'] = self.getFlow()
        r['input'] = [['flow','Maximum amount of water per unit of time'],['efficiency','Performance of a water access point'], ['gain', 'Scale (0-1) in which a water access point operates']]
        r['output'] = [['production', 'Amount of water liberated by a water access point'],['state', 'On/Off'],['gain', 'Scale (0-1) in which a water access point operates']]
        return r

    def getLogicalID(self):
        return 'room-' + str(self.getRoomID()) + '-waterap-' + str(self.getWaterAPID())