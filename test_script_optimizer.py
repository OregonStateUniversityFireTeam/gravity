from FireGirl_Optimizer import *

myOptim = FireGirl_Optimizer()

#testing __init__
print("Testing __init__.  Bounds should be 10 (-10,10) pairs")
print(myOptim.b_bounds)
print(" ")

#testing landscape creation
print("Testing Landscape Creation")
#def createNewDataSet(self, landscape_count, years_per_landscape, policy=None):
myOptim.createNewDataSet(10, 20)
print("landscapes created: " + str(len(myOptim.landscape_set)) + " out of 10")
for ls in range(10):
    print("  landscape " + str(ls) + "has " + str(len(myOptim.landscape_set[ls].log_list)) + " logbook entries.")
print(" ")


#DOING YEARS!!!

#sumLandscapeValues()
print("Testing sumLandscapeValues")
myOptim.sumLandscapeValues()
print(" landscape values:")
for v in range(len(myOptim.landscape_net_values)):
    print(" ls " + str(v) + ": " + str(myOptim.landscape_net_values[v]))
print( " " )


#calcLandscapeWeights()
print("Testing calcLandscapeWeights")
myOptim.calcLandscapeWeights()
print(" landscape weights:")
for w in range(len(myOptim.landscape_weights)):
    print(" ls " + str(w) + ": " + str(myOptim.landscape_weights[w]))
print( " " )

#calcObjectiveFn
