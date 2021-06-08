from Robot import Robot
import time
import rclpy
if __name__ == "__main__":
    rclpy.init()
    robot = Robot()
    robot.start_IdleConsumption()
    time.sleep(20)
    print(robot.BatteryLevel)
    robot.end_IdleConsumption()

    print(f"test succesvol")
    # args = None
    # robot = Robot()

    # 
    # robotMachine = Robot()
    
    # rclpy.spin(robotMachine)
    # rclpy.shutdown()