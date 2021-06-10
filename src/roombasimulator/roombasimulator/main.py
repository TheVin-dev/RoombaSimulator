from Robot import Robot
import time
import rclpy
if __name__ == "__main__":
    rclpy.init()
    robot = Robot()

    print(robot.state)
    robot.to_Idle()
    

    # args = None
    # robot = Robot()


    # robotMachine = Robot()

    # rclpy.spin(robotMachine)
    # rclpy.shutdown()  