from FireGirlOptimizer import *
FGPO = FireGirlPolicyOptimizer()

pathway_count = 20
iginition_count = 50


#setting new policy
b = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
pol = FireGirlPolicy(b)
FGPO.setPolicy(pol)

print(" ")
print("Generating Initial Set of Pathways")

FGPO.createFireGirlPathways(pathway_count,iginition_count)

print(" ")
#print("Under Wind/Temp Policy: ")
#print("objfn: " + str(FGPO.calcObjFn()))
#print("fprme: " + str(FGPO.calcObjFPrime()))
#print("weights: " + str(FGPO.pathway_weights))
#print("net values: " + str(FGPO.pathway_net_values))

###To Optimize, uncomment the following
print("Beginning Optimization Routine 1")
FGPO.USE_AVE_PROB = True
output=FGPO.optimizePolicy()
FGPO.printOptOutput(output)



### Creating new pathways with the new policy  

#the current policy will have already been set to the new one in the optimization subroutine
#  still, just to be absolutely sure:
print("  ")
print("  ")
print("Generating new pathways using the new policy:")
#print("Policy parameters are: ")
#print(str(FGPO.Policy.b))
#FGPO.createFireGirlPathways(pathway_count,iginition_count,pathway_count,FGPO.Policy)
FGPO.createFireGirlPathways(pathway_count,iginition_count,0,FGPO.Policy)
print(" ")

print("Beginning Optimization Routine 2")
output2=FGPO.optimizePolicy()
FGPO.printOptOutput(output2)
#print("Second iteration policy parameters are: ")
#print(str(FGPO.Policy.b))



### Creating new pathways with the new policy   AGAIN

#the current policy will have already been set to the new one in the optimization subroutine
#  still, just to be absolutely sure:
print("  ")
print("  ")
print("Generating new pathways using the second new policy:")
#print("Policy parameters are: ")
#print(str(FGPO.Policy.b))
#FGPO.createFireGirlPathways(pathway_count,iginition_count,pathway_count*2,FGPO.Policy)
FGPO.createFireGirlPathways(pathway_count,iginition_count,0,FGPO.Policy)
print(" ")

print("Beginning Optimization Routine 3")
output3=FGPO.optimizePolicy()
FGPO.printOptOutput(output3)
#print("Third iteration policy parameters are: ")
#print(str(FGPO.Policy.b))