import sys
import threading
from threading import Timer,Thread,Event
import time





class BatteryManager(): 
    # consumption moving to goal state
    Energy_consumed_per_Meter = 0.005 # energy / meter
    # consumption idle state
    IDLE_CONSUMPTION =0.1# consuming / s 
    
    # charge rate for charging state
    chargeRate = 0.1 # batterylvl / s 
    TIMERVAL = 1
    BatteryThreshold = .65
    def __init__(self, level =1.0,hFunction =None):
        self.BatteryLevel = level
        self.timer = perpetualTimer(self.TIMERVAL,self.IdleConsumption)
        self.hFunction = hFunction
        self.primaryGoal = None
        self.secondaryGoal = None

    def chargeBattery(self,charge):
        remaining = 1 - charge
        timetoCharge = remaining / self.chargeRate
        while (self.BatteryLevel < 1):
            self.BatteryLevel +=self.chargeRate
            print(f"Battery level: {self.BatteryLevel}")
            if (self.BatteryLevel >=1): 
                self.BatteryLevel = 1 

                self.hFunction()

                return None

            time.sleep(1)
    
    def IdleConsumption(self):
        if (self.timer.is_alive):
            self.BatteryLevel -= self.TIMERVAL * self.IDLE_CONSUMPTION
            print("BatteryLevel: {:.2f}".format(self.BatteryLevel))    
            if self.BatteryLevel < self.BatteryThreshold:
                print("Running out")
                self.timer.is_alive=False
                self.timer.stop()
                self.primaryGoal = "Werkt dit???"
                self.secondaryGoal = None
                self.hFunction()
                
            





class perpetualTimer(Thread):

    def __init__(self,t,hFunction):

        self.t=t
        self.hFunction = hFunction
        self.thread = Timer(self.t,self.handle_function)
        self._stop_event = threading.Event()

    def stop(self):
        print('stopped thread')
        self._stop_event.set()


    def handle_function(self):
        self.hFunction()
        self.thread = Timer(self.t,self.handle_function)
        self.thread.start()

    def start(self):
        self.thread.start()

    def cancel(self):
        print("Shutdown timer")
        self.thread.cancel()
        





if __name__== "__main__":
    bat = BatteryManager()
    batlow = bat.timer.start()
    print(batlow)
  
