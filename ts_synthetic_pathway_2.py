from FireGirlOptimizer import *
import random

random.seed(0)

#create pathways
pathways = []
for l in range(100):
    pathways.append(FireGirlPathway(l))


#create ignitions
for ls in pathways:
    for i in range(15):
        ign = FireGirlIgnitionRecord()
        f1 = random.randint(-100,100)
        f2 = random.randint(-100,100)
        f3 = random.randint(-100,100)
        f4 = random.randint(-100,100)
        ign.features = [1,f1,f2,f3,f4,0,0,0,0,0,0]
        
        danger = (1.0)*f1 + (0.5)*f2 - (0.5)*f3 - (1.0)*f4
        
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
opt.pathway_set = pathways

objfn1 = opt.calcObjFn()
fprm1 = opt.calcObjFPrime()

#Printing initial values
print("Initial Values")
print("Obj Fn: " + str(objfn1))
print("Fprime: " + str(fprm1))
#print("net values: " + str(opt.pathway_net_values))
#print("weights : " + str(opt.pathway_weights))

#Optimizing
if True:

    print(" ")
    print(" ")
    print("Optimizing Policy, beginning with a coin-toss policy ")
    opt.Policy.b = [0,0,0,0,0,0,0,0,0,0,0]
    output = opt.optimizePolicy(1)
    print("Outputs")
    opt.printOptOutput(output)
    
if False:

    print(" ")
    print(" ")
    print("Optimizing Policy, beginning with a nudged policy ")
    opt.Policy.b = [0,0.2,0.2,-0.2,-0.2,0,0,0,0,0,0]
    output = opt.optimizePolicy(1)
    print("Outputs")
    opt.printOptOutput(output)
    #print("raw outputs")
    #print(str(output))