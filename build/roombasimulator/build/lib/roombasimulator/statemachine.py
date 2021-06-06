
from transitions import Machine 
import enum
from Robot import Robot 
from transitions import State






robot = Robot()




machine = Machine(model=robot,states = states_list,transitions=transitions,initial='Moving')

