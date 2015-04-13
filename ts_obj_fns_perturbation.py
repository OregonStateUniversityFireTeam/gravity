import random, math
from FireGirlOptimizer import *
FGPO = FireGirlPolicyOptimizer()

pathway_count = 20
iginition_count = 50


FGPO.createFireGirlPathways(pathway_count,iginition_count)

beta = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]

obj_fns_total = []
obj_fns_total_pert = []
obj_fns_ave = []
obj_fns_ave_pert = []

deltas_total = []
deltas_ave = []

#iterate over a proliferation of policies
for pw in range(1000):
    
    #generate a new random policy
    for b in range(11):
        beta[b] = random.uniform(-9,9)
    
    #assign the policy
    FGPO.Policy.b = beta
    
    #calculate both objective functions
    FGPO.USE_AVE_PROB = False
    obj_fns_total.append(FGPO.calcObjFn())
    FGPO.USE_AVE_PROB = True
    obj_fns_ave.append(FGPO.calcObjFn())
    
    #perturb the policy
    for b in range(11):
        beta[b] += random.uniform(-1.0,1.0)
    
    #recalculate the objective functions
    FGPO.USE_AVE_PROB = False
    obj_fns_total_pert.append(FGPO.calcObjFn())
    FGPO.USE_AVE_PROB = True
    obj_fns_ave_pert.append(FGPO.calcObjFn())
    
    #compute the deltas
    deltas_total.append(obj_fns_total_pert[pw] - obj_fns_total[pw])
    deltas_ave.append(obj_fns_ave_pert[pw] - obj_fns_ave[pw])
    

    
#print the results to a file
f = open('perturbation_test.txt', 'w')
for pw in range(1000):
    f.write(str(obj_fns_total[pw]) + "," + str(obj_fns_total_pert[pw]) + "," + str(obj_fns_ave[pw]) + "," + str(obj_fns_ave_pert[pw]) + "\n")
    
f.close()