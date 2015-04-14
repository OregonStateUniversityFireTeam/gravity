import random, math
from FireGirlOptimizer import *
FGPO = FireGirlPolicyOptimizer()

pathway_count = 20
iginition_count = 50


FGPO.createFireGirlPathways(pathway_count,iginition_count)

obj_fns_total = []
obj_fns_total_pert = []
obj_fns_ave = []
obj_fns_ave_pert = []


#get an optimal policy
results = FGPO.optimizePolicy()

#save those betas
pol_optim = []

for i in range(len(FGPO.Policy.b)):
    pol_optim.append(FGPO.Policy.b[i] + 1.0 - 1.0)

    
#perturb the policy many times and record the changes
for i in range(1000):
    
    #calculate both objective functions
    FGPO.USE_AVE_PROB = False
    obj_fns_total.append(FGPO.calcObjFn())
    FGPO.USE_AVE_PROB = True
    obj_fns_ave.append(FGPO.calcObjFn())
    
    #perturb the optimal policy
    for j in range(11):
        FGPO.Policy.b[j] = pol_optim[j] + random.uniform(-0.1,0.1)
    
    #recalculate the objective functions
    FGPO.USE_AVE_PROB = False
    obj_fns_total_pert.append(FGPO.calcObjFn())
    FGPO.USE_AVE_PROB = True
    obj_fns_ave_pert.append(FGPO.calcObjFn())    

    
#print the results to a file
f = open('perturbation_test.txt', 'w')
for pw in range(1000):
    f.write(str(obj_fns_total[pw]) + "," + str(obj_fns_total_pert[pw]) + "," + str(obj_fns_ave[pw]) + "," + str(obj_fns_ave_pert[pw]) + "\n")
    
f.close()