from FireGirlPathway import *

#create new Pathway, id=0, default policy, default as FireGirlPathway
ls = FireGirlPathway(0)

ls.generateNewPathway()

print '{0:6} {1:12} {2:12} {3:12} {4:12} {5:12} {6:12}'.format(
               'Year', 'Choice', 'Cells Brnd', 'Timb Loss', 'Sup. Cost', 'Harvest Totl', 'Growth Totl')

for y in range(500):
    ls.doOneYear()
    choice = ls.ignitions[y].getChoice()
    #'timber loss', 'cells burned', 'suppression cost', 'burn time'
    outcomes = ls.ignitions[y].getOutcomes()
    supcost = ls.yearly_suppression_costs
    growth = ls.yearly_growth_totals[y]
    harvest = ls.yearly_logging_totals[y]

    print '{0:3} {1:12} {2:12} {3:12} {4:12} {5:12} {6:12}'.format(
            y, choice, round(outcomes[1]), round(outcomes[0]), round(outcomes[2]), round(harvest), round(growth))


#supcost = ls.ignitions[y].getSuppressionTotal()
#harvest = ls.ignitions[y].getHarvestTotal()


#'{0:12.3f} {1:12.3f} {2:12.3f}'.format(arg1, arg2, arg3)