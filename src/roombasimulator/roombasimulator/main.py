from Robot import Robot
import time
import rclpy

def main():
    rclpy.init()
    robot = Robot()

    # print(robot.state)
    # robot.to_Idle()
    

    args = None
    robot = Robot()


    robotMachine = Robot()

    rclpy.spin(robotMachine)
    rclpy.shutdown()  
    
if __name__ == "__main__":
    main()