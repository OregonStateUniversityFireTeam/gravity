from FireGirl_Landscape import *
from FireGirl_Policy import *
import math
from scipy.optimize import *

class OptimizerDataSet:
    def __init__(self):
        #A list to hold all the landscapes in a data set, whether they represent FireGirl or FireWoman landscapes
        self.landscape_set = []
        
        #A list to hold the net values of each landscape in the data set
        self.landscape_net_values =[]
        
        #A list to hold the "probability weights" of each landscape
        self.landscape_weights = []
        
        #The policy that is controlling each landscape's fire suppression choices
        #This should be set to one of the two child classes of HKBFire_Policy: 
        #  FireGirl_Policy or FireWoman_Policy
        self.Policy = None
        
        #Boundaries for what the parameters can be set to during scipy's optimization routine:
        self.b_bounds = []

        #Flag: Use log(probabilities)  -  If we want to force sums of log(probs), set to True
        #                                 To just multiply probabilities, set to False
        self.USE_LOG_PROB = False

            
    def calcLandscapeWeights(self):
        #Currently, this is a mandatory override in child classes.
        pass

    def calcObjectiveFn(self, b=None):
        #This function contains the optimization objective function. It operates
        #  on the current list of landscapes. If any values for 'b' are passed in,
        #  (most likely by scipy.optimize.fmin_l_bfgs_b(), then they are assigned
        #  to the current FireGirl_Policy object so that subsequent function calls
        #  will use the correct ones.
                
        #The objective function is the sum of each landscape's net value, weighted
        #  by the overall probability of its suppression choices. This probabilty
        #  is simply the suppression decision values from the logistic function
        #  all multiplied together.


        #variable to hold the final value
        obj_fn_val = 0    
        
        # checking for new beta parameters
        if not b == None:
            self.Policy.b = b
      

        # Calculate the weights... these will use the current Policy
        #    rather than whatever policy the landscapes used during simulation
        #    Typically, this will be the multiplied total of the inidividual probabilities
        #    associated with following or not-following the policy
        self.calcLandscapeWeights()
        
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


    def calcObjDerivative(self, b=None):
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


        # list to hold the final values, one per parameter
        d_obj_d_bk = []
        for i in range(len(b)):
            d_obj_d_bk.append(0)


        #iterate over each beta and evaluate the gradient along it
        for beta in range(len(b)):

            #get the total probability for each landscape decision sequence
            self.calcLandscapeWeights()

            #variable to hold the sum of the delta(prob)/prop values
            sum_delta_prob_ = 0

            for l in range(len(self.landscape_set)):

                for i in range(len(self.landscape_set[l].Logbook.log_list)):

                    logistic = FireGirl_Policy.logistic

                    prob = (sup_i)*logistic()

                    sum_delta_prob_ += delta_prob / prob

                d_obj_d_bk[l] += self.landscape_net_values[l] * self.landscape_weights[l] * sum_delta_prob_


        
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
            
            #               arg names:    func                  x0             fprime, args, approx_grad, bounds
            output_policy = fmin_l_bfgs_b(self.calcObjectiveFn, self.Policy.b, None,   [],   True,       self.b_bounds)
            
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
    
   
    
   
class FireGirl_Optimizer(OptimizerDataSet):
    #This class inherits the generic OptimizerDataSet class for use with
    #  the FireGirl model.
    
    def __init__(self):
        
        #A flag for whether or not to include ending landscapes' standing timber
        #   value in the total landscape value
        self.count_standing_timber = True
      
        #Boundaries for what the parameters can be set to during scipy's optimization routine:
        self.b_bounds = []
        #there are 10 parameters, and each has an upper and lower bound. They need
        #   to be in a list of pairs. Right now, they're all being set identically.
        for i in range(10):
            self.b_bounds.append([-10,10])
    
    def createNewDataSet(self, landscape_count, years_per_landscape, policy=None):
        #This function is unique to the FireGirl_Optimizer class:  FireWoman has a 
        #  separate functionality for loading in data.
        
        #This function will create a new dataset in memory in preparation for 
        #   optimizePolicy().
        
        #Check if we need a new policy, or if one was passed in
        if policy == None:
            #no policy passed, so create a new one
            self.Policy = FireGirl_Policy()
        
        #Clear the landscape_set list in case there's old landscapes in it
        self.landscape_set = []
        
        #Create new landscapes and add them to the landscape_set list
        for i in range(landscape_count):
            self.landscape_set.append(FireGirl_Landscape(i, self.Policy))
        
        #Have each landscape create new data for itself. Right now their timber_values 
        #   and fuel_loads are set uniformally to zero
        for ls in self.landscape_set:
            ls.generateNewLandscape()
            #Have each landscape simulate for the given number of years
            ls.doYears(years_per_landscape)
            
        #Finish up by calculating the final values of each landscape
        sumLandscapeValues()
        
    
    def sumLandscapeValues(self):
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
                    
                if not entry.logging_total == None:
                    #adding values from logging
                    net_val += entry.logging_total
                    
            #finished looping over this landscape's logbook entries    
                
            #now, if desired, adding up any remaining land value
            if self.count_standing_timber == True:
                for i in range(43,86):
                    for j in range(43,86):
                        net_val += self.landscape_set[ls].timber_value[i][j]
            
            #before we go on to the next landscape, add this value to the net
            #  value list at the same index as the landscape is in the landscape_set list
            #  
            #note: doing the +1 -1 thing to ensure that a value, rather than a reference, is passed
            self.landscape_net_values[ls] = ( net_val + 1 - 1 )
        
        #all landscapes have had their net values recorded
        
        
    def calcLandscapeWeights(self):
        #Mandatory Override of the parent class function with the same name.
        
        #This function looks through each landscape and sums up the ln() of the
        #  suppression probabilities of each logbook entry. The probability used
        #  is that of having actually made the suppression decision that was made,
        #  so, for instance, a suppress decision when the suppression probability
        #  was 0.60 would yield 0.60, but a let-burn decision would yield 1-p = 0.40
        
        #clear old weights
        self.landscape_weights = []
        
        #a loop variable
        entry_sum = 1
        
        #loop over each landscape
        for ls in range(len(self.landscape_set)):
            
            #adding a new element to landscape_weights for this index
            self.landscape_weights.append(0)
            
            #reset the sum
            if self.USE_LOG_PROB == False:
                entry_sum = 1  #for multiplication, start at 1
            else:
                entry_sum = 0  #for sums of log(probabilities), start at 0
            
            #loop over this landscape's logbook entries
            for entry in self.landscape_set[ls].Logbook.log_list:
                
                #calculate the probability of suppression at this event given 
                #  the current policy, which may or may not be different than
                #  what was used when the landscape was being simulated
                #
                #the Policy object uses the following function signature to update
                #  the values it uses to calculate a suppression probability
                #def setValues(self, windspeed, temp, date, timber_val, timber_ave8, timber_ave24, fuel, fuel_ave8, fuel_ave24)
                #
                #  and this one to evaluate the probability
                #def evaluateSuppressionProbability()
                
                #For Reference:
                #Values held by the logbook entry
                #entry.year
                #entry.date
                #entry.loc
                #entry.temp
                #entry.wind
                #entry.timber
                #entry.timber_ave8
                #entry.timber_ave24
                #entry.fuel
                #entry.fuel_ave8
                #entry.fuel_ave24
                #entry.suppress_prob
                #entry.suppress_decision
                #entry.cells_burned
                #entry.timber_loss
                #entry.logging_total
                #entry.eco1
                #entry.eco2
                #entry.eco3 
                
                #Signature: setValues(self, windspeed, temp, date, timber_val, timber_ave8, timber_ave24, fuel, fuel_ave8, fuel_ave24)
                self.Policy.setValues(entry.wind, entry.temp, entry.date, entry.timber, entry.timber_ave8, entry.timber_ave24,
                                      entry.fuel, entry.fuel_ave8, entry.fuel_ave24)
                # note that Policy.setValues will sanitize it's own inputs (in particular if there are 'None' values present)
                
                
                #here, we're assuming that the Policy object has already loaded
                #  the appropriate parameters elsewhere
                new_prob = self.Policy.evaluateSuppressionProbability()
                #print ("in FG calcLandscapeWeights: new_prob = " + str(new_prob))
                
                # picking the appropriate version of the probabilty:
                if entry.suppress_decision == True:
                    #this fire was suppressed, so use the probability as it stands

                    if self.USE_LOG_PROB == True:
                        #we're using log(prob) calculations, so add the log(new_prob) to the sum
                        entry_sum += math.log(new_prob)
                    else:
                        #we're using straight probability multiplication, so just multiply
                        entry_sum *= new_prob
                else:
                    #this fire was not suppressed, so use 1-p

                    if self.USE_LOG_PROB == True:
                        #we're using log(prob) calculations, so add the log(new_prob) to the sum
                        entry_sum += math.log(1 - new_prob)
                    else:
                        #we're using straight probability multiplication, so just multiply
                        entry_sum *= (1 - new_prob)
                    
            
            #done looping over this landscape's logbook entries
            
            #adding the sum to the appropriate list at the same index as the landscape 
            #   is in the landscape_set list
            #
            #note: doing the +1-1 thing to ensure that a value, rather than a reference, is passed
            self.landscape_weights[ls] = ( entry_sum + 1 - 1 )
        
        
        #Done looping: All landscape weights have been recorded

    def calcObjectiveFn_NOW_IGNORING(self, b=None):
        # Override of the parent function:
        
        #This function contains the optimization objective function. It operates
        #  on the current list of landscapes. If any values for 'b' are passed in,
        #  (most likely by scipy.optimize.fmin_l_bfgs_b(), then they are assigned
        #  to the current FireGirl_Policy object so that subsequent function calls
        #  will use the correct ones.
                
        #The objective function is the sum of each landscape's net value, weighted
        #  by the overall probability of its suppression choices. This probabilty
        #  is simply the suppression decision values from the logistic function
        #  all multiplied together.
        
        #I'm using the ln(prob) in place of prob and summing instead of multiplying
        #  in order to avoid zeroing out the products
        
        #The smaller the probability, the more negative is it's ln() value. Thus
        #  the sum of ln(p) values which are smaller (on average) will have a more
        #  negative value. To weight the landscape values, we want the value of 
        #  a more probable landscape outcome to have a higher weight, and ones
        #  with low probability of occuring to have a lower weight. So if we
        #  divide each landscape's value by the absolute value of it's ln(p) sum, 
        #  we should get this effect nicely. Low probability sums will be larger 
        #  in absolute terms, so using them in the divisor will have the desired
        #  effect.        
        
        obj_fn_val = 0    
        
        # checking for new beta parameters
        if not b == None:
            #sanitization check to make sure enough values are being passed in
            if len(b) >= 10:
                self.Policy.b = b
            else:
                print("Error in FireGirl_Optimizer.calcObjectiveFn(): Input arg 'b' contains < 10 elements. Ignoring the values given.")
        
        
        # First, calculate the final landscape values
        self.sumLandscapeValues()
        print("Landscape values:")
        print(self.landscape_net_values)
        print(" ")
        
        # Second, calculate the weights... these will use the current Policy
        #    rather than whatever policy the landscapes used during simulation
        self.calcLandscapeWeights()
        print("LandscapeWeights:")
        print(self.landscape_weights)
        print(" ")
        
        #a variable to hold the sum of ALL the probability-weighted landscape values
        total_value = 0
        
        #loop over all the values/weights and sum them
        for ls in range(len(self.landscape_set)):
            total_value += self.landscape_net_values[ls] / abs(self.landscape_weights[ls])
        
        #NOTE:
        #any final checks/modifications to total_val can go here:
        obj_fn_val = total_value    
        
        
        return obj_fn_val
    
class FireWoman_Optimizer(OptimizerDataSet):
    #This class inherits from the OptimizerDataSet class and is designed
    #  to interact specifically with FireWoman data.
    
    def __init__(self):
        #Any FireWoman unique class members go here...
        pass
        
    def calcLandscapeWeights(self):
        #This function will loop through all the entries from every fire on every 
        # landscape provided from the FireWoman model. For each fire, the probability
        # that the current policy (regardless of what policy was used at the time) 
        # would suppress the fire is calculated.
        #If the decision was to suppress, the ln() of that probability is used in the next step
        #If the decision was to let-burn, the ln() of 1-p is used in the next step.
        #
        #For each fire event in one landscape's history, the sum is taken of all the ln(p OR 1-p) values
        #This sum is assigned as the weight for this landscape.
        
        pass
        
    def calcObjectiveFn(self, b=None):
        #This function is called by the object.OptimizePolicy function.
        #If no b values are passed, it will use it's self.Policy object to 
        #  re-calculate Landscape weights using the calcLandscapeWeights function
        #If b values are passed, which will be done within scipy's optimization routines,
        #  the landscape weights will use them instead of it's own policy.
        
        #The objective function value is:
        
        # The sum of:
        #    The net-present value of each landscape, 
        #               divided by 
        # the absolute value of that landscape's weight
        
        pass
