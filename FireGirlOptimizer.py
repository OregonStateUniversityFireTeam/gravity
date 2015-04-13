from FireGirlPathway import *
from FireGirlPolicy import *
import math, scipy, pickle
from scipy.optimize import *

class FireGirlPolicyOptimizer:
    def __init__(self, USING_FIREGIRL_PATHWAYS=True):
        #A list to hold all the pathways in a data set, whether they represent FireGirl or
        #    FireWoman pathways
        self.pathway_set = []
        
        #A list to hold the net values of each pathway in the data set
        self.pathway_net_values =[]
        
        #A list to hold the "probability weights" of each pathway
        self.pathway_weights = []
        
        #Boundaries for what the parameters can be set to during scipy's optimization routine:
        self.b_bounds = []
        if USING_FIREGIRL_PATHWAYS == True:
            for i in range(11):
                self.b_bounds.append([-10,10])

        #Flag: Use log(probabilities)  -  If we want to force sums of log(probs), set to True
        #                                 To just multiply probabilities, set to False
        self.USE_LOG_PROB = False
        
        #Flag: Use average probability instead of total probability on the pathway weight
        #   calculations
        self.USE_AVE_PROB = False

        #Flag: Using FireGirl pathways = True
        #      Using FireWoman pathways = False
        self.USING_FIREGIRL_PATHWAYS = USING_FIREGIRL_PATHWAYS


        #The policy that is controlling each pathway's fire suppression choices
        #This should be set to one of the two child classes of HKBFire_Policy: 
        #  FireGirl_Policy or FireWoman_Policy

        if USING_FIREGIRL_PATHWAYS == True:
            #FireGirl uses 11 parameters, so set them all to 0 (coin-toss policy)
            self.Policy = FireGirlPolicy(None,0.0,11)
        else:
            #FireWoman uses ??? parametres, so set them all to 0 (coin-toss policy)
            self.Policy = FireGirlPolicy(None,0.0,30)


        ##########################################################################################
        #FireGirl-specific flags and data members. These are unused if FireWoman-style pathways
        #    are being used
        ##########################################################################################

        #A flag for whether or not to include ending pathways' standing timber
        #   value in the total pathway value
        self.count_standing_timber = False
      


    ##########################
    # Optimization Functions #
    ##########################

    def calcPathwayWeights(self, USE_SELF_POLICY=True):
        #This function looks through each fire of a given pathway and applies the current
        #  policy to the features of each one. The resulting 'probability' from the policy 
        #  function is either multiplied or 'log-summed' be the others to produce the final 
        #  weighting value. This is done for every pathway in the pathway_set, and each
        #  weight is assigned to pathway_weights[] at the same index as their pathway in 
        #  the pathway_set list

        #clearing old weights
        self.pathway_weights = []

        #iterating over each pathway and appending each new weigh to the list
        for pw in self.pathway_set:

            #setting the pathway's USE_LOG_PROB flag to match the optimizer's flag
            pw.USE_LOG_PROB = self.USE_LOG_PROB
        
            #setting this pathway's policy to the current one
            if USE_SELF_POLICY:
                pw.assignPolicy(self.Policy)
            else:
                #setting this to false indicates that the pathways have their own policies
                # (possibly applied elsewhere) and that they should use them, instead of
                # taking the optimizer's current policy. Mostly used for testing
                pass
            
            #pw.DEBUG = True
            p = 0.0
            if self.USE_AVE_PROB:
                #TESTING - USING Average Probability instead of total probability
                p = pw.calcAveProb()
            #pw.DEBUG = False
            else:
                p = pw.calcTotalProb()
            
            self.pathway_weights.append(p)

    def calcObjFn(self, b=None):
        #This function contains the optimization objective function. It operates
        #  on the current list of pathways. If any values for 'b' are passed in,
        #  (most likely by scipy.optimize.fmin_l_bfgs_b(), then they are assigned
        #  to the current HKBFire_Policy object so that subsequent function calls
        #  will use the correct ones.
                
        #The objective function is the sum of each pathway's net value, weighted
        #  by the overall probability of its suppression choices. This probabilty
        #  is simply the suppression decision values from the logistic function
        #  all multiplied together.


        #variable to hold the final value
        obj_fn_val = 0    
        
        # checking for new beta parameters
        if not b == None:
            self.Policy.setParams(b)

        #Note: self.calcPathwayWeights will assign this policy to each pathway

        # Calculate the weights... these will use the current Policy
        #    rather than whatever policy the pathways used during simulation
        #    Typically, this will be the multiplied total of the inidividual probabilities
        #    associated with following or not-following the policy
        self.calcPathwayWeights()

        #Note: self.pathway_net_values is being assigned either in:
        #   1) createFireGirlPathways() when those pathways are first made
        #   2) loadFireGirlPathways() when those pathways are loaded up
        #   3) loadFireWomanPathways() when those pathways are loaded up

        #now assign them to the local list, for ease
        self.pathway_net_values = []
        for pw in self.pathway_set:
            self.pathway_net_values.append(pw.net_value)
        
        #a variable to hold the sum of ALL the probability-weighted pathway values
        total_value = 0
        
        #loop over all the values/weights and sum them
        for pw in range(len(self.pathway_set)):
            total_value += self.pathway_net_values[pw] * self.pathway_weights[pw]
        


        #NOTE:
        #any final checks/modifications to total_val can go here:

        #since scipy fmin... is a minimization routine, return the negative
        obj_fn_val = -1 * total_value    
        
        
        return obj_fn_val

    def FP_delta_prob(self, beta, pw, ign):
        #this function calculates the inner "delta_prob" value for each calculation of the derivitive.
        # caclObjFPrime() loops over it repeatedly, and passes in which parameter (beta), pathway (pw) and
        # ignition (ign) to calculate value, which is then summed in caclObjFPrime()
        
        
        #making a function handle for ease within the loop
        spare_pol = FireGirlPolicy()
        logistic = spare_pol.logistic
        
        #NOTE: the individual pathways have already had their policies updated
        #  to the current one in self.calcPathwayWeights()

        #get the suppression choice of this pathway at this ignition
        choice = self.pathway_set[pw].getChoice(ign)
        #and set it to binary
        sup = 0
        if choice == True: sup = 1

        #get the new probability (according to the current policy) of suppressing
        # this ignition in this pathway
        prob_pol = self.pathway_set[pw].getProb(ign)

        #set the probability of actually doing what we did
        prob = sup * prob_pol   +   (1-sup)*(1-prob_pol)

        #checking for unreasonably small probabilities
        if prob == 0:
            prob = 0.00001

        #get the cross product of this pathway at this ignition
        cross_product = self.pathway_set[pw].getCrossProduct(ign)

        #get the feature of this pathway and this ignition for this beta
        flik = self.pathway_set[pw].getFeature(ign, beta)


        delta_lgstc = flik * logistic(cross_product) * (1.0 - logistic(cross_product))

        delta_prob = sup * delta_lgstc + (1 - sup)*(-1)*delta_lgstc
        
        return delta_prob

        
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
        #   Sum over pathways [ val_l * product over ignitions [ prob_i ] * sum over ignitions [d wrt prob / prob] ]
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
            
        #get the weight (total or ave) for each pathway decision sequence using the 
        #   current policy (which is possibly being varied by l_bfgs, etc...)
        self.calcPathwayWeights()

        #making a function handle for ease within the loop
        spare_pol = FireGirlPolicy()
        logistic = spare_pol.logistic
        
        #iterate over each beta and evaluate the gradient along it
        for beta in range(len(b)):

            #SEE MATHEMATICS DOCUMENTATION FOR A DETAILED EXPLANATION OF ALL THAT FOLLOWS

            #variable to hold the sum of the delta(prob)/prop values
            sum_delta_prob = 0

            for pw in range(len(self.pathway_set)):

                #reset value for this pathway
                sum_delta_prob = 0

                for i in range(self.pathway_set[pw].getIgnitionCount()):

                    #set the probability of actually doing what we did
                    prob = sup * prob_pol   +   (1-sup)*(1-prob_pol)

                    #checking for unreasonably small probabilities
                    if prob == 0:
                        prob = 0.00001


                    delta_prob = self.FP_delta_prob(beta, pw, i)
                    
                    if self.USE_AVE_PROB:
                        sum_delta_prob += delta_prob
                    else:
                        sum_delta_prob += delta_prob / prob

                
                #finished adding up sum_delta_prob for all the ignitions in this pathway, so
                # calculate the d/dx value:
                
                if self.USE_AVE_PROB:
                    invI = (1.0 / self.pathway_set[pw].getIgnitionCount())
                    d_obj_d_bk[beta] += self.pathway_net_values[pw] * invI * sum_delta_prob
                else:
                    d_obj_d_bk[beta] += self.pathway_net_values[pw] * self.pathway_weights[pw] * sum_delta_prob
                    
                    

                #going on to the next pathway

            #going on to the next beta

        #finished with all betas

        # because this is a minimization routine, and the objective function is being flipped, so too
        #should be the derivatives
        for b in range(len(d_obj_d_bk)):
            #d_obj_d_bk[b] *= -1
            d_obj_d_bk[b] *= -1


        # And Finally, return the list
        return scipy.array(d_obj_d_bk)

       
    def optimizePolicy(self, iterations=1, acceptance_threshold=None):
        #This function will work through the given number of gradient descent 
        #  iterations using the current set of pathways for its data set.
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
        obj_vals.append(self.calcObjFn())
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
            for i in range(len(output_policy[0])):
                self.Policy.b[i] = output_policy[0][i] + 1.0 - 1.0

            #self.Policy.b = output_policy[0]
            
            #debugging check
            #print("output policy is: " + str(output_policy[0]))
            #print("after assigning it to self.Policy.b, ...b is: ")
            #print(str(self.Policy.b))
            
            #run the next iteration
            
            
        #Iterations are Finished, so prepare the return value
        ret_val = [param_sets, obj_vals]
        
        return ret_val
    

    def printOptOutput(self, output):
        #takes the outputs from the optimize() function and prints them in a nicer way
        params = output[0]
        obj_vals = output[1]
        
        print("         ObjFn Val,     Params.....")
        print("                        CONS   date    date2    temp   wind   timb   timb8  timb24  fuel  fuel8  fuel24")
        for v in range(len(obj_vals)):
            if v == 0:
                print("before: "),
            else:
                print("after:  "),
            print(str(round(obj_vals[v],2)) + "  "),
            
            for p in range(len(params[v])):
                print(" " + str(round(params[v][p],3))),
            
            print("") #to end the line
                
            
            
    
    ###############################
    # FireGirl-specific Functions #
    ###############################
    def createFireGirlPathways(self, pathway_count, years, start_at_ID=0, policy=None):
        #This function creates a new set of FireGirl-style pathways (deleting all current
        #    pathway data)
        
        #Check if we need a new policy, or if one was passed in
        if policy == None:
            #no policy passed, so create a new one
            self.Policy = FireGirlPolicy(None,0,11)
        else:
            #one was passed, so set it to the current one.
            self.Policy = policy
        
        #Clear the pathway_set list in case there's old pathways in it
        self.pathway_set = []
        
        #Create new pathways and add them to the pathway_set list
        for i in range(start_at_ID, start_at_ID + pathway_count):
            self.pathway_set.append(FireGirlPathway(i, policy))
        
        #Have each pathway create new data for itself. Right now their timber_values 
        #   and fuel_loads are set uniformally to zero
        print("Creating pathway "),  #the comma indicates to python not to end the line
        for pw in self.pathway_set:

            #have each pathway create timber/fuel data for itself
            print(str(pw.ID_number) + ","), #the comma indicates to python not to end the line
            pw.generateNewPathway()

            #Have each pathway simulate for the given number of years
            pw.doYears(years)

            #and after all years are finished, have each pathway calculate its net value
            pw.updateNetValue()
        
        #end the print line
        print(" ")
        
        #DEPRECATED
        #Finish up by calculating the final values of each pathway
        #print("Summing pathway Values")
        #self.sumPathwayValues()


    ###################
    # Other Functions #
    ###################
    def saveFireGirlPathways(self, filename):
        output = open(filename, 'wb')

        # Pickle dictionary using default protocol 0.
        pickle.dump(self.pathway_set, output)

        output.close()

    def loadFireGirlPathways(self, filename):
        #This function loads a saved set of FireGirl pathways

        pkl_file = open(filename, 'rb')

        self.pathway_set = []
        self.pathway_set = pickle.load(pkl_file)

        pkl_file.close()

        #and do the post-processing
        
        #force each pathway to update their values
        for ls in self.pathway_set:
            ls.updateNetValue()

    def loadFireWomanPathways(self, filename):
        #This function loads a saved set of FireWoman Pathways

        #REMINDER: this function needs to assign values to self.pathway_net_values

        pass

    def setPolicy(self, policy):
        #take the policy given and give it to every pathway in the current set.
        self.Policy = policy
        for ls in self.pathway_set:
            ls.assignPolicy(self.Policy)

    def resetPolicy(self):
        #This function resets the policy to a 50/50 coin-toss
        pass

    def loadPolicy(self, filename):
        #This function loads a saved policy and assigns it to this optimization object
        pass
    