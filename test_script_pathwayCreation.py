from FireGirlPathway import *
from FireGirlPolicy import *
import random

#pol = FireGirlPolicy()
lndscp = FireGirlPathway(11)
lndscp.generateNewPathway()
lndscp.doOneYear()
lndscp.doOneYear()
lndscp.doYears(2)
print("Pathway's logbook contains " + str(len(lndscp.Logbook.log_list)) + " items")
f_len = len(lndscp.FireLog)
print("Pathway's fire log contains " + str(f_len) + " items")

print(len(lndscp.FireLog[0].burn_events))
print(len(lndscp.FireLog[1].burn_events))
print(len(lndscp.FireLog[2].burn_events))
#print(len(lndscp.FireLog[3].burn_events))

#print(lndscp.FireLog[2].burn_events[0])
lndscp.FireLog[0].printFireHistory()


lndscp.doYears(96)
print("Pathway's logbook contains " + str(len(lndscp.Logbook.log_list)) + " items")
f_len = len(lndscp.FireLog)
print("Pathway's fire log contains " + str(f_len) + " items")

#printing the logbook items
#for log in range(len(lndscp.Logbook.log_list)