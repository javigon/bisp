'''
Test Class for dummyDB

Created on Jan 16, 2013

@author: Javier Gonzalez

'''

from sys import *

path.append("..")
from dummy import dummy
        
if __name__ == '__main__':
    testCase = dummy.DummyBif(0)

    
    print(testCase.getNumRoomPairs())
    print(testCase.getRoomPairList())
    print(testCase.getRoomList())
    print(testCase.getBuildingServ('heating'))
    print(testCase.getRoomServ('heating',5))
    print(testCase.getFloorServ('heating',0))