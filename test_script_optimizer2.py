from FireGirl_Optimizer import *
FGPO = FireGirlPolicyOptimizer()

###To create, uncomment the following two lines:
FGPO.createFireGirlLandscapes(100,50)
#FGPO.saveFireGirlLandscapes("FG_landscapes_20x50.fgl")

###To load (already created data), uncomment the following line
#FGPO.loadFireGirlLandscapes("FG_landscapes_20x50.fgl")


#print("objfn: " + str(FGPO.calcObjFn()))
#print("fprme: " + str(FGPO.calcObjFPrime()))
#print("weights: " + str(FGPO.landscape_weights))
#print("net values: " + str(FGPO.landscape_net_values))

#setting new policy
b = [0,0,0,0,0,0,0,0,0,0,0]
pol = FireGirlPolicy(b)
FGPO.setPolicy(pol)
print(" ")
#print("Under Wind/Temp Policy: ")
#print("objfn: " + str(FGPO.calcObjFn()))
#print("fprme: " + str(FGPO.calcObjFPrime()))
#print("weights: " + str(FGPO.landscape_weights))
#print("net values: " + str(FGPO.landscape_net_values))

###To Optimize, uncomment the following
print("Beginning Optimization Routine")
FGPO.USE_AVE_PROB = True
output=FGPO.optimizePolicy()
FGPO.printOptOutput(output)