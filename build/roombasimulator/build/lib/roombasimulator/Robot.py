import BatteryManagement
from BatteryManagement import BatteryManager
import transitions
from transitions import Machine 
import rclpy
import numpy as np
from rclpy import Node 
from rclpy.action import ActionClient

from geometry_msgs.msg import PoseStamped,Pose, Point
from squaternion import Quaternion
from nav2_msgs.action import NavigateToPose
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseStamped,Pose
from std_msgs.msg import Header 
from builtin_interfaces.msg import Time
from rclpy.qos import QoSDurabilityPolicy, QoSHistoryPolicy, QoSReliabilityPolicy
from rclpy.qos import QoSProfile
from nav_msgs.msg import Odometry
from std_msgs.msg import String

import random 
import time 

class pose():
    def __init__(self,x=0,y=0,z=0,w=1,i=0,j=0,k=0):
        self.x = x
        self.y = y 
        self.z = z 

        # quaternion
        self.w = w 
        self.i = i 
        self.j = j 
        self.k = k 



        self.phi = self.__get__phi() # get euler z angle from quaternion
    def __get__phi(self):
        return phi 

class Robot(Node,BatteryManager):
    states_list = ['Idle', 'Moving', 'Charging','Error']
    trans = [
    { 'trigger': 'goal_received', 'source': 'Idle', 'dest': 'Moving', 'after': 'MovetoGoal' ,'conditions': 'enoughCharge'},
    { 'trigger': 'arrived', 'source': 'Moving', 'dest': 'Idle','before':'stop', 'after':'PickGoal' ,'conditions': 'isArrived'},
    { 'trigger': 'ChargeNoGoal', 'source': 'Idle', 'dest': 'Charging' ,'conditions': 'ChargeTreshold'},
    { 'trigger': 'ChargeGoal', 'source': 'Idle', 'dest': 'Charging', 'after': 'MovetoGoal' ,'unless': 'enoughCharge'},
    { 'trigger': 'toGoalFromCharge', 'source': 'Charging', 'dest': 'Moving' ,'conditions': '[enoughCharge,GoalReceived]'},
    { 'trigger': 'toIdle', 'source': 'Charging', 'dest': 'Idle' ,'conditions': '[enoughCharge,noGoalReceived]','after':'PickGoal'},
    { 'trigger': 'error','source': '*', 'dest': 'Error' ,'after': 'Reset' }]



    TIMER_INTERVAL = 1 

    def __init__(self):
        super.__init__('BatteryPoweredRobot')
        self.goal_list = [NavigateToPose.Goal()] * 12
        #create publishers and subscribers 
        self._odomlistener = self.create_subscription(Odometry,'/odom',self.OdomCallback,10)
        self._twistListener = self.create_subscription(Twist,'/cmd_vel',self.curr_velocity,10)
        self._action_client = ActionClient(self,NavigateToPose,'/navigate_to_pose')

        self._IdleTimer = self.create_timer(self.TIMER_INTERVAL,self.IdleConsumption)
        # set current position and velocity
        self.curr_pose = Pose()
        self.curr_vel = Twist()
        self.curr_goal = None
        self.dst_remaining = 0

        # State machine 
        self.machine = Machine( 
        model = self,
        transitions = self.trans,
        states = self.states,
        initial = self.STOPPED)

        # State dependet attributes 
        self.pwrconsumption = self.idleConsumption


    # async callbacks
    def OdomCallback(self,msg):
        self.curr_pose = msg.Pose
    
    def curr_velocity(self,msg):
        self.curr_vel = msg


    def feedback_call(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.distance = feedback.distance_remaining
        self.get_logger().info('Received feedback distance: {0}'.format(feedback.distance_remaining))
        self.dst_remaining = feedback.distance_remaining


    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return

        self.get_logger().info('Goal accepted :)')


        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info('Result: {0}'.format(result))
    

    #Entry points states
    def IdleCallback(self) -> None:
        new_goal = self.pickGoal()
        #goal_pose = Pose(new_goal.pose.pose.position.x,new_goal.pose.pose.position.y,new_goal.pose.pose.position.z)

        dst =  None# get distance of the planned path .Action Distance remaining
        

        
        # verify new goal 
            # reachable reject and charge or accept
            # valid goal (inside maze) -> reject or accept
        # set curr goal to new goal 
        # 
        
        self.MovetoGoal(new_goal)
        

    def ChargingCallback(self)-> None:
        pass

    def MovingCallback(self)-> None:
        self._action_client.wait_for_server()
        self._send_goal_future = self._action_client.send_goal_async(self.cu)
        self._send_goal_future.add_done_callback(self.goal_response_callback)    


    #Triggers state transitions 
    def MovetoGoal(self,goal):
        print("We should now move to the goal")
        self.curr_goal = goal
        
    # Conditions for state transitions
    def enoughCharge(self):
        return True

    def isArrived(self): 
        return random.random() < 0.4


    def ChargeThreshold(self):
        return self.BatteryLevel < self.BatteryThreshold
     



    # Helper functions 
    def PickGoal(self):
        print("Picking new goal")
        new_goal = np.random.choice(self.goal_list)
        time.sleep(5)
        
        return new_goal 

    def stop(self):
        print("Set speed to 0")
    
    def Reset(self):
        print("Resetting everything!")

robot = Robot()

