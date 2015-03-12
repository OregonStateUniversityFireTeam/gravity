from FireGirl_Landscape import *

#create new landscape, id=0, default policy, default as FireGirlLandscape
ls = FireGirlLandscape(0)

ls.generateNewLandscape()

for y in range(15):
    ls.doOneYear()
    print("Year " + str(y))
    print("Fire Results")
    #print(ls.ignitions[y].feature_labels)
    #print(ls.ignitions[y].features)
    print(ls.ignitions[y].outcome_labels)
    print(ls.ignitions[y].outcomes)
    print("Policy  : " + str(ls.ignitions[y].getProb()))
    print("Suppress: " + str(ls.ignitions[y].getChoice()))
