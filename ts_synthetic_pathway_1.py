from FireGirlOptimizer import *
#from FireGirlPathway import *
#from FireGirlPolicy import *
#from FireGirlPathwayLogbook import *

#without initializing a policy, these will each have an all-zero (coin-toss) policy
ls0 = FireGirlPathway(0)
ls1 = FireGirlPathway(1)
ls2 = FireGirlPathway(2)
ls3 = FireGirlPathway(3)


#setting ignition records manually

# "correct" decision 1
ig1a = FireGirlIgnitionRecord()
ig1a.features = [1,100,-100,0,0,0,0,0,0,0,0]
ig1a.policy_prob = 0.5
ig1a.policy_choice = True #suppress
ig1a.year = 0

# "incorrect" decision 1
ig1b = FireGirlIgnitionRecord()
ig1b.features = [1,100,-100,0,0,0,0,0,0,0,0]
ig1b.policy_prob = 0.5
ig1b.policy_choice = False #let-burn
ig1b.year = 0

# "correct" decision 2
ig2a = FireGirlIgnitionRecord()
ig2a.features = [1,-100,100,0,0,0,0,0,0,0,0]
ig2a.policy_prob = 0.5
ig2a.policy_choice = False #let-burn
ig2a.year = 1

# "incorrect" decision 2
ig2b = FireGirlIgnitionRecord()
ig2b.features = [1,-100,100,0,0,0,0,0,0,0,0]
ig2b.policy_prob = 0.5
ig2b.policy_choice = True #suppress
ig2b.year = 1



#setting pathway results manually
# LS0 : +Suppress+ -Suppress- : Value = 0
# LS1 : -Let-Burn- -Suppress- : Value = -100
# LS2 : +Suppress+ +Let-Burn+ : Value = 100
# LS3 : -Let-Burn- +Let-Burn+ : Value = 0

#instead of calling ls.updateNetValue() to have it calculate anything, I'm just
# accessing the .net_value members directly
ls0.year = 1
ls0.ignitions.append(ig1a) #right
ls0.ignitions.append(ig2b) #wrong
ls0.net_value = 0

ls1.year = 1
ls1.ignitions.append(ig1b) #wrong
ls1.ignitions.append(ig2b) #wrong
ls1.net_value = -200

ls2.year = 1
ls2.ignitions.append(ig1a) #right
ls2.ignitions.append(ig2a) #right
ls2.net_value = 200

ls3.year = 1
ls3.ignitions.append(ig1b) #wrong
ls3.ignitions.append(ig2a) #right
ls3.net_value = 0



#Add pathways to a new Optimizer object

opt = FireGirlPolicyOptimizer()
opt.pathway_set.append(ls0)
opt.pathway_set.append(ls1)
opt.pathway_set.append(ls2)
opt.pathway_set.append(ls3)

objfn1 = opt.calcObjFn()
fprm1 = opt.calcObjFPrime()

#Printing initial values
print("Obj Fn: " + str(objfn1))
print("Fprime: " + str(fprm1))
print("net values: " + str(opt.pathway_net_values))
print("weights : " + str(opt.pathway_weights))

#Trying it with my known, best policy
print(" ")
print(" ")
print("Trying new calculations with my best policy")
opt.Policy.b = [0,1,-1,0,0,0,0,0,0,0,0]
objfn2 = opt.calcObjFn()
fprm2 = opt.calcObjFPrime()

#Printing initial values
print("Obj Fn: " + str(objfn2))
print("Fprime: " + str(fprm2))
print("net values: " + str(opt.pathway_net_values))
print("weights : " + str(opt.pathway_weights))


#Trying it with my known, best policy
print(" ")
print(" ")
print("Trying new calculations with a bad policy")
opt.Policy.b = [0,-1,1,0,0,0,0,0,0,0,0]
objfn2 = opt.calcObjFn()
fprm2 = opt.calcObjFPrime()

#Printing initial values
print("Obj Fn: " + str(objfn2))
print("Fprime: " + str(fprm2))
print("net values: " + str(opt.pathway_net_values))
print("weights : " + str(opt.pathway_weights))


#Optimizing
if True:

    print(" ")
    print(" ")
    print("Optimizing Policy, beginning with a coin-toss policy ")
    opt.Policy.b = [0,0,0,0,0,0,0,0,0,0,0]
    output = opt.optimizePolicy(2)
    print("Outputs")
    print(str(output))
