import sys
from threading import Timer,Thread,Event
import time
class BatteryManager(): 
    # consumption moving to goal state
    Energy_consumed_per_Meter = 0.005 # energy / meter
    # consumption idle state
    IDLE_CONSUMPTION =0.1# consuming / s 
    
    # charge rate for charging state
    chargeRate = 0.1 # batterylvl / s 
    CHARGE_TIMERVAL = 1
    BatteryThreshold = .1
    def __init__(self, level =1.0):
        self.BatteryLevel = level
        self.timer = perpetualTimer(self.CHARGE_TIMERVAL,self.IdleConsumption)
        
    def chargeBattery(self,charge):
        remaining = 1 - charge
        timetoCharge = remaining / self.chargeRate
        while (self.BatteryLevel < 1):
            self.BatteryLevel +=self.chargeRate
            print(f"Battery level: {self.BatteryLevel}")
            if (self.BatteryLevel >=1): 
                self.BatteryLevel = 1 
                return None
            time.sleep(1)

    def IdleConsumption(self):
        self.BatteryLevel -= self.CHARGE_TIMERVAL * self.IDLE_CONSUMPTION
        print("Current level: {0:.3f}| Currently using {1:.3f} Energy/s".format(self.BatteryLevel,0.1))

            #self.BatteryLevel = BatteryThreshold
            





class perpetualTimer():

    def __init__(self,t,hFunction):

        self.t=t
        self.hFunction = hFunction
        self.thread = Timer(self.t,self.handle_function)
        self.level = 0 
    def handle_function(self):
        self.hFunction()
        self.thread = Timer(self.t,self.handle_function)
        self.thread.start()

    def start(self):
        self.thread.start()

    def cancel(self):
        self.thread.cancel()
        



if __name__== "__main__":
    bat = BatteryManager()
    bat.timer.start()
