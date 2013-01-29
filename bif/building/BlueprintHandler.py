import time
import sys
import traceback

from apscheduler.scheduler import Scheduler
from apscheduler.jobstores.ram_store import RAMJobStore
from numpy.distutils import environment
from django.utils.datetime_safe import datetime
from django.utils.timezone import utc
from repo.models import Measurement
import exceptions

class BlueprintHandler:
    setter_blacklist = []
    getter_blacklist = []
    
    def __init__ (self, blueprint, testing=False, testing_count=10):
        self.blueprint = blueprint
        self.testing = testing
        self.testing_count = testing_count
        self.scheduler = Scheduler()

    def do_step(self):
        print 'stepping'
        try:
            # Fetch any outstanding events from the engine process and execute in simulator
            while not self.local_queue.empty():
                action = self.local_queue.get()
                try:
                    self.blueprint.interface.set(action[0], float(action[1]))
                    print 'Received action:', action
                except exceptions.ValueError:
                    print "Value '"+str(action[1])+"' is not convertable to float"
            
            points = self.blueprint.interface.get_getters()
    
            self.blueprint.step(stepcount=int(1/.1))
    
            g = {}
            for point in points:
                if point in BlueprintHandler.getter_blacklist:
                    continue
                g[point] = self.blueprint.interface.get(point)

        
            for k in g.keys():
                m = Measurement()
                m.bid = self.blueprint.building.buildingID
                m.timestamp = datetime.utcnow().replace(tzinfo=utc)
                m.uuid = k
                m.val = g[k]
                m.save()
        except:
            #print 'error: ', sys.exc_info()
            print 'trace: ', traceback.print_exc()

    def init_scheduler(self):
        schedule_store = RAMJobStore()

        # Write data every 15 seconds.
        job_second = self.scheduler.add_interval_job(self.do_step, 0, 0, 0, 0, 15)

        schedule_store.add_job(job_second)

        self.scheduler.add_jobstore(schedule_store, 'Simulator scheduler', quiet = False)

    def start (self, queue=None):
        self.local_queue = queue
        self.init_scheduler()
        self.scheduler.start()

    def stop (self):
        self.scheduler.shutdown()

