'''
Created on Dec 14, 2012

Implements a manager of building instances. Whenever we wish to access information about
a building, we consult the manager, to get an reference to an object that allow us to
query the building.

A user may use available_buildings() to retrieve a list of buildings available and then
retrieve the building instance using lookup(buildingId)

@author: Matias Bjorling
'''

from repo.models import Building
from webconf.settings import BUILDING_REPRESENTATION_DEBUG, BUILDING_REPRESENTATION_IFC,\
    BUILDING_REPRESENTATION_REVIT

import sys
import traceback
from building import BlueprintHandler, Blueprint
from multiprocessing.queues import Queue
from multiprocessing.process import Process
import time
from datetime import datetime

def _Manager__init_simulator(building, queue):
    try:
        blueprint = Blueprint.BluePrint(yearlimit=20, building=building)
        
        def getstarttime():
          now = datetime.now()
          origin = datetime(now.year, 1, 1, 0,0,0)
          td = now - origin
          return td.total_seconds()
        starttime = getstarttime()
        blueprint.construct(starttime)
        
        bh = BlueprintHandler.BlueprintHandler(blueprint, True)
        bh.start(queue)
        
        while 1:
            time.sleep(10000)
            
    except:
        print "Unexpected error:", sys.exc_info()[:2]
        traceback.print_tb(sys.exc_info()[2])

class _Manager(object):

    binstances = dict()
    
    comm_queues = dict()
    
    def __call__(self):
        return self
    
    @classmethod
    def initialize_all(self):
        print 'wee'
        for b in self.get_available_buildings():
            self.lookup(b.bid)

    @classmethod
    def lookup(self, buildingID):
        from building.dummy import dummy
        '''
        @buildingID: int
        '''
        building = Building.objects.get(bid=buildingID)
        print building

        if building is None:
            return None

        if self.binstances.has_key(buildingID) is False:
            ins = None
            if building.bri == BUILDING_REPRESENTATION_DEBUG:
                ins = dummy.DummyBif(buildingID)
            elif building.bri == BUILDING_REPRESENTATION_IFC:
                raise NotImplementedError, 'Missing implementation of IFC plugin'
            elif building.bri == BUILDING_REPRESENTATION_REVIT:
                raise NotImplementedError, 'Missing implementation of Revit plugin'

            # Fire up the simulator for the building if necessary.
            self.comm_queues[buildingID] = Queue()
            p = Process(target=_Manager__init_simulator, args=(ins, self.comm_queues[buildingID]))
            p.start()

            self.binstances[buildingID] = ins

        return self.binstances[buildingID]

    @classmethod
    def get_available_buildings(self):
        return Building.objects.filter(active=True)
    
    @classmethod
    def set_building_service(self, buildingID, serviceID, value):
        if self.comm_queues[buildingID] is None:
            #FIX Insert error message into log.
            return
        
        self.comm_queues[buildingID].put([serviceID, value])
    
# Initialize the manager
Manager = _Manager()
