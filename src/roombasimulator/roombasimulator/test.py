import numpy as np 
class Goal():
    def __init__(self):
        pass
    
    def __str__(self):
        return "Navigation Goal"
    
    def __repr__(self):
        return str(self)
chargeLoc = Goal() 
goal_list = [Goal()] * 5
goal_list.insert(0,chargeLoc)
d = ["Charge" if x==0  else x for x in range(len(goal_list)) ]


#mark_apple if apple_is_ripe else leave_it_unmarked for apple in apple_box


goalDict = dict(zip(d,goal_list))
id = np.random.choice(list(goalDict.keys()))

print(goalDict)
print(id)
print(f"Chose {id} goal: {goalDict.get(id, 'Empty goal')}")
