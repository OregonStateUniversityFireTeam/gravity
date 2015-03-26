from FireGirl_Optimizer import *
from FireGirl_Landscape import *
from FireGirl_Policy import *
from FireGirl_Landscape_Logbook import *

#without initializing a policy, these will each have an all-zero (coin-toss) policy
ls0 = FireGirlLandscape(0)
ls1 = FireGirlLandscape(1)
ls2 = FireGirlLandscape(2)


#setting ignition records manually

# "correct" decision 1
ig1a = FireGirlIgnitionRecord()
ig1a.features = [1,100,0,0,0,0,0,0,0,0,0]
ig1a.policy_prob = 0.5
ig1a.policy_choice = True
#outcomes are in the form [timber_loss, cells_burned, sup_cost, end_time]
ig1a.outcomes = [0,0,0,0]
ig1a.year = 0
ig1a.burn_time = 0
ig1a.location = [0,0]

# "incorrect" decision 1
ig1b = FireGirlIgnitionRecord()
ig1b.features = [1,100,0,0,0,0,0,0,0,0,0]
ig1b.policy_prob = 0.5
ig1b.policy_choice = False
#outcomes are in the form [timber_loss, cells_burned, sup_cost, end_time]
ig1b.outcomes = [0,0,10000,0]
ig1b.year = 0
ig1b.burn_time = 0
ig1b.location = [0,0]

# "correct" decision 2
ig2a = FireGirlIgnitionRecord()
ig2a.features = [1,-100,0,0,0,0,0,0,0,0,0]
ig2a.policy_prob = 0.5
ig2a.policy_choice = True
#outcomes are in the form [timber_loss, cells_burned, sup_cost, end_time]
ig2a.outcomes = [0,0,0,0]
ig2a.year = 0
ig2a.burn_time = 0
ig2a.location = [0,0]

# "incorrect" decision 2
ig2b = FireGirlIgnitionRecord()
ig2b.features = [1,-100,0,0,0,0,0,0,0,0,0]
ig2b.policy_prob = 0.5
ig2b.policy_choice = False
#outcomes are in the form [timber_loss, cells_burned, sup_cost, end_time]
ig2b.outcomes = [0,0,10000,0]
ig2b.year = 0
ig2b.burn_time = 0
ig2b.location = [0,0]



#setting landscape results manually

ls0.year = 0
ls0.FireLog.append(...)
#instead of calling ls.updateNetValue() to have it calculate anything, I'm just
# accessing the .net_value member directly
ls0.net_value = 0
