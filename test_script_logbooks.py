from FireGirl_Landscape_Logbook import *

item1 = FireGirl_Landscape_Logbook_Item()
item1.setAll(1, 2, [3,4], 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20)
#item1.printAll()
item1.setAll(100, [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [])
#item1.printAll()
item1.setAll(None, None, None, None, None,None,None,None,None,None,None,None,None,None,None,None, None, None, 2000)
#item1.printAll()



#item2 = FireGirl_Landscape_Logbook_Item()
#item2.setAll(100, 200, [300,400], 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000)

lb = FireGirl_Landscape_Logbook()
lb.updateYear(2015, 2, [3,4], 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20)
            #print(len(lb.log_list))
            #lb.updateYear(2015, -1111, [3,4], 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20)
            #print(len(lb.log_list))
            #lb.log_list[0].printAll()
            #lb.checkYearExists(2015)
            #print(len(lb.log_list))
            #lb.checkYearExists(2016)
            #print(len(lb.log_list))
lb.updateDate(2016, -9999)
            #lb.log_list[1].printAll()
            #print(len(lb.log_list))
#lb.checkYearExists(2016)