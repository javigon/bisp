# ex:set ts=2:

from random import random, uniform, normalvariate

secsperday = 60*60*24

class OccupancySimple ():
  def __init__ (self, days, count, daycount=secsperday, mu=4, sigma=3, sigmamod=12, somelist=None):
    self.map = [0]*days
    self.daycount = daycount
    self.mu = mu
    self.sigma = sigma
    self.sigmamod = sigmamod
    self.lastday = None
    self.daymap = [0]*secsperday
    self.time = 0
    if somelist != None: somelist.append(self)
    
    for i in range(count):
      index = int(uniform(0,days))
      size = normalvariate(mu, sigma*uniform(0,sigmamod))
      
      for s in range(int(size)):
        self.map[(index+s) % len(self.map)] += 1
  def index (self, time=None):
#    print self
    if time==None: time=self.time
    day    = int(time/(secsperday))
    subday = int(time%(secsperday))
    
    if day != self.lastday:
      self.daymap = [0]*secsperday
#      print dir(self)
#      print self.daycount
      # fill out
      for i in range(self.daycount):
        index = int(normalvariate(secsperday/2, 3600*2))
        size = normalvariate(60, 60)
        
        for s in range(int(size)):
          s -= int(size/2)
          if index+s >=0 and index+s < len(self.daymap):
            self.daymap[index+s] += 1
      
      self.lastday = day
    
    return self.map[day]*10+self.daymap[subday]+random()
  def set_time (self, time):
    self.time = time
  def rerun (self):
    pass
  

