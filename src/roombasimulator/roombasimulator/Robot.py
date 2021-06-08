#!usr/bin/ python3
import BatteryManagement
from BatteryManagement import BatteryManager
import transitions
from transitions import Machine 
import rclpy
import numpy as np
from rclpy.node import Node 
from rclpy.action import ActionClient
import math
from geometry_msgs.msg import PoseStamped,Pose, Point
from squaternion import Quaternion
from nav2_msgs.action import NavigateToPose
from nav2_msgs.action import ComputePathToPose
from nav_msgs.msg import Path
from geometry_msgs.msg import Twist
from std_msgs.msg import Header 
from builtin_interfaces.msg import Time

from nav_msgs.msg import Odometry
from std_msgs.msg import String
import random 
import time 
import sys


class Robot(Node):
    states_list = ['initial','Idle', 'Moving', 'Charging','Error']
    trans = [
    { 'trigger': 'to_Idle', 'source': 'initial', 'dest': 'Idle', },
    { 'trigger': 'Moving', 'source': 'Idle', 'dest': 'Moving', 'after': 'MovetoGoal' ,'conditions': 'enoughCharge'},
    { 'trigger': 'Charging', 'source': 'Moving', 'dest': 'Charging', 'after': 'charge' ,'conditions': 'arrivedChargeLocation'},
    { 'trigger': 'Idling', 'source': 'Moving', 'dest': 'Idle','conditions': ['NOT arrivedChargeLocation','secondGoalEmpty']}, #NOTE: these condition should be OR 
    { 'trigger': 'MovingfromCharge', 'source':'Charging', 'dest': 'Moving', 'after': 'MovetoGoal' ,'conditions': 'BatteryFull'},
   
   ]



    TIMER_INTERVAL = 1 

    def __init__(self):
        super().__init__('BatteryPoweredRobot')
        #BatteryManager.__init__(self)
        self.BatteryManager = BatteryManager()

        self.goal_list = dict(zip(range(0,8),[NavigateToPose.Goal()] * 9))
        #create publishers and subscribers 
        self._odomlistener = self.create_subscription(Odometry,'/odom',self.OdomCallback,10)
        self._goallistener = self.create_subscription(PoseStamped,'/goal_pose',self.goalListener,1)
        self._twistListener = self.create_subscription(Twist,'/cmd_vel',self.curr_velocity,10)
        self._action_client_Navigation = ActionClient(self,NavigateToPose,'/navigate_to_pose')
        self._action_client_Pathplanning = ActionClient(self,ComputePathToPose,'/compute_path_to_pose')
        
        #self._IdleTimer = self.create_timer(self.TIMER_INTERVAL,self.IdleConsumption)
        # set current position and velocity
        self.curr_pose = Pose()
        self.curr_vel = Twist()
        self.curr_goal = None
        self.dst_remaining = 0.
        self.dst = 0 # dst used by initial reachable check
        self.chargeLoc = Pose()
        self.chargeLoc.position.x = 0.
        self.chargeLoc.position.y = 0.
        self.chargeLoc.position.z = 0.
        # State machine 
        self.machine = Machine( 
        model = self,
        transitions = self.trans,
        states = self.states_list,
        initial = "initial") 

        self.primaryGoal = None
        self.secondaryGoal = None

        
    def on_enter_Idle(self):
        print('Entered the Idle state')
        self.start_IdleConsumption()
        self.PickGoal()

    # async callbacks from subscribers
    def OdomCallback(self,msg):
        self.curr_pose = msg.Pose
        #self.curr_pose = pose(temp.position.x,temp.position.y,temp.position.z)

    def curr_velocity(self,msg):
        if self.machine.is_state('Moving'):
            self.curr_vel = msg
            vx = msg.linear.x 
            vy = msg.linear.y 
            
            V = math.sqrt(vx*vx + vy+vy)
            if V >0.01:

                dt = 0.5
                ds = V * dt 
                # TODO: get interval between messages and calculate dx
                #ds = math.sqt(dx*dx + dy*dy)
                self.BatteryManager.changeBatterylevelMoving(ds)

    def goalListener(self,msg):
        # If we want to incorporate manual goal support (HELLLL NOO)
        #self.new_goal = msg 
        pass


    # callback for the Navigate to pose action 
    def feedback_navigation(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.distance = feedback.distance_remaining
        self.get_logger().info('Received feedback distance: {0}'.format(feedback.distance_remaining))
        self.dst_remaining = feedback.distance_remaining


    def goal_response_navigation(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return

        self.get_logger().info('Goal accepted :)')


        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_navigation)

    def get_result_navigation(self, future):
        result = future.result().result
        self.get_logger().info('Result: {0}'.format(result))
        
    # Callbacks for the Compute path to pose action 
    def feedback_pp(self, feedback_msg):
        # er bestaat geen feedback msg for compute path to pose action
        #feedback = feedback_msg.feedback
        pass


    def goal_response_pp(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Path rejected??? :(')
            return

        self.get_logger().info('calculating path:)')


        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_pp)


    def get_result_pp(self, future):
        # path is of type nav_msgs.msg Path -> a sequence<PoseStamped>. 
        poses = future.result().result.path.poses # list() met posestamped als het goed is. 
        # path -> poses -> list(posestamped) -> (Pose, Header) Pose -> position -> x,y,z
        x = self.curr_pose.position.x
        y = self.curr_pose.position.y
        
        
        dst = 0 
        for i in range(len(poses)-1):
            #if i ==len(poses)-1:
            #    break

            dx = (poses[i+1].pose.position.x - poses[i].pose.position.x)
            dy = (poses[i+1].pose.position.y - poses[i].pose.position.y)
            dst += math.sqrt(dx*dx + dy*dy)

        self.dst = dst
                
        reachable = self.goalReachable(self.dst)


        if reachable:
            print(f"Goal is reachable, executing {self.primaryGoal.pose.pose.position.x,self.primaryGoal.pose.pose.position.y} ")
        elif not reachable:
            self.primaryGoal,self.secondaryGoal = self.chargeLoc,self.primaryGoal
            self.ChargeGoal()
        
        self.MovetoGoal()
 
        


    #Entry points states
    def PickGoal(self):
        print("Picking new goal")
        id = np.random.choice(list(self.goal_list.keys()))
        self.primaryGoal = self.goal_list[id]
        time.sleep(5)
        
        
        #goal_pose = Pose(new_goal.pose.pose.position.x,new_goal.pose.pose.position.y,new_goal.pose.pose.position.z)

        # start verifying goal thread
        
        # TODO: Check if pathplanning server needs a NavigatetoPose.goal or just an pose 
        print('Goal done!')
        return 
        self._action_client_Pathplanning.wait_for_server()
        self._send_goal_future = self._action_client_Pathplanning.send_goal_async(self.primaryGoal)
        self._send_goal_future.add_done_callback(self.goal_response_pp)

        
    def start_IdleConsumption(self):
        """ 
        Second idle starting point. starting the idle consumption of battery
        """
        #self.IdleConsumption()
        self.BatteryManager.timer.start()
        while (1): 
            if self.BatteryManager.BatteryLevel <= self.BatteryManager.BatteryThreshold: 
                print(f"Running out of energy! Get to the charge station!")
                #TODO: Trigger move to charge
                self.BatteryManager.timer.cancel()
                #self.primaryGoal = self.ChargeLoc
                #self.secondaryGoal = None
                #self.Move()
                break
        # if battery gets too low in the callback thread, transition to Charging state
    
    def end_IdleConsumption(self):
        self.BatteryManagertimer.cancel()
        print("timer canceled")


    def ChargingCallback(self):
        """ 
        Entry point function for Charging state
        """
        self._action_client_Navigation.wait_for_server()
        self._send_goal_future = self._action_client_Navigation.send_goal_async(self.chargeLoc)
        self._send_goal_future.add_done_callback(self.goal_response_navigation)    
        

    def MovingCallback(self):
        """ 
        Entry point function for Moving state
        """
        self._action_client_Navigation.wait_for_server()
        self._send_goal_future = self._action_client_Navigation.send_goal_async(self.curr_goal)
        self._send_goal_future.add_done_callback(self.goal_response_navigation)    


    #Triggers state transitions 
    def Moving(self,goal):
        print("We should now move to the goal")
        pass 


    def ChargeGoal(self):
        pass
        
    # Conditions for state transitions
    def enoughCharge(self):
        return True

    def isArrived(self): 
        return random.random() < 0.4


    def ChargeThreshold(self):
        return self.BatteryLevel < self.BatteryThreshold
     



    # Helper functions 
    def goalReachable(self,dst,dst_toCharge=0):
        Energy_needed_oneway = dst * self.Energy_consumed_per_Meter
        if Energy_needed_oneway*1.5 < self.BatteryLevel:
            return True

        return False
        #TODO: we need to make sure we can get back to the charging station from the goal 
        #Energy_needded_toCharge  = dst_toCharge * self.Energy_consumed_per_Meter


    def stop(self):
        print("Set speed to 0")
    
    def Reset(self):
        print("Resetting everything!")






