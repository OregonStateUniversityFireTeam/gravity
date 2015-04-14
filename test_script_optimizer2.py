from FireGirlOptimizer import *
FGPO = FireGirlPolicyOptimizer()

###To create, uncomment the following two lines:
FGPO.createFireGirlPathways(10,50)
#FGPO.saveFireGirlPathways("FG_pathways_20x50.fgl")

###To load (already created data), uncomment the following line
#FGPO.loadFireGirlPathways("FG_pathways_20x50.fgl")


#print("objfn: " + str(FGPO.calcObjFn()))
#print("fprme: " + str(FGPO.calcObjFPrime()))
#print("weights: " + str(FGPO.pathway_weights))
#print("net values: " + str(FGPO.pathway_net_values))

#setting new policy
b = [0,0,0,0,0,0,0,0,0,0,0]
pol = FireGirlPolicy(b)
FGPO.setPolicy(pol)
print(" ")
#print("Under Wind/Temp Policy: ")
#print("objfn: " + str(FGPO.calcObjFn()))
#print("fprme: " + str(FGPO.calcObjFPrime()))
#print("weights: " + str(FGPO.pathway_weights))
#print("net values: " + str(FGPO.pathway_net_values))

###To Optimize, uncomment the following
print("Beginning Optimization Routine")
FGPO.USE_AVE_PROB = False
output=FGPO.optimizePolicy()
FGPO.printOptOutput(output)