from FireGirl_Optimizer import *
import random

random.seed(0)

#create landscapes
landscapes = []
for l in range(100):
    landscapes.append(FireGirlLandscape(l))


#create ignitions
for ls in landscapes:
    for i in range(200):
        ign = FireGirlIgnitionRecord()
        f1 = random.randint(-100,100)
        f2 = random.randint(-100,100)
        f3 = random.randint(-100,100)
        f4 = random.randint(-100,100)
        ign.features = [1,f1,f2,f3,f4,0,0,0,0,0,0]
        
        danger = (1.5)*f1 + (0.5)*f2 - (0.5)*f3 - (1.0)*f4
        
        choice = bool(random.randint(0,1))
        ign.policy_choice = choice
        
        ls.ignitions.append(ign)
        
        #note that the if danger statement is not necessary at the moment, but will be if
        # future scripts (based on this one) need non-symmetrical behavior between suppression
        # and not-suppression
        if danger > 0:
            #this fire should be suppressed. If suppressed, add the value (which is positive)
            #  as a reward. If let-burned, subtract the value
            if choice == True:
                ls.net_value += danger
            else:
                ls.net_value -= danger
        else:
            #this fire should be allowed to burn. If suppressed, add the value (which is negative)
            #  as a penalty for suppressing a good fire.  If allowed to burn, subtract the value,
            #  again, which is negative, as a reward for choosing correctly
            if choice == True:
                ls.net_value += danger
            else:
                ls.net_value -= danger

                
#create optimizer
opt = FireGirlPolicyOptimizer()
opt.landscape_set = landscapes

#Printing values with Total Prob
objfn1 = opt.calcObjFn()
fprm1 = opt.calcObjFPrime()

#Printing initial values
print("Initial Values with Total Prob")
print("Obj Fn: " + str(objfn1))
print("Fprime: " + str(fprm1))

#Printing values with Ave Prob
opt.USE_AVE_PROB = True
objfn1 = opt.calcObjFn()
fprm1 = opt.calcObjFPrime()

#Printing initial values
print(" ")
print("Initial Values with Ave. Prob")
print("Obj Fn: " + str(objfn1))
print("Fprime: " + str(fprm1))


#Optimizing with total prob
if True:

    print(" ")
    print(" ")
    print("Optimizing Policy using total-prob calculations")
    opt.USE_AVE_PROB = False
    opt.Policy.b = [0,0,0,0,0,0,0,0,0,0,0]
    output = opt.optimizePolicy(1)
    opt.printOptOutput(output)
    
#Optimizing with average prob
if True:

    print(" ")
    print(" ")
    print("Optimizing Policy using average-prob calculations")
    opt.USE_AVE_PROB = True
    opt.Policy.b = [0,0,0,0,0,0,0,0,0,0,0]
    output = opt.optimizePolicy(1)
    opt.printOptOutput(output)