import math

class FireGirlPolicy:
    #This is a the base class for both the FireGirl_Policy and FireWoman_Policy classes
    #Note: It is intended that this class will not be used on it's own, but rather only
    #  in it's inherited forms.

    #If a list of parameters is passed in, the local b values will be set accordingly,
    #  and SETALL and COUNT will be ignored.

    #If SETALL is set and params==None, then all parameters will be set to the given value

    #COUNT is the total number of parameters to set, so assuming SETALL is used (no param list)
    #  then the SETALL value will be assigned this many times
    
    def __init__(self, params=None, SETALL=None, COUNT=None):
        # a list of features, designed to be set repeatedly for each fire event
        self.features = []
        
        # a list of this policy's parameters.
        self.b = []
        
        #Checking for initialization values, and assigning them as appropriate
        if not params == None:
            self.b = params
        else:
            if not COUNT == None:
                if not SETALL == None:
                    for i in range(COUNT):
                        self.b.append(SETALL)


    def setParams(self, parameter_list):
        self.b = parameter_list

    def setFeatures(self, feature_list):
        self.features = feature_list

    def getParams(self):
        return self.b

    def crossProduct(self, feature_list=None):
        #This function will return the crossproduct between each feature and it's 
        #  corresponding parameter beta value 

        #if no feature list is passed, just use what the Policy already has
        #otherwise, use what's been given.
        if not feature_list == None:
            self.features = feature_list
        
        cp = 0

        for i in range(len(self.features)):
            cp += self.features[i] * self.b[i]
            
        return cp

    def logistic(self, value):
        #This function calculates the simple logistic function value of the input
        return (  1 / (1 + math.exp(-value))  )   
    
    def calcProb(self, feature_list):
        self.features = feature_list
        cp = self.crossProduct()
        prob = self.logistic(cp)
        return prob

    ## DEPRECATING ##
    def evaluateSuppressionProbability(self):
        cp = self.crossProduct()
        return self.logistic(cp)     
        
   
class FireGirlPolicy_DEPRECATING(FireGirlPolicy):
    #This class contains all the code that actually interacts with the policy
    #  function, it's parameters, etc...
    #It inherits from a generic fire policy class, HKBFire_Policy
    
    ### FEATURE VALUES ###
    #  (as per FireGirl_Landscape.py)
    # For the suppression rule, the following are the features being used:
    #
    #  Wind Speed - one value per day/fire
    #  Temperature - one value per day/fire
    #  Date of Ignition
    #  (Date of Ignition)^2
    #  Timber Value at ignition point
    #  Average Timber Value adjacent 8
    #  Average Timber Value adjacent 24
    #  Fuel Load at ignition point
    #  Average Fuel Load adjacent 8
    #  Average Fuel Load adjacent 24
        
    def __init__(self):
        self.windspeed = 0.0
        self.temperature = 0.0
        self.date = 0.0
        self.date2 = 0.0
        self.timber_val = 0.0
        self.timber_ave8 = 0.0
        self.timber_ave24 = 0.0
        self.fuel = 0.0
        self.fuel_ave8 = 0.0
        self.fuel_ave24 = 0.0
        
        #overwriting what was already set in the parent class __init__ function
        self.b = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
        
      
    def crossProduct(self):
        #OVERRIDING parent class function of the same name.  This child class
        #  does not use the self.features list, but instead uses the individual 
        #  values, since there are only 10 of them.
        
        cp =  ( self.windspeed    * self.b[0]  +
                self.temperature  * self.b[1]  +
                self.date         * self.b[2]  +
                self.date2        * self.b[3]  +
                self.timber_val   * self.b[4]  +
                self.timber_ave8  * self.b[5]  +
                self.timber_ave24 * self.b[6]  +
                self.fuel         * self.b[7]  +
                self.fuel_ave8    * self.b[8]  +
                self.fuel_ave24   * self.b[9]    )
        
        return cp
    
    def setValues(self, windspeed, temp, date, timber_val, timber_ave8, timber_ave24, fuel, fuel_ave8, fuel_ave24):
        #This function just sets the input values. It can be done piecemeal too.
        
        #setting 0's in case there are "None" values that have been passed in
        #  just avoiding all the "else" statements that would otherwise be needed
        #  below.
        self.windspeed = 0
        self.temperature = 0
        self.date = 0
        self.date2 = 0
        self.timber_val = 0
        self.timber_ave8 = 0
        self.timber_ave24 = 0
        self.fuel = 0
        self.fuel_ave8 = 0
        self.fuel_ave24 = 0
        
        #now using the input arguments to set the policy's working numbers.
        #These only affect it's suppression probability calculations.
        if not windspeed == None:   self.windspeed = windspeed
        if not temp == None:        self.temperature = temp
        if not date == None:
                                    self.date = date
                                    self.date2 = date * date
        if not timber_val == None:  self.timber_val = timber_val
        if not timber_ave8 == None: self.timber_ave8 = timber_ave8
        if not timber_ave24 == None:self.timber_ave24 = timber_ave24
        if not fuel == None:        self.fuel = fuel
        if not fuel_ave8 == None:   self.fuel_ave8 = fuel_ave8
        if not fuel_ave24 == None:  self.fuel_ave24 = fuel_ave24
        
    
    def loadParameters(self, filename):
        #This function loads the 10 policy parameters from a file.
        #The file format is as follows:
        #
        #All ten values should be on one line, deliminated by commas
        #The function will ignore everything after the first line.
        #
        #The function returns true if it succeeded to load files, and false if
        # it did not.
        
        file = open(filename, 'r')
        input_string = file.read()
        file.close()
        
        input_vals = input_string.split(",")
        if len(input_vals) < 10:
            print("File Read Error: Too few policy parameters in file " + filename)
            return False
        else:
            for i in range(10):
                #converting the string values into floats
                self.b[i] = float(input_vals[i])
                
                #sanitizing according to max and min constraints
                if self.b[i] > self.b_max: self.b[i] = self.b_max
                if self.b[i] < self.b_min: self.b[i] = self.b_min
        
        return True
        
    def saveParameters(self, filename):
        #This function writes the current parameter list to a file.
        
        param_string = ""
        for i in range(9):
            param_string = param_string + str(self.b[i]) + ","
        param_string = param_string + str(self.b[9]) #so as not to append a final comma
        
        file = open(filename, "w")
        file.write(param_string)
        file.close()
    
    
class FireWoman_Policy:
    #This class contains all the code that actually interacts with the policy
    #  function, it's parameters, etc...
    #It inherits from a generic fire policy class, HKBFire_Policy
    
    def __init__(self):
    
        #Child classes add (or override) their own members as well
        
        #No additional members, at the moment...
        pass

    #Other FireWoman-specific functions need to go here:
    
    #def (A function to load in parameter values)
    #def (A function to directly set the feature values, if needed)
    

   