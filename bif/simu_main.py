#!/usr/bin/env python
import sys
import time
sys.path.append("../sim")

from bif.BlueprintBuilder import BlueprintBuilder
from bif.BlueprintHandler import BlueprintHandler

if __name__ == '__main__':
	bb = BlueprintBuilder(0)
	bb.build()
	building = bb.building
	bh = BlueprintHandler(building, True)
	#bh.loop(0.1, 1)
	bh.start()
	time.sleep(10)
	bh.stop()
