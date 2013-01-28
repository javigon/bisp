'''
Test Class for dummyDB

'''

from building.dummy import dummy
import unittest

class TestBif(unittest.TestCase):
    ''' 
        Test class for the bif interface. This test is independent from the bif implementation
        
        CurrentBifImpl = Dummy
    '''
    testCase = dummy.DummyBif(0)
    
    '''
        #######################################
        Test Building Architecture
        #######################################
    '''
    
    def testRooms(self):
        self.assertEqual(self.testCase.getNumFloors(),3)
        self.assertEqual(self.testCase.getNumRooms(),21)
        self.assertEqual(self.testCase.getRoomFloor(0),0)
        self.assertEqual(self.testCase.getRoomFloor(6),0)
        self.assertEqual(self.testCase.getRoomFloor(12),1)
        self.assertEqual(self.testCase.getRoomFloor(14),2)
        self.assertEqual(self.testCase.getRoomFloor(20),2)
        self.assertEqual(self.testCase.getAdjacentRooms(5),[4,6,12])
        self.assertEqual(self.testCase.getAdjacentRooms(6),[0,1,2,3,4,5,13])
        self.assertEqual(self.testCase.getAdjacentRooms(11),[4,10,12,13,18])
        self.assertEqual(self.testCase.getAdjacentRooms(13),[6,7,8,9,10,11,12,20])
    
    '''
        #######################################
        Test Lightning Services
        #######################################
    '''  
        
    ##Test implemented methods inherited from abstract class
    
    def testRoomLightExistance(self):
        self.assertEqual(self.testCase.getRoomHasServ('light',2), True)
    def testNumBuildLights(self):
        self.assertEqual(self.testCase.getNumBuildingServ('light'),51)

    def testNumFloorLights(self):
        self.assertEqual(self.testCase.getNumFloorServ('light', 2),17)
        self.assertEqual(self.testCase.getNumFloorServ('light', 1),17)
        
    def testNumRoomLights(self):
        self.assertEqual(self.testCase.getNumRoomServ('light', 0),2)
        self.assertEqual(self.testCase.getNumRoomServ('light', 20),5)
        self.assertEqual(self.testCase.getNumRoomServ('light', 2),2)
        self.assertEqual(self.testCase.getNumRoomServ('light', 6),5)
    
    def testLightPropierties(self):
        self.assertEqual(self.testCase.getEfficiencyServ('light',3),0)
        self.assertEqual(self.testCase.getExpenditureServ('light',3),60.0)

    '''
        #######################################
        Test Watering Services
        #######################################
    ''' 
    ##Test implemented methods inherited from abstract class
    
    def testRoomWaterExistance(self):
        self.assertEqual(self.testCase.getRoomHasServ('water', 0), False)
        self.assertEqual(self.testCase.getRoomHasServ('water', 5), True)
    
    def testNumBuildWaterps(self):
        self.assertEqual(self.testCase.getNumBuildingServ('water'),3)

    def testNumFloorWaterps(self):
        self.assertEqual(self.testCase.getNumFloorServ('water', 2),1)

        
    def testNumRoomWaterps(self):
        self.assertEqual(self.testCase.getNumRoomServ('water', 0),0)
        self.assertEqual(self.testCase.getNumRoomServ('water', 2),0)
        self.assertEqual(self.testCase.getNumRoomServ('water', 5),1)

    def testWaterPropierties(self):
        self.assertEqual(self.testCase.getEfficiencyServ('water',2),0)
        self.assertEqual(self.testCase.getExpenditureServ('water',0),0)

    '''
        #######################################
        Test Air Condition Services
        #######################################
    '''
    
    ##Test implemented methods inherited from abstract class
    
     
    def testACExistance(self):
        self.assertEqual(self.testCase.getRoomHasServ('air', 0), True)
        self.assertEqual(self.testCase.getRoomHasServ('air', 18), True)
        self.assertEqual(self.testCase.getRoomHasServ('air', 5), False)
    
    def testNumBuildAC(self):
        self.assertEqual(self.testCase.getNumBuildingServ('air'),21)
        self.assertEqual(self.testCase.getNumFloorServ('air', 0),7)
        self.assertEqual(self.testCase.getNumRoomServ('air', 0),1)
        self.assertEqual(self.testCase.getNumRoomServ('air', 12),0)
        self.assertEqual(self.testCase.getNumRoomServ('air', 13),2)
      
    def testACPropierties(self):
        self.assertEqual(self.testCase.getEfficiencyServ('air',2),0)
        self.assertEqual(self.testCase.getExpenditureServ('air',0),60.0)
    

    '''
        #######################################
        Test Blinder Services
        #######################################
    '''
    ##Test implemented methods inherited from abstract class
      
    def testBlindsExistance(self):
        self.assertEqual(self.testCase.getRoomHasServ('blinds', 0), True)
        self.assertEqual(self.testCase.getRoomHasServ('blinds', 18), True)
        self.assertEqual(self.testCase.getRoomHasServ('blinds', 5), False)
        self.assertEqual(self.testCase.getRoomHasServ('blinds', 13), False)
    
    def testNumBuildBlinds(self):
        self.assertEqual(self.testCase.getNumBuildingServ('blinds'),30)
        self.assertEqual(self.testCase.getNumFloorServ('blinds', 0),10)
        self.assertEqual(self.testCase.getNumRoomServ('blinds', 0),2)
        self.assertEqual(self.testCase.getNumRoomServ('blinds', 12),0)
        self.assertEqual(self.testCase.getNumRoomServ('blinds', 13),0)

    def testBlinderPropierties(self):
        self.assertEqual(self.testCase.getEfficiencyServ('blinds',2),0)
        self.assertEqual(self.testCase.getExpenditureServ('blinds',0),0)
    

    '''
        #######################################
        Test Air Heating Services
        #######################################
    '''
    ##Test implemented methods inherited from abstract class
    
    def testHeatingExistance(self):
        self.assertEqual(self.testCase.getRoomHasServ('heating', 0), True)
        self.assertEqual(self.testCase.getRoomHasServ('heating', 18), True)
        self.assertEqual(self.testCase.getRoomHasServ('heating', 5), False)

    def testNumBuildHeating(self):
        self.assertEqual(self.testCase.getNumBuildingServ('heating'),21)
        self.assertEqual(self.testCase.getNumFloorServ('heating', 0),7)
        self.assertEqual(self.testCase.getNumRoomServ('heating', 0),1)
        self.assertEqual(self.testCase.getNumRoomServ('heating', 12),0)
        self.assertEqual(self.testCase.getNumRoomServ('heating', 13),2)
        self.assertEqual(self.testCase.getNumRoomServ('heating', 6),2)
        self.assertEqual(self.testCase.getNumRoomServ('heating', 4),1)

    def testHeaterPropierties(self):
        self.assertEqual(self.testCase.getEfficiencyServ('heating',2),0)
        self.assertEqual(self.testCase.getExpenditureServ('heating',0),60.0)


    ##No dummy implementation-specific methods to be tested
if __name__ == '__main__':
    unittest.main()

    #testCase = dummy2.DummyBif(0)

    #print(testCase.getNumFloors(0))
    #print(testCase.getNumRooms(0))
    #print(testCase.getNumLights(0))


    
    #print(testCase.getNumRoomPairs(0))
    #print(testCase.getRoomPairList(0))
    #print(testCase.getRoomList(0))
    #print(testCase.getBuildingServ('heating'))
    #print(testCase.getRoomServ('heating'5))
    #print(testCase.getFloorServ('heating',0))


