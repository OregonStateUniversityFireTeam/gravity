##########################################################################################################
#
#  Test, as per emails between HKB and Dr. Dietterich on 4-14-15
#
#1.	Generate a set of pathways (100s) using a coin-toss policy
#2.	Calculate the optimal policy using my surrogate obj fn (though if I could, both would be far better)
#3.	Create a large set of perturbations of that optimal policy
#4.	Re-generate a new set of pathways, each using one of the perturbed policies to make its choices
#5.	Re-generate a new set of pathways using the optimal policy from step 3
#6.	Compare the objective function values of each of the pathways generated using perturbed policies to 
#       the objective function values of the pathways generated under the optimal policy
#7.	Assuming that the differences between obj fn values from perturbed-policy pathway sets are distributed
#       normally about their mean, compute confidence intervals indicating:
#   a.	With 95% confidence, the mean of the differences between the final objective function values of
#       perturbed policy-pathways from the optimal-policy pathways is between A and B
##########################################################################################################

### NOTES ######################################################
#  This test is re-using the same set of starting landscape snap-shots for each pathway,
#    both in the initial set, and in all subsequent sets. 
################################################################


import random, math
from FireGirlOptimizer import *
FGPO = FireGirlPolicyOptimizer()

pathway_count = 20
iginition_count = 100

### STEP 1 ######################################################
#	Generate a set of pathways (100s) using a coin-toss policy

FGPO.createFireGirlPathways(pathway_count,iginition_count)


### STEP 2 ######################################################
#   Calculate the optimal policy using my surrogate obj fn (though if I could, both would be far better)

FGPO.USE_AVE_PROB = True
results = FGPO.optimizePolicy()


### STEP 3 ######################################################
#	Create a large set of perturbations of that optimal policy

#copy the values of the optimal policy
pol_optim = []
for i in range(11):
    pol_optim.append(FGPO.Policy.b[i] + 1.0 - 1.0)

pert_pols = []
for i in range(11):
    #make new copies of the optimal policy
    pol_copy1 = []
    pol_copy2 = []
    for j in range(11):
        pol_copy1.append(pol_optim[j] + 1.0 - 1.0)
        pol_copy2.append(pol_optim[j] + 1.0 - 1.0)
    
    #perturb the copied policies at index i
    pol_copy1[i] += 0.5
    pol_copy2[i] -= 0.5
    
    #add the perturbed copies to the list
    pert_pols.append(pol_copy1)
    pert_pols.append(pol_copy2)
    

### STEP 4 ######################################################
#   Re-generate a new set of pathways, each using one of the perturbed policies to make its choices 

#lists to hold final objective function values
pert_pathways_objfn_total = []
pert_pathways_objfn_ave = []

#loop over each perturbed policy
for p in pert_pols:
    #set the current policy to this perturbed policy
    FGPO.Policy.b = p
    
    #generate a new pathway set
    FGPO.createFireGirlPathways(pathway_count,iginition_count)
    
    #calculate and save the objective function values of these pathways
    FGPO.USE_AVE_PROB = False
    pert_pathways_objfn_total.append(FGPO.calcObjFn())
    FGPO.USE_AVE_PROB = True
    pert_pathways_objfn_ave.append(FGPO.calcObjFn())

    
### STEP 5 ######################################################
#   Re-generate a new set of pathways using the optimal policy from step 3

#set the current policy to the optimal policy again
FGPO.Policy.b = pol_optim

#generate a new set of pathways using this set
FGPO.createFireGirlPathways(pathway_count,iginition_count)

#record the objective function values
FGPO.USE_AVE_PROB = False
opt_pathway_objfn_total = FGPO.calcObjFn()
FGPO.USE_AVE_PROB = True
opt_pathway_objfn_ave = FGPO.calcObjFn()


### STEP 6 ######################################################
#  	Compare the objective function values of each of the pathways generated using perturbed policies to 
#       the objective function values of the pathways generated under the optimal policy

