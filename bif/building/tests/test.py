'''
Test Class for dummyDB

'''

from bif.impl import dummy
import unittest

class TestBif(unittest.TestCase):
    ''' 
        Test class for the bif interface. This test is independet from the bif implementation
        
        CurrentBifImpl = Dummy
    '''
    testCase = dummy.DummyBif()
    
    def testNumBuildLights(self):
        self.assertEqual(self.testCase.getNumBuildLights(1),200)
        self.assertEqual(self.testCase.getNumBuildLights(0),100)

    def testNumFloorLights(self):
        self.assertEqual(self.testCase.getNumFloorLights(0, 1), 33)
        self.assertEqual(self.testCase.getNumFloorLights(0, 2), 34)
        self.assertEqual(self.testCase.getNumFloorLights(1, 0), 60)
        self.assertEqual(self.testCase.getNumFloorLights(1, 3), 20)
        
    def testNumRoomLights(self):
        self.assertEqual(self.testCase.getNumRoomLights(0, 8), 10)
        self.assertEqual(self.testCase.getNumRoomLights(1, 4), 15)
        self.assertEqual(self.testCase.getNumRoomLights(1, 12), 10)
    
    def testLumLights(self):
        self.assertEqual(self.testCase.getLumLight(200), 60)
        
    def testConsLights(self):
        self.assertEqual(self.testCase.getConsLight(15), 60)
        self.assertEqual(self.testCase.getConsLight(150), 80) 
        self.assertEqual(self.testCase.getConsLight(250), 100)
        self.assertEqual(self.testCase.getConsLight(299), 100) 
       
    def testPosLights(self):
        self.assertEqual(self.testCase.getPosLight(0), [1,2])
        self.assertEqual(self.testCase.getPosLight(145), [146,147])
        self.assertEqual(self.testCase.getPosLight(299), [300,301])

'''
bad testing
class TestClass:
    
    myDummy = dummy.dummyBif()
        
    s = 'Number of lights in building 1: ' + repr(myDummy.getNumBuildLights(1))
    print(s)
        
    s = 'Number of lights in building 0, floor 2: ' + repr(myDummy.getNumFloorLights(0,2))
    print(s)

    s = 'Number of lights in building 1, room 13: ' + repr(myDummy.getNumRoomLights(1,13))
    print(s)
    
    s = 'Light 268: ' + repr(myDummy.getLumLight(268))
    print(s)

    s = 'Consumption of light 268: ' + repr(myDummy.getConsLight(268))
    print(s)
    
    s = 'Position Light 268: ' + repr(myDummy.getPosLight(268))
    print(s)
'''
        
if __name__ == '__main__':
    unittest.main()