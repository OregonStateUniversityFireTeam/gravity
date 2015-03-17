from FireGirl_Optimizer import *
from FireGirl_Policy import *


FGPO = FireGirlPolicyOptimizer()

FGPO.createFireGirlLandscapes(4,10) #four landscapes, ten years each

#testing landscape.assignPolicy(params=None, SETALL=x, COUNT=y)
pol0 = FireGirlPolicy(params=None, SETALL=-50, COUNT=11)
pol1 = FireGirlPolicy(params=None, SETALL=0, COUNT=11)
pol2 = FireGirlPolicy(params=None, SETALL=1, COUNT=11)
pol3 = FireGirlPolicy(params=None, SETALL=50, COUNT=11)

FGPO.landscape_set[0].assignPolicy(pol0)
FGPO.landscape_set[1].assignPolicy(pol1)
FGPO.landscape_set[2].assignPolicy(pol2)
FGPO.landscape_set[3].assignPolicy(pol3)

print("Testing landscape.assignPolicy(params=None, SETALL=x, COUNT=y)")
print(" ls0 should have all = -50")
print(FGPO.landscape_set[0].Policy.b)
print(" ls1 should have all = 0")
print(FGPO.landscape_set[1].Policy.b)
print(" ls2 should have all = 1")
print(FGPO.landscape_set[2].Policy.b)
print(" ls3 should have all = 50")
print(FGPO.landscape_set[3].Policy.b)


#testing landscape.assignPolicy(params)
pol4 = FireGirlPolicy(params=[-40,-40,-40,-40,-40,-40,-40,-40,-40,-40,-40])
pol5 = FireGirlPolicy(params=[-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11])
pol6 = FireGirlPolicy(params=[-5,-4,-3,-2,-1,0,1,2,3,4,5])
pol7 = FireGirlPolicy(params=[40,40,40,40,40,40,40,40,40,40,40])

FGPO.landscape_set[0].assignPolicy(pol4)
FGPO.landscape_set[1].assignPolicy(pol5)
FGPO.landscape_set[2].assignPolicy(pol6)
FGPO.landscape_set[3].assignPolicy(pol7)
print(" ")
print(" ")
print("Testing landscape.assignPolicy(params=[])")
print(" ls0 should have all = -40")
print(FGPO.landscape_set[0].Policy.b)
print(" ls1 should have params from -1 to -11")
print(FGPO.landscape_set[1].Policy.b)
print(" ls2 should have params from -5 to 5")
print(FGPO.landscape_set[2].Policy.b)
print(" ls3 should have all = 40")
print(FGPO.landscape_set[3].Policy.b)


#testing landscape.calcTotalProb()
print(" ")
print(" ")
print("Testing landscape.calcTotalProb()")
print("ls0   "),
print(FGPO.landscape_set[0].calcTotalProb())
print("ls1   "),
print(FGPO.landscape_set[1].calcTotalProb())
print("ls2   "),
print(FGPO.landscape_set[2].calcTotalProb())
print("ls3   "),
print(FGPO.landscape_set[3].calcTotalProb())
print("  and the resulting landscape_weights are:")
FGPO.calcLandscapeWeights()
print(FGPO.landscape_weights)


#testing ignition.getProb for each ignition in each landscape
print(" ")
print(" ")
print("Printing ignition.getProb() values for each ignition in each landscape")
for i in range(10):
	if i == 0:
		print("ls0    ls1    ls2    ls3")
	for l in range(4):
		print("{0:3.3f} ".format(FGPO.landscape_set[l].ignitions[i].getProb())),
	print(" ") #for an endline
	
#the getProb() function returns values which were set in landscape.DoYear() step 2 
#   it uses the landscape.evaluateSuppressionRule(ignite_date, ignite_loc, ignite_wind, ignite_temp) command

#Printing the fire features for each landscape's ignitions
print(" ")
for ls in FGPO.landscape_set:
	print("Landscape " + str(ls.ID_number) + " ignition features")
	for i in range(10):
		ftrs = ls.ignitions[i].getFeatures()
		for f in range(11):
			print(round(ftrs[f],3)),
		print(" ") #for a line break
		
		
#Testing evaluateSuppressionRule(self, ignite_date, ignite_loc, ignite_wind, ignite_temp)
print(" ")
print(" ")
print("Testing landscape.evaluateSuppressionRule(self, ignite_date, ignite_loc, ignite_wind, ignite_temp)")
for ls in FGPO.landscape_set:
	print("Landscape " + str(ls.ID_number) + " .evaluateSuppressionRule() returns: ")
	for i in range(10):
		#needed ign feature indices are 1, location, 3, 4
		f = ls.ignitions[i].getFeatures()
		loc = ls.ignitions[i].location
		print(ls.evaluateSuppressionRule(f[1], loc, f[3], f[4]))


#Testing landscape.Policy.calcProb(features) and .crossProduct()
print(" ")
print(" ")
print("Testing landscape.Policy.calcProb(features) return values:")
for ls in FGPO.landscape_set:
	print("Landscape " + str(ls.ID_number) + " .Policy.calcProb(features) returns: ")
	print("Policy b[]: " + str(ls.Policy.b))
	for i in range(10):
		#needed ign feature indices are 1, location, 3, 4
		f = ls.ignitions[i].getFeatures()
		print("Cross Product: " + str(ls.Policy.crossProduct(f)))
		print("calcProb: " + str(ls.Policy.calcProb(f)))