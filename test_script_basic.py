from FireGirl_Landscape import *
from FireGirl_Policy import *
import random

pol = FireGirl_Policy()

lndscpe = FireGirl_Landscape(1,pol)

#testing .drawIgnitionDay()
no_ig = 0
fail = False
low = 99999
high = -99999
for i in range(1000):
	#This function draws a random day to simulate an ignition. 
	#Possible return values are:
	#  -1 -> no ignition this year
	#  positive integer -> date (out of 365) of the ignition
		
	d = lndscpe.drawIgnitionDay()
	
	if d == -1:
		no_ig += 1
	else:
		if d < low: low = d
		if d > high: high = d
		if (d < 0):
			fail = True
		if d > 364:
			fail = True
	
print('Test 1:  landscape.drawIgnitionDay() returned ' + str(no_ig) + ' no-ignition events out of 1000')
print("     high: " + str(high) + "   low: " + str(low))
if fail:
	print('   test failed: landscape.drawIgnitionDay()... Some values out of bounds')
print(" ")
	
#lndscpe.drawLocation(self)
	#This function chooses a random location on the landscape and returns
	#  it as a two-element list
	
	#I'm only allowing fires to start from within the center 43x43 block,
	#   so that there's plenty of buffer around the edges for big fires to
	#   burn into.

#testing .tempMean()
low = 99999
high = -9999
low_day = -1
high_day = -1
for i in range(365):

	#This function returns the mean temperature on the given date
	#It is based on a cosine function which bottoms out on Day 0/365
	
	#Since a pure cosine starts at 1, then drops to -1 at pi, and back to
	# 1 at 2pi, I'm just going to flip it over by multiplying by -1, and then
	# adjusting the range so that entering 365 will be the same as 2pi, etc...
	mean = lndscpe.tempMean(i)
	if mean < low:
		low = mean
		low_day = i
	if mean > high:
		high = mean
		high_day = i
print("Test 2:  landscape.tempMean(self,date) returns:")
print("    Coldest day: " + str(low_day) + " with temp = " + str(low))
print("    Hottest day: " + str(high_day) + " with temp = " + str(high))
print(" ")


#lndscpe.tempVar(self, date)
	#This function returns the variance (sigma) of the temperature distribution
	#   on the given date.
	#For the moment, this is just being held constant.

#testing .drawTemperature(self.date)
	#This function takes a date (out of 365) and draws a day-time temperature.
	#Temperatures are drawn from bell-shaped distributions, whose parameters
	#  vary by date. For instance, the mean of the distribution will be higher
	#  in the mid-summer, and lower elsewhere, whereas the variance of the 
	#  distribution might be greater during the beginning and end of summer.
day_low = [9999, 9999, 9999, 9999]
day_high = [-9999,-9999,-9999,-9999]
day_sum = [0,0,0,0]
day_mean = [-9999,-9999,-9999,-9999]
for day in range(4):
	for draw in range(1000):
		temp = lndscpe.drawTemperature(day*90)
		if temp > day_high[day]:
			day_high[day] = temp
		if temp < day_low[day]:
			day_low[day] = temp
		day_sum[day] += temp
for day in range(4):
	day_mean[day] = day_sum[day] / 1000
print("Test 3:  landscape.drawTemperature(self, date)")
print("  day 0:   low = " + str(day_low[0]) + ", high = " + str(day_high[0]) + ", mean = " + str(day_mean[0]) )
print("  day 90:  low = " + str(day_low[1]) + ", high = " + str(day_high[1]) + ", mean = " + str(day_mean[1]) )
print("  day 180: low = " + str(day_low[2]) + ", high = " + str(day_high[2]) + ", mean = " + str(day_mean[2]) )
print("  day 270: low = " + str(day_low[3]) + ", high = " + str(day_high[3]) + ", mean = " + str(day_mean[3]) )
print(" ")
	
#TESTING lndscpe.drawWindSpeed(self, date)
speeds  = [0,0,0,0,0,0,0,0,0,0,0,0] #twelve of them
fail = False
for i in range(10):
	for j in range(365):
		#This function takes a date (out of 365) and draws a day-time wind speed.
		#Wind speeds are taken from an exponential distribution
		spd = lndscpe.drawWindSpeed(j)
		if spd > 110:
			speeds[11] += 1
		elif spd > 100:
			speeds[10] += 1
		elif spd > 90:
			speeds[9] += 1
		elif spd > 80:
			speeds[8] += 1
		elif spd > 70:
			speeds[7] += 1
		elif spd > 60:
			speeds[6] += 1
		elif spd > 50:
			speeds[5] += 1
		elif spd > 40:
			speeds[4] += 1
		elif spd > 30:
			speeds[3] += 1
		elif spd > 20:
			speeds[2] += 1
		elif spd > 10:
			speeds[1] += 1
		else:
			speeds[0] += 1
		if spd < 0:
			fail = True
print("TEST 4: lndscpe.drawWindSpeed(self, date)")
for i in range(11):
	print("  Speeds < " + str(i*10 + 10) + ": " + str(speeds[i]))
print("  Speeds > 110: " + str(speeds[11]))
print(" ")

#testing .generateNewLandscape()
print("TEST 5: .generateNewLandscape()"),
try:		
	lndscpe.generateNewLandscape(self)
	print(": success")
except:
	print(": FAILED")
print(" ")
	
	
	
#testing fuel and timber averages
fail24 = False
fail8 = False
for i in range(43,86):
	for j in range(43,86):
		sum = 0
		#testing 24's
		for x in range(i-2, i+2):
			for y in range(j-2,j+2):
				if not (i == x and j == y):
					r = random.randint(0,100)
					sum += r
					lndscpe.fuel_load[x][y] = r
					lndscpe.timber_value[x][y] = r+1
		avef = sum / 24
		avet = avef + 1
		f24 = lndscpe.calcFuelAve24(i,j)
		t24 = lndscpe.calcTimberAve24(i, j)
		if not (f24 == avef and t24 == avet):
			fail24 = True
			
		#testing 8's
		for x in range(i-1, i+1):
			for y in range(j-1,j+1):
				if not (i == x and j == y):
					r = random.randint(0,100)
					sum += r
					lndscpe.fuel_load[x][y] = r
					lndscpe.timber_value[x][y] = r+1
		avef = sum / 8
		avet = avef + 1
		f8 = lndscpe.calcFuelAve8(i,j)
		t8 = lndscpe.calcTimberAve8(i, j)
		if not (f8 == avef and t8 == avet):
			fail8 = True

print("TEST 6:  Fuel and Timber Averages - "),
if (fail24 == False and fail8 == False):
	print("  success")
else:
	print("  FAILED")
print(" ")

#testing lndscpe.evaluateSuppressionRule(self, ignite_date, ignite_loc, ignite_wind, ignite_temp)
print("TEST 7: Suppression Rule - args are date, loc=[90,90], wind, temp")
loc = [90,90]
print("loc 90,90 timber = " + str(lndscpe.timber_value[90][90]))
print("        and fuel = " + str(lndscpe.fuel_load[90][90]))
print ("0,loc,0,0 yields: " 		+ str(lndscpe.evaluateSuppressionRule(0,  loc, 0,     0))  )
print ("10,loc,10,10 yields: " 		+ str(lndscpe.evaluateSuppressionRule(10, loc, 10,   10))  )
print ("30,loc,30,30 yields: " 	 	+ str(lndscpe.evaluateSuppressionRule(30, loc, 30,   30))  )
print ("50,loc,50,50 yields: "      + str(lndscpe.evaluateSuppressionRule(50, loc, 50,   50))  )
print ("100,loc,100,100 yields: "   + str(lndscpe.evaluateSuppressionRule(100,loc, 100, 100))  )
print ("200,loc,-100,-100 yields: " + str(lndscpe.evaluateSuppressionRule(200,loc,-100,-100))  )
print ("300,loc,200,0 yields: "     + str(lndscpe.evaluateSuppressionRule(300,loc, 200,   0))  )
print ("180,loc,-100,150 yields: "  + str(lndscpe.evaluateSuppressionRule(180,loc,-100, 150))  )
print(" ")

#testing chooseSuppression
#lndscpe.chooseSuppression(self, suppress_prob)



#testing lndscpe.calcFireSpreadRate(self, wind, temp, fuel)
print("TEST 8: Firespread Rate - args are    wind, temp, fuel")
print("  0,-100,   0 yields:     " + str(lndscpe.calcFireSpreadRate(  0,-100,   0))  )
print("  0,   0,   0 yields:     " + str(lndscpe.calcFireSpreadRate(  0,   0,   0))  )
print("  0, 100,   0 yields:     " + str(lndscpe.calcFireSpreadRate(  0, 100,   0))  )
print("  0,   0, 100 yields:     " + str(lndscpe.calcFireSpreadRate(  0,   0, 100))  )
print("100,   0,   0 yields:     " + str(lndscpe.calcFireSpreadRate(100,   0,   0))  )
print("100, 100, 100 yields:     " + str(lndscpe.calcFireSpreadRate(100, 100, 100))  )
print(" ")

#testing lndscpe.calcCrownFireRisk(self, fuel)
print("TEST 9: Crownfire Risk - arg is fuel")
print("  0 yields:     " + str(lndscpe.calcCrownFireRisk(  0))  )
print(" 20 yields:     " + str(lndscpe.calcCrownFireRisk( 20))  )
print(" 40 yields:     " + str(lndscpe.calcCrownFireRisk( 40))  )
print(" 60 yields:     " + str(lndscpe.calcCrownFireRisk( 60))  )
print(" 80 yields:     " + str(lndscpe.calcCrownFireRisk( 80))  )
print("100 yields:     " + str(lndscpe.calcCrownFireRisk(100))  )
print(" ")			


#testing .generateNewLandscape()
print("TEST 10: .doOneYear"),
try:		
	lndscpe.doOneYear()
	print(": success")
except:
	print(": FAILED")
print(" ")


#testing .generateNewLandscape()
print("TEST 11: .doYears(...)"),
try:		
	lndscpe.doYears(4)
	print(": success")
except:
	print(": FAILED")
print(" ")	

		

