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
    { 'trigger': 'to_Idle', 'source': 'initial', 'dest': 'Idle'},
    { 'trigger': 'to_Moving', 'source': 'Idle', 'dest': 'Moving','before': 'stopTimer' },
    { 'trigger': 'Charging', 'source': 'Moving', 'dest': 'Charging','conditions': 'arrivedChargeLocation'},
    { 'trigger': 'Idling', 'source': 'Moving', 'dest': 'Idle','conditions': ['NOT arrivedChargeLocation','secondGoalEmpty']}, #NOTE: these condition should be OR 
    { 'trigger': 'MovingfromCharge', 'source':'Charging', 'dest': 'Moving','conditions': 'BatteryFull'},
   
   ]



    TIMER_INTERVAL = 1 

    def __init__(self):
        super().__init__('BatteryPoweredRobot')
        #BatteryManager.__init__(self)
       
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

        self.BatteryManager = BatteryManager(hFunction=self.to_Moving)
        
        self.BatteryManager.primaryGoal= None
        self.BatteryManager.secondaryGoal= None
        
        self.velocity_timer = time.time()
        
    def on_enter_Idle(self):
        print('Entered the Idle state')
        self.BatteryManager.timer.start()
        #thread = self.start_IdleConsumption()
        self.PickGoal()

    def on_enter_Charging(self):
        """ 
        Entry point function for Charging state
        """
        # self._action_client_Navigation.wait_for_server()
        # self._send_goal_future = self._action_client_Navigation.send_goal_async(self.chargeLoc)
        # self._send_goal_future.add_done_callback(self.goal_response_navigation)    
        
        pass
    def on_enter_Moving(self):
        """ 
        Entry point function for Moving state
        """
        print("Entered state Moving")
        print(f"current primary goal: {self.BatteryManager.primaryGoal}")
        # self._action_client_Navigation.wait_for_server()
        # self._send_goal_future = self._action_client_Navigation.send_goal_async(self.curr_goal)
        # self._send_goal_future.add_done_callback(self.goal_response_navigation)    



    # async callbacks from subscribers
    def OdomCallback(self,msg):
        self.curr_pose = msg.Pose
       

    def curr_velocity(self,msg):
        time_received = time.time() 
        dt = time_received - self.velocity_timer  
        
        print("velocties: {:.2f}, {:.2f}".format(msg.linear.x,msg.linear.y))
        print("Time elasped: {:.2f}, equal to rate: {:.2f}".format(dt, 1/dt))
        if self.machine.is_state('Moving'):
            self.curr_vel = msg
            vx = msg.linear.x 
            vy = msg.linear.y 
            V = math.sqrt(vx*vx + vy+vy)
            if V >0.01:
                ds = V * dt 
                # TODO: get interval between messages and calculate dx
                #ds = math.sqt(dx*dx + dy*dy)
                self.BatteryManager.changeBatterylevelMoving(ds)
        self.velocity_timer = time.time()


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
            print(f"Goal is reachable, executing {self.BatteryManager.primaryGoal.pose.pose.position.x,self.BatteryManager.primaryGoal.pose.pose.position.y} ")
            
            self.to_Moving()
        elif not reachable:
            self.BatteryManager.primaryGoal,self.BatteryManager.secondaryGoal = self.chargeLoc,self.primaryGoal
            self.to_Moving()
        

        


    #Entry points states
    def PickGoal(self):
        print("Picking new goal")
        id = np.random.choice(list(self.goal_list.keys()))
        self.primaryGoal = self.goal_list[id]
        time.sleep(3)
        # TODO: Check if pathplanning server needs a NavigatetoPose.goal or just an pose 
        print('Goal done!') 
        
        self._action_client_Pathplanning.wait_for_server()
        self._send_goal_future = self._action_client_Pathplanning.send_goal_async(self.primaryGoal)
        self._send_goal_future.add_done_callback(self.goal_response_pp)

        
    
    def stopTimer(self):
        self.BatteryManager.timer.is_alive()
        self.BatteryManager.timer.cancel()
        self.BatteryManager.timer.stop()
        
        print("timer canceled")




    #Triggers state transitions 




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






