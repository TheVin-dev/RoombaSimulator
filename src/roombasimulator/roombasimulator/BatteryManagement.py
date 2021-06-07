import sys
from timer_test import perpetualTimer
class BatteryManager(): 
    # consumption moving to goal state
    Energy_consumed_per_Meter = 1 # energy / meter
    # consumption idle state
    idleConsumption =0.001 # consuming / s 
    
    # charge rate for charging state
    chargeRate = 1 # batterylvl / s 
    CHARGE_TIMERVAL = 1
    BatteryThreshold = 0.8
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
        self.BatteryLevel -= self.CHARGE_TIMERVAL * self.idleConsumption
        print("Current level: {0:.2f}| Currently using {0:.2f} Energy/s".format(self.BatteryLevel,self.chargeRate))
        
        if self.BatteryLevel < self.BatteryThreshold: 
            print(f"Running out of energy! Get to the charge station!")
            self.timer.cancel()
            sys.exit()
            #self.BatteryLevel = BatteryThreshold
            

    def changeBatterylevelMoving(self):
        print('Timer fires')
        #self.BatteryLevel -= self.Energy_consumed_per_Meter * dx
           
        

    def goalReachable(self,dst,dst_toCharge):
        Energy_needed_oneway = dst * self.Energy_consumed_per_Meter
        if Energy_needed_oneway*1.5 < self.BatteryLevel:
            return True

        return False
        #TODO: we need to make sure we can get back to the charging station from the goal 
        #Energy_needded_toCharge  = dst_toCharge * self.Energy_consumed_per_Meter

        



if __name__== "__main__":
    bat = BatteryManager()
    bat.timer.start()
