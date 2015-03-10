from FireGirl_Optimizer import *
FGPO = FireGirlPolicyOptimizer()
FGPO.createFireGirlLandscapes(10,10)
new_pol_params=FGPO.optimizePolicy()
print(new_pol_params)