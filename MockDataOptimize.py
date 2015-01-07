from MockDataGenerator import *
from MockDataReader import *
from scipy.optimize import *
import math, time

#scipy.optimize.fmin_l_bfgs_b(func, x0, fprime=None, args=(), approx_grad=0, bounds=None, m=10, factr=10000000.0, pgtol=1e-05, epsilon=1e-08, iprint=-1, maxfun=15000, maxiter=15000, disp=None, callback=None)[source]
#def genDataSet(B=[0,0,0,0], lins=1, years=1, printset=False, writefile=False, filename="dataset1.txt")

def main():

	parser = argparse.ArgumentParser()
	parser.add_argument("-i","--iterations", type=int, default=10, help="number of iterations through the optimizer")
	parser.add_argument("-y", "--years", type=int, default=10, help="number of years to run for each landscape")
	parser.add_argument("-l", "--lineages", "--landscapes", default=5, type=int, help="number of landscapes (aka lineages) to simulate")

	args = parser.parse_args()
	
	lins = args.lineages
	years = args.years
	iters = args.iterations
	
	Bpol = [0,0,0,0]
	for i in range(iters):
		Bpol = optim(Bpol,Bpol,lins,years,i)
	
def optim(Bcreate=[0,0,0,0], B0=[0,0,0,0], lins=50, yrs=50,iter=0):
	t0 = time.time()
	B0 = [0,0,0,0]
	filename = "dataset_iter_" + str(iter) + ".txt"
	#dataset = genDataSet(Bcreate,lins,yrs,False,True,filename) #will output each iteration's underlying data
	dataset = genDataSet(Bcreate,lins,yrs,False,False) #will not output underlying data sets
	output = fmin_l_bfgs_b(objFn, B0, None, [dataset], True, None)
	t1 = time.time()
	print("\nOPTIMIZATION OUTPUT, Iteration " + str(iter) + ":")
	print("Estimated B's:"+ "   " + str(output[0]))
	print("Value of f() at minimum:" + "   " + str(output[1]))
	print("Running Time:   " + str(t1-t0) + " sec")
	#print("Messages:")
	#for m in output[2]:
	#	print (str(m) + ":     " + str(output[2][m]))
	
	return output[0]


def objFn(B, dataset):
	probweights = []
	for lin in range(len(dataset[0])):
		probweights.append(1)
	for lin in range(len(dataset[0])):
		for yr in range(len(dataset[0][0])):
			X = dataset[0][lin][yr]
			probweights[lin] = probweights[lin]+math.log(policy_decimal(X,B,len(X)))
	
	objvalue = 0
	for i in range(len(probweights)):
		objvalue += probweights[i]*dataset[1][i]
	
	return (-1)*objvalue
	

	
if __name__ == "__main__":
   main()