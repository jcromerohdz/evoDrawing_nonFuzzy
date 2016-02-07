
import math



def get_level(points):
	base = 2 # change to change the rate at which you go through the levels
	levels = 30
	finalPoints = 2000
	scale = levels/math.log(finalPoints, base)
	level = math.floor(scale*math.log(points, base))

	return level
	
        
        



    


print get_level(4)