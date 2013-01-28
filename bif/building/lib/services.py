'''
    services - Enum of services in a building
    
    Created on Dec 8, 2012
    
    @author: Matias Bjorling, Javier Gonzalez, Aslak Johansen
'''
from building.lib import enum

class Services(enum.Enum):
    "Services available in a building"

    def __init__(self, enumVars=[]):
        if enumVars != None:
            enum.Enum.__init__(self, enumVars)
        else:
            pass
        
    def addService(self, enumVars=[]):
        enum.Enum.incr(self, enumVars)
