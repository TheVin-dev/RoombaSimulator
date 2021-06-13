import numpy as np 
from geometry_msgs.msg import PoseStamped,Pose,Point,Quaternion

chargeLoc = Pose() 

chargeLoc.position.x = 0.
chargeLoc.position.y = 0.
chargeLoc.position.z = 0.

farLeft = Pose() 
farLeft.position = Point(x=-6.681,y=-3.314,z=0.0)
farLeft.orientation = Quaternion(x=0.0,y=0.0,z=0.783,w=0.622)
random = farLeft

#Far left: (-6.681,-3.314,0,0,0,0.783,0.622)

goal_list = [farLeft,random]
goal_list.insert(0,chargeLoc)
d = ["Charge" if x==0  else x for x in range(len(goal_list)) ]
goalDict = dict(zip(d,goal_list))
#mark_apple if apple_is_ripe else leave_it_unmarked for apple in apple_box

id = np.random.choice(list(goalDict.keys()))


print(f"Chose {id} goal: {goalDict.get(id, ['Empty goal'])}")
