from FireGirlOptimizer import *
from FireGirlPolicy import *


FGPO = FireGirlPolicyOptimizer()
pol0 = FireGirlPolicy(params=None, SETALL=-50, COUNT=11)
FGPO.createFireGirlPathways(4,10,pol0) #four pathways, ten years each, policy

#testing pathway.assignPolicy(params=None, SETALL=x, COUNT=y)
pol1 = FireGirlPolicy(params=None, SETALL=0, COUNT=11)
pol2 = FireGirlPolicy(params=None, SETALL=1, COUNT=11)
pol3 = FireGirlPolicy(params=None, SETALL=50, COUNT=11)

FGPO.pathway_set[0].assignPolicy(pol0)
FGPO.pathway_set[1].assignPolicy(pol1)
FGPO.pathway_set[2].assignPolicy(pol2)
FGPO.pathway_set[3].assignPolicy(pol3)

print("Testing pathway.assignPolicy(params=None, SETALL=x, COUNT=y)")
print(" ls0 should have all = -50")
print(FGPO.pathway_set[0].Policy.b)
print(" ls1 should have all = 0")
print(FGPO.pathway_set[1].Policy.b)
print(" ls2 should have all = 1")
print(FGPO.pathway_set[2].Policy.b)
print(" ls3 should have all = 50")
print(FGPO.pathway_set[3].Policy.b)


#testing pathway.assignPolicy(params)
pol4 = FireGirlPolicy(params=[-40,-40,-40,-40,-40,-40,-40,-40,-40,-40,-40])
pol5 = FireGirlPolicy(params=[-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11])
pol6 = FireGirlPolicy(params=[-5,-4,-3,-2,-1,0,1,2,3,4,5])
pol7 = FireGirlPolicy(params=[40,40,40,40,40,40,40,40,40,40,40])

FGPO.pathway_set[0].assignPolicy(pol4)
FGPO.pathway_set[1].assignPolicy(pol5)
FGPO.pathway_set[2].assignPolicy(pol6)
FGPO.pathway_set[3].assignPolicy(pol7)
print(" ")
print(" ")
print("Testing pathway.assignPolicy(params=[])")
print(" ls0 should have all = -40")
print(FGPO.pathway_set[0].Policy.b)
print(" ls1 should have params from -1 to -11")
print(FGPO.pathway_set[1].Policy.b)
print(" ls2 should have params from -5 to 5")
print(FGPO.pathway_set[2].Policy.b)
print(" ls3 should have all = 40")
print(FGPO.pathway_set[3].Policy.b)


#testing pathway.calcTotalProb()
print(" ")
print(" ")
print("Testing pathway.calcTotalProb() with suppress policy")
FGPO.Policy = pol7
print("ls0   "),
print(FGPO.pathway_set[0].calcTotalProb())
print("ls1   "),
print(FGPO.pathway_set[1].calcTotalProb())
print("ls2   "),
print(FGPO.pathway_set[2].calcTotalProb())
print("ls3   "),
print(FGPO.pathway_set[3].calcTotalProb())
print("  and the resulting pathway_weights are:")
FGPO.calcPathwayWeights()
print(FGPO.pathway_weights)

#testing pathway.calcTotalProb()
print(" ")
print(" ")
print("Testing pathway.calcTotalProb() with let-burn policy")
FGPO.Policy = pol0
print("ls0   "),
print(FGPO.pathway_set[0].calcTotalProb())
print("ls1   "),
print(FGPO.pathway_set[1].calcTotalProb())
print("ls2   "),
print(FGPO.pathway_set[2].calcTotalProb())
print("ls3   "),
print(FGPO.pathway_set[3].calcTotalProb())
print("  and the resulting pathway_weights are:")
FGPO.calcPathwayWeights()
print(FGPO.pathway_weights)

#testing pathway.calcTotalProb()
print(" ")
print(" ")
print("Testing pathway.calcTotalProb() with coin-toss policy")
FGPO.Policy = pol1
print("ls0   "),
print(FGPO.pathway_set[0].calcTotalProb())
print("ls1   "),
print(FGPO.pathway_set[1].calcTotalProb())
print("ls2   "),
print(FGPO.pathway_set[2].calcTotalProb())
print("ls3   "),
print(FGPO.pathway_set[3].calcTotalProb())
print("  and the resulting pathway_weights are:")
FGPO.calcPathwayWeights()
print(FGPO.pathway_weights)


#testing ignition.getProb for each ignition in each pathway
if False:
	print(" ")
	print(" ")
	print("Printing ignition.getProb() values for each ignition in each pathway")
	for i in range(10):
		if i == 0:
			print("ls0    ls1    ls2    ls3")
		for l in range(4):
			print("{0:3.3f} ".format(FGPO.pathway_set[l].ignitions[i].getProb())),
		print(" ") #for an endline
	
#the getProb() function returns values which were set in pathway.DoYear() step 2 
#   it uses the pathway.evaluateSuppressionRule(ignite_date, ignite_loc, ignite_wind, ignite_temp) command

#Printing the fire features for each pathway's ignitions
if False:
	print(" ")
	for ls in FGPO.pathway_set:
		print("Pathway " + str(ls.ID_number) + " ignition features")
		for i in range(10):
			ftrs = ls.ignitions[i].getFeatures()
			for f in range(11):
				print(round(ftrs[f],3)),
			print(" ") #for a line break
		
		
#Testing evaluateSuppressionRule(self, ignite_date, ignite_loc, ignite_wind, ignite_temp)
print(" ")
print(" ")
print("Testing pathway.evaluateSuppressionRule(self, ignite_date, ignite_loc, ignite_wind, ignite_temp)")
for ls in FGPO.pathway_set:
	print("Pathway " + str(ls.ID_number) + " .evaluateSuppressionRule() returns: ")
	for i in range(10):
		#needed ign feature indices are 1, location, 3, 4
		f = ls.ignitions[i].getFeatures()
		loc = ls.ignitions[i].location
		print(ls.evaluateSuppressionRule(f[1], loc, f[3], f[4]))


#Testing pathway.Policy.calcProb(features) and .crossProduct()
if False:
	print(" ")
	print(" ")
	print("Testing pathway.Policy.calcProb(features) return values:")
	for ls in FGPO.pathway_set:
		print("Pathway " + str(ls.ID_number) + " .Policy.calcProb(features) returns: ")
		print("Policy b[]: " + str(ls.Policy.b))
		for i in range(10):
			#needed ign feature indices are 1, location, 3, 4
			f = ls.ignitions[i].getFeatures()
			print("Cross Product: " + str(ls.Policy.crossProduct(f)))
			print("calcProb: " + str(ls.Policy.calcProb(f)))



#Testing calcObjFn() with different policies
print(" ")
print(" ")
print("Testing calcObjFn() and calcObjFPrime() with a let-burn policy")
FGPO.Policy = pol0
print("calcObjFn() returns: " + str(FGPO.calcObjFn()))
print("calcObjFPrime() returns: " + str(FGPO.calcObjFPrime()))

print(" ")
print("Testing calcObjFn() and calcObjFPrime() with a coin-toss policy")
FGPO.Policy = pol1
print("calcObjFn() returns: " + str(FGPO.calcObjFn()))
print("calcObjFPrime() returns: " + str(FGPO.calcObjFPrime()))

print(" ")
print("Testing calcObjFn() and calcObjFPrime() with a suppress-all policy")
FGPO.Policy = pol7
print("calcObjFn() returns: " + str(FGPO.calcObjFn()))
print("calcObjFPrime() returns: " + str(FGPO.calcObjFPrime()))
