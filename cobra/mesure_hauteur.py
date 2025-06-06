import math
from centrale_inirtielle import mesure_angles
from tf_luna import mesure_distance
from XY import xy
import time


while 1:
    x,y,z = xy()
    tangage, roulis, lacet = mesure_angles()
    d = mesure_distance()
    h = d*math.cos(tangage*math.pi/180)*math.cos(roulis*math.pi/180)

    print(x,y,h, "tangage",tangage,"roulis", roulis,"lacet",lacet)