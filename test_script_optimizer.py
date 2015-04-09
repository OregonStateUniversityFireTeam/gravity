from FireGirlOptimizer import *

myOptim = FireGirlPolicyOptimizer()

#testing __init__
#print("Testing __init__.  Bounds should be 10 (-10,10) pairs")
#print(myOptim.b_bounds)
#print(" ")

#testing pathway creation
print("Testing Pathway Creation")
#def createNewDataSet(self, pathway_count, years_per_pathway, policy=None):
myOptim.createFireGirlPathways(10, 20)
print("Pathways created: " + str(len(myOptim.pathway_set)) + " out of 10")
for ls in range(10):
    print("  pathway " + str(ls) + " has " + str(myOptim.pathway_set[ls].getIgnitionCount()) + " logbook entries.")
print(" ")


#DOING YEARS!!!

#DEPRECATED
if False:
    #sumPathwayValues()
    print("Testing sumPathwayValues")
    myOptim.sumPathwayValues()
    print(" pathway values:")
    for v in range(len(myOptim.pathway_net_values)):
        print(" ls " + str(v) + ": " + str(myOptim.pathway_net_values[v]))
    print( " " )


#calcpathwayWeights()
print("Testing calcPathwayWeights")
myOptim.calcPathwayWeights()
print(" pathway weights:")
for w in range(len(myOptim.pathway_weights)):
    print(" ls " + str(w) + ": " + str(myOptim.pathway_weights[w]))
print( " " )

#calcObjectiveFn
