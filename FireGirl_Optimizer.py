from FireGirl_Landscape import *
from FireGirl_Policy import *
import math, scipy, pickle
from scipy.optimize import *

class FireGirlPolicyOptimizer:
    def __init__(self, USING_FIREGIRL_LANDSCAPES=True):
        #A list to hold all the landscapes in a data set, whether they represent FireGirl or
        #    FireWoman landscapes
        self.landscape_set = []
        
        #A list to hold the net values of each landscape in the data set
        self.landscape_net_values =[]
        
        #A list to hold the "probability weights" of each landscape
        self.landscape_weights = []
        
        #Boundaries for what the parameters can be set to during scipy's optimization routine:
        self.b_bounds = []
        if USING_FIREGIRL_LANDSCAPES == True:
            for i in range(11):
                self.b_bounds.append([-10,10])

        #Flag: Use log(probabilities)  -  If we want to force sums of log(probs), set to True
        #                                 To just multiply probabilities, set to False
        self.USE_LOG_PROB = False

        #Flag: Using FireGirl landscapes = True
        #      Using FireWoman landscapes = False
        self.USING_FIREGIRL_LANDSCAPES = USING_FIREGIRL_LANDSCAPES


        #The policy that is controlling each landscape's fire suppression choices
        #This should be set to one of the two child classes of HKBFire_Policy: 
        #  FireGirl_Policy or FireWoman_Policy

        if USING_FIREGIRL_LANDSCAPES == True:
            #FireGirl uses 11 parameters, so set them all to 0 (coin-toss policy)
            self.Policy = FireGirlPolicy(None,0,11)
        else:
            #FireWoman uses ??? parametres, so set them all to 0 (coin-toss policy)
            self.Policy = FireGirlPolicy(None,0,30)


        ##########################################################################################
        #FireGirl-specific flags and data members. These are unused if FireWoman-style landscapes
        #    are being used
        ##########################################################################################

        #A flag for whether or not to include ending landscapes' standing timber
        #   value in the total landscape value
        self.count_standing_timber = False
      


    ##########################
    # Optimization Functions #
    ##########################

    def calcLandscapeWeights(self):
        #This function looks through each fire of a given landscape and applies the current
        #  policy to the features of each one. The resulting 'probability' from the policy 
        #  function is either multiplied or 'log-summed' be the others to produce the final 
        #  weighting value. This is done for every landscape in the landscape_set, and each
        #  weight is assigned to landscape_weights[] at the same index as their landscape in 
        #  the landscape_set list

        #clearing old weights
        self.landscape_weights = []

        #iterating over each landscape and appending each new weigh to the list
        for ls in self.landscape_set:

            #setting the landscape's USE_LOG_PROB flag to match the optimizer's flag
            ls.USE_LOG_PROB = self.USE_LOG_PROB
        
            #setting this landscape's policy to the current one
            ls.assignPolicy(self.Policy)
                
            p = ls.calcTotalProb()

            self.landscape_weights.append(p)

    def calcObjFn(self, b=None):
        #This function contains the optimization objective function. It operates
        #  on the current list of landscapes. If any values for 'b' are passed in,
        #  (most likely by scipy.optimize.fmin_l_bfgs_b(), then they are assigned
        #  to the current HKBFire_Policy object so that subsequent function calls
        #  will use the correct ones.
                
        #The objective function is the sum of each landscape's net value, weighted
        #  by the overall probability of its suppression choices. This probabilty
        #  is simply the suppression decision values from the logistic function
        #  all multiplied together.


        #variable to hold the final value
        obj_fn_val = 0    
        
        # checking for new beta parameters
        if not b == None:
            self.Policy.setParams(b)

        #Note: self.calcLandscapeWeights will assign this policy to each landscape

        # Calculate the weights... these will use the current Policy
        #    rather than whatever policy the landscapes used during simulation
        #    Typically, this will be the multiplied total of the inidividual probabilities
        #    associated with following or not-following the policy
        self.calcLandscapeWeights()

        #Note: self.landscape_net_values is being assigned either in:
        #   1) createFireGirlLandscapes() when those landscapes are first made
        #   2) loadFireGirlLandscapes() when those landscapes are loaded up
        #   3) loadFireWomanLandscapes() when those landscapes are loaded up

        #now assign them to the local list, for ease
        self.landscape_net_values = []
        for ls in self.landscape_set:
            self.landscape_net_values.append(ls.net_value)
        
        #a variable to hold the sum of ALL the probability-weighted landscape values
        total_value = 0
        
        #loop over all the values/weights and sum them
        for ls in range(len(self.landscape_set)):
            total_value += self.landscape_net_values[ls] * self.landscape_weights[ls]
        


        #NOTE:
        #any final checks/modifications to total_val can go here:

        #since scipy fmin... is a minimization routine, return the negative
        obj_fn_val = -1 * total_value    
        
        
        return obj_fn_val

    def calcObjFPrime(self, betas=None):
        #This function returns the gradient of the objective function

        #The scipy documentation describes the fprime arguement as:
        #fprime : callable fprime(x,*args)
        #The gradient of func. If None, then func returns the function value and the 
        #  gradient (f, g = func(x, *args)), unless approx_grad is True in which case func returns only f.

        #The return value should probably just be a list of the derivitive values with respect to each 
        #   b-parameter in the policy

        #  d Obj()/d b_k value is 
        #
        #   Sum over landscapes [ val_l * product over ignitions [ prob_i ] * sum over ignitions [d wrt prob / prob] ]
        #
        #   where d wrt prob =  sup_i * d(logistic(b*f)) + (1 - sup_i)(-1) (d(logistic(b*f)))
        #
        #   and where d(logistic(b*f)) = f_l,i,k * logistic(f_l,i,k * b_k) * (1 - logistic(f_l,i,k * b_k))

        #Assign values to b. I don't think this function will ever be called
        #  outside of the l_bfgs function, but if so, handle it:
        b = None
        if betas == None:
            b = self.Policy.getParams()
        else:
            b = betas

        # list to hold the final values, one per parameter
        d_obj_d_bk = []
        for i in range(len(b)):
            d_obj_d_bk.append(0)


        #iterate over each beta and evaluate the gradient along it
        for beta in range(len(b)):

            #get the total probability for each landscape decision sequence using the 
            #   current policy (which is possibly being varied by l_bfgs, etc...)
            self.calcLandscapeWeights()

            #SEE MATHEMATICS DOCUMENTATION FOR A DETAILED EXPLANATION OF ALL THAT FOLLOWS

            #variable to hold the sum of the delta(prob)/prop values
            sum_delta_prob = 0

            for l in range(len(self.landscape_set)):

                #reset value for this landscape
                sum_delta_prob = 0

                for i in range(self.landscape_set[l].getIgnitionCount()):

                    #making a function handle for ease
                    spare_pol = FireGirlPolicy()
                    logistic = spare_pol.logistic

                    #NOTE: the individual landscapes have already had their policies updated
                    #  to the current one in self.calcLandscapeWeights()

                    #get the suppression choice of this landscape at this ignition
                    choice = self.landscape_set[l].getChoice(i)
                    #and set it to binary
                    sup = 0
                    if choice == True: sup = 1

                    #get the new probability (according to the current policy) of suppressing
                    # this ignition in this landscape
                    prob_pol = self.landscape_set[l].getProb(i)

                    #set the probability of actually doing what we did
                    prob = sup * prob_pol   +   (1-sup)*(1-prob_pol)

                    #checking for unreasonably small probabilities
                    if prob == 0:
                        prob = 0.00001

                    #get the cross product of this landscape at this ignition
                    cross_product = self.landscape_set[l].getCrossProduct(i)

                    #get the feature of this landscape and this ignition for this beta
                    flik = self.landscape_set[l].getFeature(i, beta)


                    delta_lgstc = flik * logistic(cross_product) * (1 - logistic(cross_product))

                    delta_prob = sup * delta_lgstc + (1 - sup)*(-1)*delta_lgstc

                    sum_delta_prob += delta_prob / prob

                
                d_obj_d_bk[beta] += self.landscape_net_values[l] * self.landscape_weights[l] * sum_delta_prob


                #going on to the next landscape

            #going on to the next beta

        #finished with all betas

        # because this is a minimization routine, and the objective function is being flipped, so too
        #should be the derivatives
        for b in range(len(d_obj_d_bk)):
            d_obj_d_bk[b] *= -1


        # And Finally, return the list
        return scipy.array(d_obj_d_bk)

        
    def optimizePolicy(self, iterations=1, acceptance_threshold=None):
        #This function will work through the given number of gradient descent 
        #  iterations using the current set of landscapes for its data set.
        #It returns a list containing two elements
        #  -The first is a list of the policy parameters used in
        #  each iteration
        #  -The second is a list of the optimized objective function value 
        #  for each iteration

        
        # a list to hold each iteration's final objective function value
        obj_vals = []
        # a list to hold the parameters returned by each iteration
        param_sets = []
        
        #record the first 'optimization value' which is really just a placeholder 
        #  to keep indices even
        obj_vals.append(-9999999)
        #record the first parameter set
        param_sets.append(self.Policy.b)
        
        for iter in range(iterations):
            #tell scipy to optimize our objective function (calcObjectiveFn())
            #  given a certain set of parameters...
            
            #running the scipy gradient descent method
            #signature is:
        	#scipy.optimize.fmin_l_bfgs_b(func, x0, fprime=None, args=(), approx_grad=0, bounds=None, m=10, 
            #                             factr=10000000.0, pgtol=1e-05, epsilon=1e-08, iprint=-1, maxfun=15000,
            #                             maxiter=15000, disp=None, callback=None)
        	# func is a function name, at is referenceing the objective function that it will use
        	# x0 is the starting parameters that fmin_l_bfgs_b() will use
        	# fprime="None" is telling fmin...() that we are not passing in a function to calculate derivitave values
        	# args=() is asking for any input arguments needed for the objective function, other than the beta parameters
        	# approx_grad is telling fmin...() to approximate it's own derivatives, or to use some other gradient
        	# bounds should be a list of upper and lower bound pairs. See scipy.optimize.fmin_l_bfgs_b documentation.
        	# The rest of the arguments are left as defaults.
            
            #converting to numpy arrays
            x0 = scipy.array(self.Policy.b)

            #               arg names:    func            x0  fprime,               args, approx_grad, bounds
            output_policy = fmin_l_bfgs_b(self.calcObjFn, x0, self.calcObjFPrime,   [],   False,       self.b_bounds)
            
            #the output of fmin_l_bfgs_b() has the following structure: [x, f, d], where:
            #   x : array_like
            #       Estimated position of the minimum.
            #   f : float
            #       Value of func at the minimum.
            #   d : dict
            #       Information dictionary.
            
            
            #record the new parameter set
            param_sets.append(output_policy[0])
            
            #record the final objective function value
            obj_vals.append(output_policy[1])
            
            #take the new parameter set and assign them back to the policy
            self.Policy.b = output_policy[0]
            
            #run the next iteration
            
            
        #Iterations are Finished, so prepare the return value
        ret_val = [param_sets, obj_vals]
        
        return ret_val
    

    ###############################
    # FireGirl-specific Functions #
    ###############################
    def createFireGirlLandscapes(self, landscape_count, years, policy=None):
        #This function creates a new set of FireGirl-style landscapes (deleting all current
        #    landscape data)

       
        #Check if we need a new policy, or if one was passed in
        if policy == None:
            #no policy passed, so create a new one
            self.Policy = FireGirlPolicy(None,0,11)
        
        #Clear the landscape_set list in case there's old landscapes in it
        self.landscape_set = []
        
        #Create new landscapes and add them to the landscape_set list
        for i in range(landscape_count):
            self.landscape_set.append(FireGirlLandscape(i, self.Policy))
        
        #Have each landscape create new data for itself. Right now their timber_values 
        #   and fuel_loads are set uniformally to zero
        for ls in self.landscape_set:

            #have each landscape create timber/fuel data for itself
            print("Creating landscape " + str(ls.ID_number))
            ls.generateNewLandscape()

            #Have each landscape simulate for the given number of years
            ls.doYears(years)

            #and after all years are finished, have each landscape calculate its net value
            ls.updateNetValue()
        
        #DEPRECATED
        #Finish up by calculating the final values of each landscape
        #print("Summing Landscape Values")
        #self.sumLandscapeValues()


    def DEPRECATINGsumLandscapeValues(self):
        #THIS FUNCTION IS NOW HANDLED WITHIN THE LANDSCAPE OBJECTS THEMSELVES, VIA
        # THE landscape.updateNetValue() MEHTOD.


        #This function is unique to the FireGirl model, which does not calculate
        # it's own interal net-present-value like FireWoman does. It is really just
        # a sub-function of the calcObjectiveFn() function.
        
        #This function looks through each landscape in the dataset and sums its
        #  total net value, and then records them in the self.landscape_net_values list
        
        #loop-variable to hold one landscape's net value
        net_val = 0
        
        #erasing previous net-values
        self.landscape_net_values = []
        
        #looping through each landscape
        for ls in range(len(self.landscape_set)):
            
            #adding new element to landscape_net_values for this index
            self.landscape_net_values.append(0)
            
            #reseting net_val
            net_val = 0
            
            #looping through each of this landscape's logbook entries
            for entry in self.landscape_set[ls].Logbook.log_list:
                
                if not entry.timber_loss == None:
                    #subtracting timber losses from crown fires
                    net_val -= entry.timber_loss
                
                #these are never reported...
                if not entry.logging_total == None:
                    #adding values from logging
                    net_val += entry.logging_total
                    
            #finished looping over this landscape's logbook entries    
                
            #now, if desired, adding up any remaining land value
            if self.count_standing_timber == True:
                for i in range(43,86):
                    for j in range(43,86):
                        net_val += self.landscape_set[ls].timber_value[i][j]


            #Add Up logging totals, since they are not reported above
            net_val += self.landscape_set[ls].getHarvestTotal()
            net_val -= self.landscape_set[ls].getSuppressionTotal()


            #before we go on to the next landscape, add this value to the net
            #  value list at the same index as the landscape is in the landscape_set list
            #  
            #note: doing the +1 -1 thing to ensure that a value, rather than a reference, is passed
            self.landscape_net_values[ls] = ( net_val + 1 - 1 )
        
        #all landscapes have had their net values recorded



    ###################
    # Other Functions #
    ###################
    def saveFireGirlLandscapes(self, filename):
        output = open(filename, 'wb')

        # Pickle dictionary using default protocol 0.
        pickle.dump(self.landscape_set, output)

        output.close()

    def loadFireGirlLandscapes(self, filename):
        #This function loads a saved set of FireGirl Landscapes

        pkl_file = open(filename, 'rb')

        self.landscape_set = []
        self.landscape_set = pickle.load(pkl_file)

        pkl_file.close()

        #and do the post-processing
        
        #force each landscape to update their values
        for ls in self.landscape_set:
            ls.updateNetValue()

    def loadFireWomanLandscapes(self, filename):
        #This function loads a saved set of FireWoman Landscapes

        #REMINDER: this function needs to assign values to self.landscape_net_values

        pass

    def setPolicy(self, policy):
        #take the policy given and give it to every landscape in the current set.
        self.Policy = policy
        for ls in self.landscape_set:
            ls.Policy = self.Policy


    def resetPolicy(self):
        #This function resets the policy to a 50/50 coin-toss
        pass
    def loadPolicy(self, filename):
        #This function loads a saved policy and assigns it to this optimization object
        pass
    