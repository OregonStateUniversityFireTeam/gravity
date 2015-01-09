import argparse, random, math

def main():
	
	#just getting arguments... see Optimization code for a description
	parser = argparse.ArgumentParser()
	parser.add_argument("-y", "--years", type=int, default=10, help="number of years to run for each landscape")
	parser.add_argument("-l", "--lineages", "--landscapes", default=5, type=int, help="number of landscapes (aka lineages) to simulate")
	parser.add_argument("-p", "--printset", action="store_true", help="Print the dataset to screen")
	parser.add_argument("-o", "--outputoff", action="store_true", help="Suppress file output")

	args = parser.parse_args()
	
	lins = args.lineages
	years = args.years
	writefile = True
	printset = False
	
	if args.printset:
		printset = True
	
	#Make a new dataset
	if not(args.outputoff):
		dataset = genDataSet([0,0,0,0], lins, years, printset, True, "dataset1.txt")
	else:
		dataset = genDataSet([0,0,0,0], lins, years, printset)
		
	
def genDataSet(B=[0,0,0,0], lins=1, years=1, printset=False, writefile=False, filename="dataset1.txt"):
	#This is the primary function in this file. It creates a new dataset, consisting of a number of landscapes which
	#  each evolve over a number of years.  It can then write to files, or standard out.
		
	#Create a list of landscape values
	lineage_cost = []
	#Create a list of landscapes, which has members that are lists of years
	lineages = []
	for l in range(lins):
		lineages.append([])
		lineage_cost.append(0)
		for y in range(years):
			#for each year, generate a list of features.. just modelling conditions in an abstract way.
			lineages[l].append(genFeatures())
	
	#Calculate the net cost of each landscape as the sum of the value of each fire(year)
	for l in range(lins):
		for y in range(years):
			lineage_cost[l] += calcCost(lineages[l][y][0],
			                            lineages[l][y][1],
						    lineages[l][y][2],
						    lineages[l][y][3], policy(lineages[l][y], B, 3))
	
	if printset:
		print(lineages)
		print(lineage_cost)
	
	if writefile:
		writeAll([lineages, lineage_cost], filename)
	
	#this is the format of the "dataset"  It is a list of lineages, and a list of their "costs" which are just the landscape values
	return [lineages,lineage_cost]

def writeAll(dataset,name):
	#just writing it out... nothing interesting
	name = str(name)
	f = open(name, 'w')
	data = dataset[0]
	values = dataset[1]
	f.write("#DataSet " + name + "\n")
	for l in range(len(data)):
		f.write("#Lineage" + str(l) + "\n")
		for y in range(len(data[l])):
			f.write("L_" + str(l) + "_Y_" + str(y) + ",")
			f.write(str(data[l][y][0]) + ",")
			f.write(str(data[l][y][1]) + ",")
			f.write(str(data[l][y][2]) + ",")
			f.write(str(data[l][y][3]) + "\n")
			
	f.write("#Final Values of " + name + "\n")
	for l in range(len(values)):
		f.write(str(values[l]))
		if l < (len(values) - 1):
			f.write(",")
		else:
			f.write("\n")
			
	f.close()
	
	
def calcCost(x1, x2, x3, x4,suppress):
	#This function calculates the cost of a fire according to a "hidden" "black box" function ;)
	
	#burn_net = x4*(x1-x2+x3-50) #older version... different (unstable) dynamics
	burn_net = ((20-x1)**2 + (40-x2)**2 + (60-x3)**2 )* (80-x4)**2
	
	if suppress:
		#suppression cost is high if the fire is a big one
		if burn_net > 50:
			return 50 + (burn_net - 50) #for emphasis
			
		#and costs only 50 if it's a small one
		else:
			return 50
	
	#otherwise, the cost is just the burn itself
	else:
		return burn_net

def genFeatures(count=4):
	#generating random features for a year. they are uniform throughout the year, and there is only one pixel
	vals = []
	for i in range(count-1):
		vals.append(random.randint(0,100))
	vals.append(random.randint(1,4)) #the last one is the landscape value surrogate...shouldn't be so big
	return vals

def policy_decimal(X,B,length):
	#does the dot-product of a year's features by policy parameters, and takes the logistic
	inside = 0
	for i in range(length):
		inside += X[i]*B[i]
	return logistic_fn(inside)
	
def policy(X,B,length):
	#returns true if the resulting policy_decimal() value is 50% or greater
	decimal = policy_decimal(X,B,length)
	if decimal >= 0.5:
		return True
	else:
		return False
	
def logistic_fn(x):
	#calculate the simple logistic funtion value of x
	return 1 / (1 + math.exp(-x))

if __name__ == "__main__":
   main()
