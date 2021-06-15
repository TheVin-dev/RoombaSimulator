import sys
import threading
from threading import Timer,Thread,Event
import time




class BatteryManager(): 
    # consumption moving to goal state
    Energy_consumed_per_Meter = 0.005 # energy / meter
    # consumption idle state
    IDLE_CONSUMPTION =0.01# consuming / s 
    
    # charge rate for charging state
    chargeRate = 0.1 # batterylvl / s 
    TIMERVAL = 1
    BatteryThreshold = .65
    def __init__(self,chargeLoc, level =1.0,hFunction =None,eFunction = None):
        self.BatteryLevel = level
        self.timer = perpetualTimer(self.TIMERVAL,self.IdleConsumption)
        self.chargeLoc = chargeLoc


        self.to_move = hFunction
        self.to_error = eFunction
        self.primaryGoal = None
        self.secondaryGoal = None

    def chargeBattery(self):
        inittial_charge = self.BatteryLevel
        remaining = 1 - inittial_charge
        timetoCharge = remaining / self.chargeRate
        while (self.BatteryLevel < 1):
            self.BatteryLevel +=self.chargeRate
            print(f"Battery level: {self.BatteryLevel}")
            if (self.BatteryLevel >=1): 
                self.BatteryLevel = 1 

                
                self.to_move()
               

            time.sleep(1)
    
    def IdleConsumption(self):
        if (self.timer.is_alive):
            self.BatteryLevel -= self.TIMERVAL * self.IDLE_CONSUMPTION
            print("BatteryLevel: {:.2f}".format(self.BatteryLevel))
            if self.BatteryLevel <=0: 
                print("Battery died! Need maintenance! ")
                self.timer.is_alive=False
                self.to_error()
                if self.BatteryLevel < self.BatteryThreshold:
                    print("Running out")
                    self.primaryGoal = self.chargeLoc
                    self.to_move()
                
            





class perpetualTimer(Thread):

    def __init__(self,t,hFunction):

        self.t=t
        self.hFunction = hFunction
        self.thread = Timer(self.t,self.handle_function)
        self._stop_event = threading.Event()

    def stop(self):
        #print('stopped thread')
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
  
