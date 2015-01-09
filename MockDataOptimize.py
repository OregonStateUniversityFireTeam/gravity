from MockDataGenerator import *
from MockDataReader import *
from scipy.optimize import *
import math, time


# -HKB-
# Here are the important function signatures from other libraries that are being used below

#scipy.optimize.fmin_l_bfgs_b(func, x0, fprime=None, args=(), approx_grad=0, bounds=None, m=10, factr=10000000.0, pgtol=1e-05, epsilon=1e-08, iprint=-1, maxfun=15000, maxiter=15000, disp=None, callback=None)[source]
#def genDataSet(B=[0,0,0,0], lins=1, years=1, printset=False, writefile=False, filename="dataset1.txt")

def main():

	#This is just a generic arguement parser setup from
	# https://docs.python.org/3/library/argparse.html
	#
	# "iterations" is the number of times the script will run the gradient descent mechanism.
	#    Looking at one set of landscapes and optimizing a policy counts as one iteration
	#    so then if you use that new policy on a new set of data, that would be two iterations, and so on.
	#
	# "years" is just the number of fire/growth cycles that will be used on my mock data generation scheme. 
	#     It's the analog to the year count in the full-up FireWoman code.
	#
	# "lineages" or "landscapes" is the number of independent landscapes to use. Each landscape undergoes only 
	#     a single evolution... that is, there are no comparisions between initial choices or anything like that.
	#     Just make a new landscape, let fires burn, and decide each time (based on the policy at the time) whether
	#     to suppress or let-burn.
	
	parser = argparse.ArgumentParser()
	parser.add_argument("-i","--iterations", type=int, default=10, help="number of iterations through the optimizer")
	parser.add_argument("-y", "--years", type=int, default=10, help="number of years to run for each landscape")
	parser.add_argument("-l", "--lineages", "--landscapes", default=5, type=int, help="number of landscapes (aka lineages) to simulate")

	# Recording the arguements which were passed in to this script
	args = parser.parse_args()
	
	# Sorting out the arguments
	lins = args.lineages
	years = args.years
	iters = args.iterations
	
	#Bpol is the policy itself. In this case, we're only using four features/variables/attributes, so there are,
	#  likewise, only four parameters.
	Bpol = [0,0,0,0]
	
	# for each iteration, optim() will take the current policy and run a single iteration, then assign the new,
	#     updated policy back to Bpol, which is then used for the next iteration, etc...
	for i in range(iters):
		# optim() takes a second argument, which is a starting point for the policy parameters, as used by
		#    the scipy functions. In this case, we're just going to start with each parameter set to the values...
		#    It's just a formality, but allows for more complex behavior if desired later
		Bpol = optim(Bpol,Bpol,lins,years,i)
		
	# because optim() handles it's own print statements internally, nothing else happens in main()
	
def optim(Bcreate=[0,0,0,0], B0=[0,0,0,0], lins=50, yrs=50,iter=0):
	#recording the system time
	t0 = time.time()
	
	#setting the initial start point. Can be commented out to allow the B0 argument to actually function...
	B0 = [0,0,0,0]
	
	#new file, using the "iter" value. This lets each iteration print to it's own output file
	filename = "dataset_iter_" + str(iter) + ".txt"
	
	# Generate a new dataset
	#dataset = genDataSet(Bcreate,lins,yrs,False,True,filename) #will output each iteration's underlying data to files
	dataset = genDataSet(Bcreate,lins,yrs,False,False) #will not output underlying data sets to files
	
	#running the scipy gradient descent method
	#signature is:
	#scipy.optimize.fmin_l_bfgs_b(func, x0, fprime=None, args=(), approx_grad=0, bounds=None, m=10, factr=10000000.0, pgtol=1e-05, epsilon=1e-08, iprint=-1, maxfun=15000, maxiter=15000, disp=None, callback=None)
	# objFn is a function name, at is referenceing the objective function at the end of this file
	# B0 is a list of zeroes, or whatever is passed in to optim(). It is the starting parameters that fmin_l_bfgs_b() will use
	# "None" is telling fmin...() that we are not passing in a function to calculate derivitave values
	# [dataset] is the matrix fmin...() needs. It's rows are each fire, and columns are each feature
	# "True" is telling fmin...() to approximate it's own derivatives
	# "None" (the second time) is specifying "no bounds" on what the parameters can be. This should be changed into a list of 
	#     upper and lower bound pairs. See scipy.optimize.fmin_l_bfgs_b documentation.
	# The rest of the arguments are left as defaults.
	output = fmin_l_bfgs_b(objFn, B0, None, [dataset], True, None)
	
	#recording system time again
	t1 = time.time()
	
	#printing the results.  "Estimated B's" are the values for the parameters: this is the policy given by fmin...()
	print("\nOPTIMIZATION OUTPUT, Iteration " + str(iter) + ":")
	print("Estimated B's:"+ "   " + str(output[0]))
	print("Value of f() at minimum:" + "   " + str(output[1]))
	print("Running Time:   " + str(t1-t0) + " sec")
	#print("Messages:")
	#for m in output[2]:
	#	print (str(m) + ":     " + str(output[2][m]))
	
	#output[0] is the list of policy parameters. Other elements are documented in the scipy.optimize.fmin_l_bfgs_b docs.
	return output[0]


def objFn(B, dataset):
	#This function takes the dataset and a policy and calculates the weighted value of the whole set.
	#  This is the heart of my algorithm... each landscape value is weighted by the overall probability of having been
	#  chosen, given a policy.
	
	#new list for the weighting values
	probweights = []
	
	#assigning weights of 1, to start with
	for lin in range(len(dataset[0])):
		probweights.append(1)
	
	#for each year/decision, calculating the dot-product of that year's features and policy parameters, and then
	# summing their logarithms (same as doing the product of the probabilities)
	for lin in range(len(dataset[0])):
		for yr in range(len(dataset[0][0])):
			X = dataset[0][lin][yr]
			
			#policy_decimal() is a function that does the logistic math, and returns the decimal output
			probweights[lin] = probweights[lin]+math.log(policy_decimal(X,B,len(X)))
	
	# adding up all the value from each landscape for the total value of the entire dataset
	objvalue = 0
	for i in range(len(probweights)):
		objvalue += probweights[i]*dataset[1][i]
	
	# since this is a minimization algorthim, and because higher values are "better", return the negative of the value
	return (-1)*objvalue
	

	
if __name__ == "__main__":
   main()
