class FireGirlIgnitionRecord:
    #This class holds the salient information from any igition, either in FireGirl or
    #  in FireWoman landscapes.

    #self.features is a list of feature values known at the beginning of each ignition
    #   event. This should only contain information that a fire manager would know at 
    #   the time of ignition, and on which they could base their suppression decisions.

    #self.policy_prob holds the probability of suppresion given by a FireGirlPolicy object.

    #self.policy_choice is a boolean flag which records True if the fire was suppressed and
    #   False if the fire was not suppressed.

    #self.outcomes is a list of any information about the results of the fire, mostly intended
    #   for post hoc analysis of the program.

    #self.feature_labels is an optional list of strings describing what each value in 
    #   self.features means.

    #self.outcome_labels is an optional list of strings describing what each value in 
    #   self.outcomes means.

    def __init__(self):
        self.features = []
        self.policy_prob = 1
        self.policy_choice = False
        self.outcomes = []
        self.feature_labels = []
        self.outcome_labels = []
        self.year = 0
        self.burn_time = 0

    def getYear(self):
        return self.year

    def getProb(self):
        return self.policy_prob

    def getChoice(self):
        return self.policy_choice

    def getFeatures(self):
        return self.features

    def getOutcomes(self):
        return self.outcomes

    def getFeatureLabels(self):
        return self.feature_labels

    def getOutcomeLabels(self):
        return self.outcome_labels

    def getBurnTime(self):
        return self.burn_time

    def setYear(self, year):
        self.year = year

    def setChoice(self, choice):
        self.policy_choice = choice

    def setProb(self, prob):
        self.policy_prob = prob

    def setFeatures(self, feature_list):
        self.features = feature_list

    def setOutcomes(self, outcome_list):
        self.outcomes = outcome_list

    def setFeatureLabels(self, labels):
        self.feature_labels = labels

    def setOutcomeLabels(self, labels):
        self.outcome_labels = labels

    def setBurnTime(self, time):
        self.burn_time = time



class FireGirl_Landscape_Logbook:
    # This class defines an entire logbook
    
    def __init__(self):
        #A list will hold the actual entries
        self.log_list = []


    def checkYearExists(self, year):
        #This function checks if there's already an item of this year in the logbook
        #If so, nothing happens. If not, it creates one.
        
        year_found = False
        #checking for an item with this year
        for item in self.log_list:
            #print("Logbook.checkYearExists(year):  looking for year " + str(year)),
            if item.year == year:
                #item found, update this value
                year_found = True
                #print(": FOUND")
            #else:
                #print(": NOT FOUND")
        
        if year_found == False:
            #print("LogBook.checkYearExists(...) didn't find a year, so creating one")
            #no item with this year in the logbook, so make a new one and append it.
            item = FireGirl_Landscape_Logbook_Item()
            item.year = year
            #print("  before append, list contains: " + str(len(self.log_list)))
            self.log_list.append(item)    
            #print("  after append, list contains: " + str(len(self.log_list)))
            
            
            
    def updateYear(self, year, date, loc, temp, wind, timber, timber_ave8, timber_ave24, 
                        fuel, fuel_ave8, fuel_ave24, suppress_prob, suppress_decision,
                        cells_burned, timber_lost, logging_total, eco1, eco2, eco3):
                        
        #This function will take every entry needed for a logbook entry, and will
        #  update or create as needed. Values given as "[]" or "None" will be ignored.
        
        #check to see if this year already has an entry
        year_found = False
        for item in self.log_list:
            if item.year == year:
                year_found = True
                #the item exists, so update it's values
                item.setAll(year, date, loc, temp, wind, timber, timber_ave8, timber_ave24, 
                        fuel, fuel_ave8, fuel_ave24, suppress_prob, suppress_decision,
                        cells_burned, timber_lost, logging_total, eco1, eco2, eco3)
                        
        #if the year wasn't found in the logbook, create and add a new item
        if year_found == False:
            #new logbook item
            item = FireGirl_Landscape_Logbook_Item(year, date, loc, temp, wind, timber, timber_ave8, timber_ave24, 
                                                   fuel, fuel_ave8, fuel_ave24, suppress_prob, suppress_decision,
                                                    cells_burned, timber_lost, logging_total, eco1, eco2, eco3)
            #add item to the list
            self.log_list.append(item)
    
    def printAll(self):
        pass
    
    #The following functions will update the value of a given year's logbook_item
    #   and will create a new item with otherwise empty values if there isn't one.
    def updateDate(self, year, date):
        #print("logbookitem,updateDate(...) received year: " + str(year))
        self.checkYearExists(year)
        
        for item in self.log_list:
            if item.year == year:
                item.date = date
                break
    
    def updateLoc(self, year, loc):
        
        self.checkYearExists(year)
        
        for item in self.log_list:
            if item.year == year:
                item.loc = loc
                break
            
    def updateTemp(self, year, temp):
        
        self.checkYearExists(year)
        
        for item in self.log_list:
            if item.year == year:
                item.temp = temp
                break
    
    def updateWind(self, year, wind):
        
        self.checkYearExists(year)
        
        for item in self.log_list:
            if item.year == year:
                item.wind = wind
                break
    
    def updateTimber(self, year, timber):
        
        self.checkYearExists(year)
        
        for item in self.log_list:
            if item.year == year:
                item.timber = timber
                break
    
    def updateTimberAve8(self, year, timber_ave8):
        
        self.checkYearExists(year)
        
        for item in self.log_list:
            if item.year == year:
                item.timber_ave8 = timber_ave8
                break
    
    def updateTimberAve24(self, year, timber_ave24):
        
        self.checkYearExists(year)
        
        for item in self.log_list:
            if item.year == year:
                item.timber_ave24 = timber_ave24
                break
    
    def updateFuel(self, year, fuel):
        
        self.checkYearExists(year)
        
        for item in self.log_list:
            if item.year == year:
                item.fuel = fuel
                break
    
    def updateFuelAve8(self, year, fuel_ave8):
        
        self.checkYearExists(year)
        
        for item in self.log_list:
            if item.year == year:
                item.fuel_ave8 = fuel_ave8
                break
    
    def updateFuelAve24(self, year, fuel_ave24):
        
        self.checkYearExists(year)
        
        for item in self.log_list:
            if item.year == year:
                item.fuel_ave24 = fuel_ave24
                break
            
    def updateSuppressProb(self, year, suppress_prob):
        
        self.checkYearExists(year)
        
        for item in self.log_list:
            if item.year == year:
                item.suppress_prob = suppress_prob
                break
            
    def updateSuppressDecision(self, year, suppress_decision):
        
        self.checkYearExists(year)
        
        for item in self.log_list:
            if item.year == year:
                item.suppress_decision = suppress_decision
                break
            
    def updateCellsBurned(self, year, cells_burned):
        
        self.checkYearExists(year)
        
        for item in self.log_list:
            if item.year == year:
                item.cells_burned = cells_burned
                break
                
    def updateTimberLoss(self, year, timber_lost):
        
        self.checkYearExists(year)
        
        for item in self.log_list:
            if item.year == year:
                item.timber_lost = timber_lost
                break
                
    def updateLoggingTotal(self, year, logging_total):
        
        self.checkYearExists(year)
        
        for item in self.log_list:
            if item.year == year:
                item.logging_total = logging_total
                break
                
    def updateEco1(self, year, eco1):
        
        self.checkYearExists(year)
        
        for item in self.log_list:
            if item.year == year:
                item.eco1 = eco1
                break
                
    def updateEco2(self, year, eco2):
        
        self.checkYearExists(year)
        
        for item in self.log_list:
            if item.year == year:
                item.eco2 = eco2
                break
                
    def updateEco3(self, year, eco3):
        
        self.checkYearExists(year)
        
        for item in self.log_list:
            if item.year == year:
                item.eco3 = eco3
                break


class FireGirl_Landscape_Logbook_Item:
    # This class defines a single entry in a landscape logbook
    
    def __init__(self, year=None, date=None, loc=None, temp=None, wind=None, 
                    timber=None, timber_ave8=None, timber_ave24=None, 
                    fuel=None, fuel_ave8=None, fuel_ave24=None, suppress_prob=None,
                    suppress_decision=None, cells_burned=None, timber_loss=None,
                    logging_total=None, eco1=None, eco2=None, eco3=None):
            
        self.year = None
        self.date = None
        self.loc = None
        self.temp = None
        self.wind = None
        self.timber = None
        self.timber_ave8 = None
        self.timber_ave24 = None
        self.fuel = None
        self.fuel_ave8 = None
        self.fuel_ave24 = None
        self.suppress_prob = None
        self.suppress_decision = None
        self.cells_burned = None
        self.timber_loss = None
        self.logging_total = None
        self.eco1 = None
        self.eco2 = None
        self.eco3 = None
        
        #and now just pass the input arguments to the setAll() function
        self.setAll(year, date, loc, temp, wind, timber, timber_ave8, timber_ave24, 
                fuel, fuel_ave8, fuel_ave24, suppress_prob, suppress_decision,
                cells_burned, timber_loss, logging_total, eco1, eco2, eco3)
    
    
    def setAll(self, year, date, loc, temp, wind, timber, timber_ave8, timber_ave24, 
                    fuel, fuel_ave8, fuel_ave24, suppress_prob, suppress_decision,
                    cells_burned, timber_loss, logging_total, eco1, eco2, eco3):
        
        #setting values: check for [] or None, and if found, ignore
        
        if not (year == [] or year == None):
            self.year = year
            
        if not (date == [] or date == None):
            self.date = date
        
        if not (loc == [] or loc == None):
            self.loc = loc
            
        if not (temp == [] or temp == None):
            self.temp = temp
        
        if not (wind == [] or wind == None):
            self.wind = wind
        
        if not (timber == [] or timber == None):
            self.timber = timber
        
        if not (timber_ave8 == [] or timber_ave8 == None):
            self.timber_ave8 = timber_ave8
        
        if not (timber_ave24 == [] or timber_ave24 == None):
            self.timber_ave24 = timber_ave24
            
        if not (fuel == [] or fuel == None):
            self.fuel = fuel
            
        if not (fuel_ave8 == [] or fuel_ave8 == None):
            self.fuel_ave8 = fuel_ave8
            
        if not (fuel_ave24 == [] or fuel_ave24 == None):
            self.fuel_ave24 = fuel_ave24
            
        if not (suppress_prob == [] or suppress_prob == None):
            self.suppress_prob = suppress_prob
            
        if not (suppress_decision == [] or suppress_decision == None):
            self.suppress_decision = suppress_decision
            
        if not (cells_burned == [] or cells_burned == None):
            self.cells_burned = cells_burned
            
        if not (timber_loss == [] or timber_loss == None):
            self.timber_loss = timber_loss
            
        if not (logging_total == [] or logging_total == None):
            self.logging_total = logging_total
            
        if not (eco1 == [] or eco1 == None):
            self.eco1 = eco1
            
        if not (eco2 == [] or eco2 == None):
            self.eco2 = eco2
            
        if not (eco3 == [] or eco3 == None):
            self.eco3 = eco3

    def printAll(self):
        if not self.year == None: 
            print("Log Item from year " + str(self.year))
        else:
            print("Log Item: Year Not Set")
        if not self.year == None: print("date: " + str(self.date)),
        if not self.loc == None: print("  loc: " + str(self.loc)),
        if not self.temp == None: print("  temp: " + str(self.temp)),
        if not self.wind == None: print("  wind: " + str(self.wind)),
        if not self.timber == None: print("  timber: " + str(self.timber)),
        if not self.timber_ave8 == None: print("  t8: " + str(self.timber_ave8)),
        if not self.timber_ave24 == None: print("  t24: " + str(self.timber_ave24)),
        if not self.fuel == None: print("  fuel: " + str(self.fuel)),
        if not self.fuel_ave8 == None: print("  f8: " + str(self.fuel_ave8)),
        if not self.fuel_ave24 == None: print("  f24: " + str(self.fuel_ave24))
        
        if not self.suppress_prob == None: print("  sup_prob: " + str(self.suppress_prob)),
        if not self.suppress_decision == None: print("  sup_dec: " + str(self.suppress_decision)),
        if not self.cells_burned == None: print("  cells_burned: " + str(self.cells_burned)),
        if not self.timber_loss == None: print("  timber_loss: " + str(self.timber_loss)),
        if not self.logging_total == None: print("  log_tot: " + str(self.logging_total)),
        if not self.eco1 == None: print("  eco1: " + str(self.eco1)),
        if not self.eco2 == None: print("  eco2: " + str(self.eco2)),
        if not self.eco3 == None: print("  eco3: " + str(self.eco3))
        
        
class FireGirl_FireLog:
    #This class defines a logbook for a single fire. The location of each cell
    #that burns, and the local fire time (not the landscape year) is recorded.
        
    def __init__(self, year):

        #a list to hold individual burn events <- meaning a single cell igniting
        self.burn_events = []
        
        #a record of the year in which this fire takes place
        self.year = year
        
        #records of overall fire results
        self.cells_burned = 0
        self.timeber_loss = 0
    
    
    def addIgnitionEvent(self, time, location, spread_rate, crown_burned):
        #this function takes the time and location of an ignition and other 
        #  pertinent information and adds it to the list.
        
        this_event = [time, location, spread_rate, crown_burned, "ignition"]
        self.burn_events.append(this_event)
    
    def updateResults(self, timber_loss, cells_burned):
        self.cells_burned = cells_burned
        self.timber_loss = timber_loss
        
    def printBasicInfo(self):
        print("Year " + str(self.year) + " Fire:  Cells burned = " + str(self.cells_burned) + "   Timber Loss = " + str(self.timber_loss) )
    
    def printFireHistory(self):
        for i in range(len(self.burn_events)):
            b = self.burn_events[i]
            print("Ignition at time " + str( round(b[0],3) )     ),
            print("   Loc : " + str(b[1]) ),
            print("   SprdRt: " + str(  round(b[2],3)   )),
            print("   CrownBurn: " + str(b[3]))