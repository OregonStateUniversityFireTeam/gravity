import random

def FireGirl_DS_alg(seedValue, min_val, max_val, roughness=0.5):
    #This function creates a new 129x129 grid of values. It will return a list
    #  containing two elements, the first is a nested list for the timber_value
    #  grid, and the second is a nested list for the fuel_load grid
    #
    #Arguments:
    #seedValue:  is used to ensure replicability. If set to -1, the function
    #              uses system-provided random values instead (system time)
    #min_val:    is the lowest value the ds algorithm will allow in the grid
    #max_val:    is the highest value the ds algorithm will allow in the grid
    #roughness:  is a parameter of the ds algorithm which determines how smooth
    #              or rough the resulting field of values is. Values must fall
    #              between 0 and 1. Values close to 1 will result in rougher 
    #              landscapes than values close to 0. The first iteration of the
    #              DS algorithm will allow variation up to half the range between
    #              min_val and max_val. Subsquent iterations will multiply this
    #              range by the roughness value of the previous iteration.
    
    #Creating the timber_value and fuel_load grids
    timber_val = []
    fuel_load = []
    for i in range(129):
        timber_val.append([])
        fuel_load.append([])
        for j in range(129):
            timber_val[i].append(0)
            fuel_load[i].append(0)
            
            
    #setting seed value
    if seedValue == -1:
        #if the seed value was given as -1, that indicates using pseudo-random
        #  system values, and ignoring replicability
        #using random.seed() with no arguements allows python to use its
        #   ordinary system-defined pseudo-random values
        random.seed()
    else:
        #a seed value is specified, so use it. This allows replicability
        random.seed(seedValue)
        
        
            
    # Note to Self: to increment over the NxN grid, increment by x:
    #  9x9     -> 16
    #  17x17   -> 8
    #  33x33   -> 4
    #  65x65   -> 2
    #  129x129 -> 1
    
    
    #seeding the initial 9x9 grid with random values between min_val and max_val
    # (by incrementing in 16s, we'll cover 9 values, i.e. the 9x9 sub-grid)
    for i in range(0,129,16):
        for j in range(0,129,16):
            timber_val[i][j] = random.uniform(min_val, max_val)
            
    #TESTING
    #print("Step 1 results, 0-17")
    #printgrid(timber_val,0,17,0,17)
    #print("Step 1 results, 112-129")
    #printgrid(timber_val,112,129,112,129)
    
    
    #starting the DS algorithm with the 17x17 subgrid
    #First, make the diamonds, by inserting new values orthogonally between 
    #  the 9x9 grid-point values.  This means that on even-indexed rows we'll
    #  put values in starting at 7 (the 8th value), and incrementing by 16's.
    #  and averaging from the values 8 before, and 8 after on the same row.
    #  On odd-indexed rows, we'll start on index 0, and increment by 16s, and use
    #  average from the values above and below (in the same column).
    
    val_timb = 0
    val_fuel = 0
    wiggle_range = (0.5 * (max_val - min_val))
    
    #doing even-indexed rows
    for j in range(0,129,16):
        for i in range(8,129,16):
            #look at the value 8 before, and 8 after, and average them
            val_timb = 0.5 * (timber_val[i-8][j] + timber_val[i+8][j])
            val_fuel = 0.5 * (fuel_load[i-8][j] + fuel_load[i+8][j])
            
            #now wiggle the value. Since this is the first step, we allow the
            # average to wiggle up to 1/2 the range between min_val and max_val,
            # i.e, if the range between min and max is 4, then the total wiggle-room
            # will be +/-2, which is a range of 4.
            val_timb = DS_wiggle(val_timb, min_val, max_val, wiggle_range)
            val_fuel = DS_wiggle(val_fuel, min_val, max_val, wiggle_range)
            
            #and finally, assign the values to the grids
            timber_val[i][j] = val_timb
            fuel_load[i][j] = val_fuel
    
    #doing odd-indexed rows
    for j in range(8,129,16):
        for i in range(0,129,16):
            #look at the value above and below, and average them
            val_timb = 0.5 * (timber_val[i][j+8] + timber_val[i][j-8])
            val_fuel = 0.5 * (fuel_load[i][j+8] + fuel_load[i][j-8])
            
            #now wiggle the value as above
            val_timb = DS_wiggle(val_timb, min_val, max_val, wiggle_range)
            val_fuel = DS_wiggle(val_fuel, min_val, max_val, wiggle_range)
            
            #and finally, assign the values to the grids
            timber_val[i][j] = val_timb
            fuel_load[i][j] = val_fuel
    
    #Second, make the squares, by filling in those middle cells that we skipped
    #  in the diamond step. We only need to iterate on the odd-indexed rows, 
    #  because there are no "middles" on the even-indexed rows. We'll increment
    #  starting at index 7 (the 8th value), and increment by 16s (skipping every
    #  second value in the 17x17 sub-grid, because they're already filled)
    for j in range(8,129,16):
        for i in range(8,129,16):
            #look at the four values, above, below, left and right, and average them
            val_timb = 0.25 * (timber_val[i-8][j] +
                               timber_val[i+8][j] +
                               timber_val[i][j-8] +
                               timber_val[i][j+8] )
            val_fuel = 0.25 * (fuel_load[i-8][j] +
                               fuel_load[i+8][j] +
                               fuel_load[i][j-8] +
                               fuel_load[i][j+8] )
                               
            #on the square step, we don't need to wiggle unless we really feel 
            # like it. I'm skipping it for now.
            
            #and finally, assign the values to the grids
            timber_val[i][j] = val_timb
            fuel_load[i][j] = val_fuel
    
    #TESTING
    #print("Step 2 results, 0-17")
    #printgrid(timber_val,0,17,0,17)
    #print("Step 2 results, 112-129")
    #printgrid(timber_val,112,129,112,129)
    
    
    #CONTINUING the DS algorithm with the 33X33 subgrid
    wiggle_range = roughness * (0.5 * (max_val - min_val))
    
    #doing even-indexed rows
    for j in range(0,129,8):
        for i in range(4,129,8):
            #look at the value 4 before, and 4 after, and average them
            val_timb = 0.5 * (timber_val[i-4][j] + timber_val[i+4][j])
            val_fuel = 0.5 * (fuel_load[i-4][j] + fuel_load[i+4][j])
            
            #now wiggle the value.
            val_timb = DS_wiggle(val_timb, min_val, max_val, wiggle_range)
            val_fuel = DS_wiggle(val_fuel, min_val, max_val, wiggle_range)
            
            #and finally, assign the values to the grids
            timber_val[i][j] = val_timb
            fuel_load[i][j] = val_fuel
    
    #doing odd-indexed rows
    for j in range(4,129,8):
        for i in range(0,129,8):
            #look at the value above and below, and average them
            val_timb = 0.5 * (timber_val[i][j+4] + timber_val[i][j-4])
            val_fuel = 0.5 * (fuel_load[i][j+4] + fuel_load[i][j-4])
            
            #now wiggle the value as above
            val_timb = DS_wiggle(val_timb, min_val, max_val, wiggle_range)
            val_fuel = DS_wiggle(val_fuel, min_val, max_val, wiggle_range)
            
            #and finally, assign the values to the grids
            timber_val[i][j] = val_timb
            fuel_load[i][j] = val_fuel
    
    #Second, make the squares
    for j in range(4,129,8):
        for i in range(4,129,8):
            #look at the four values, above, below, left and right, and average them
            val_timb = 0.25 * (timber_val[i-4][j] +
                               timber_val[i+4][j] +
                               timber_val[i][j-4] +
                               timber_val[i][j+4] )
            val_fuel = 0.25 * (fuel_load[i-4][j] +
                               fuel_load[i+4][j] +
                               fuel_load[i][j-4] +
                               fuel_load[i][j+4] )
                               
            #on the square step, we don't need to wiggle unless we really feel 
            # like it. I'm skipping it for now.
            
            #and finally, assign the values to the grids
            timber_val[i][j] = val_timb
            fuel_load[i][j] = val_fuel

    #TESTING
    #print("Step 3 results, 0-17")
    #printgrid(timber_val,0,17,0,17)
    #print("Step 3 results, 112-129")
    #printgrid(timber_val,112,129,112,129)
    
    
    #CONTINUING the DS algorithm with the 65X65 subgrid
    wiggle_range = roughness * roughness * (0.5 * (max_val - min_val))
    
    #doing even-indexed rows
    for j in range(0,129,4):
        for i in range(2,129,4):
            #look at the value 2 before, and 2 after, and average them
            val_timb = 0.5 * (timber_val[i-2][j] + timber_val[i+2][j])
            val_fuel = 0.5 * (fuel_load[i-2][j] + fuel_load[i+2][j])
            
            #now wiggle the value.
            val_timb = DS_wiggle(val_timb, min_val, max_val, wiggle_range)
            val_fuel = DS_wiggle(val_fuel, min_val, max_val, wiggle_range)
            
            #and finally, assign the values to the grids
            timber_val[i][j] = val_timb
            fuel_load[i][j] = val_fuel
    
    #doing odd-indexed rows
    for j in range(2,129,4):
        for i in range(0,129,4):
            #look at the value above and below, and average them
            val_timb = 0.5 * (timber_val[i][j+2] + timber_val[i][j-2])
            val_fuel = 0.5 * (fuel_load[i][j+2] + fuel_load[i][j-2])
            
            #now wiggle the value as above
            val_timb = DS_wiggle(val_timb, min_val, max_val, wiggle_range)
            val_fuel = DS_wiggle(val_fuel, min_val, max_val, wiggle_range)
            
            #and finally, assign the values to the grids
            timber_val[i][j] = val_timb
            fuel_load[i][j] = val_fuel
    
    #Second, make the squares
    for j in range(2,129,4):
        for i in range(2,129,4):
            #look at the four values, above, below, left and right, and average them
            val_timb = 0.25 * (timber_val[i-2][j] +
                               timber_val[i+2][j] +
                               timber_val[i][j-2] +
                               timber_val[i][j+2] )
            val_fuel = 0.25 * (fuel_load[i-2][j] +
                               fuel_load[i+2][j] +
                               fuel_load[i][j-2] +
                               fuel_load[i][j+2] )
                               
            #on the square step, we don't need to wiggle unless we really feel 
            # like it. I'm skipping it for now.
            
            #and finally, assign the values to the grids
            timber_val[i][j] = val_timb
            fuel_load[i][j] = val_fuel
            
    #TESTING
    #print("Step 4 results, 0-17")
    #printgrid(timber_val,0,17,0,17)
    #print("Step 4 results, 112-129")
    #printgrid(timber_val,112,129,112,129)
    
    
    #FINALLY: finishing the DS algorithm with the whole 129x129 grid
    wiggle_range = roughness * roughness * roughness * (0.5 * (max_val - min_val))
    
    #doing even-indexed rows
    for j in range(0,129,2):
        for i in range(1,129,2):
            #look at the value 1 before, and 1 after, and average them
            val_timb = 0.5 * (timber_val[i-1][j] + timber_val[i+1][j])
            val_fuel = 0.5 * (fuel_load[i-1][j] + fuel_load[i+1][j])
            
            #now wiggle the value.
            val_timb = DS_wiggle(val_timb, min_val, max_val, wiggle_range)
            val_fuel = DS_wiggle(val_fuel, min_val, max_val, wiggle_range)
            
            #and finally, assign the values to the grids
            timber_val[i][j] = val_timb
            fuel_load[i][j] = val_fuel
    
    #doing odd-indexed rows
    for j in range(1,129,2):
        for i in range(0,129,2):
            #look at the value above and below, and average them
            val_timb = 0.5 * (timber_val[i][j+1] + timber_val[i][j-1])
            val_fuel = 0.5 * (fuel_load[i][j+1] + fuel_load[i][j-1])
            
            #now wiggle the value as above
            val_timb = DS_wiggle(val_timb, min_val, max_val, wiggle_range)
            val_fuel = DS_wiggle(val_fuel, min_val, max_val, wiggle_range)
            
            #and finally, assign the values to the grids
            timber_val[i][j] = val_timb
            fuel_load[i][j] = val_fuel
    
    #Second, make the squares
    for j in range(1,129,2):
        for i in range(1,129,2):
            #look at the four values, above, below, left and right, and average them
            val_timb = 0.25 * (timber_val[i-1][j] +
                               timber_val[i+1][j] +
                               timber_val[i][j-1] +
                               timber_val[i][j+1] )
            val_fuel = 0.25 * (fuel_load[i-1][j] +
                               fuel_load[i+1][j] +
                               fuel_load[i][j-1] +
                               fuel_load[i][j+1] )
                               
            #on the square step, we don't need to wiggle unless we really feel 
            # like it. I'm skipping it for now.
            
            #and finally, assign the values to the grids
            timber_val[i][j] = val_timb
            fuel_load[i][j] = val_fuel
            
    #TESTING
    #print("Step 5 results, 0-17")
    #printgrid(timber_val,0,17,0,17)
    #print("Step 5 results, 112-129")
    #printgrid(timber_val,112,129,112,129)
    
    
    #FINALLY - RETURNING THE LANDSCAPE
    results = [timber_val, fuel_load]
    return results
            
def DS_wiggle(current_val, min, max, range):
    #This function does the actual wiggle step. It will limit the possible range
    # of values to +/- 1/2x the range argument given, and will enforce the min and max
    # restrictions
    top = current_val + (0.5 * range)
    bottom = top - range
    
    #enforcing boundaries
    if top > max:
        top = max
    if bottom < min:
        bottom = min
    
    #the new value can be anything in between these ranges, so just grab a value
    new_val = random.uniform(bottom,top)
    
    return new_val
    
    
    
    
def printgrid(grid, x_start, x_end, y_start, y_end):
    #this is a test function to print segments of any 2D array. Make sure the 
    #  indices are okay, because it's not going to bother checking for you.
    
    for i in range(x_start,x_end):
        for j in range(y_start, y_end):
            print(str(int(grid[i][j])) + " "), #terminating with a comma instructs print to skip the newline
        print(" ") #to get a newline
            
            
            
            
            
            
            
            