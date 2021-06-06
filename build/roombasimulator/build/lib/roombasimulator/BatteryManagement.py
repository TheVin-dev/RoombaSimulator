
import time

class BatteryManager(): 
    # consumption moving to goal state
    Energy_consumed_per_Meter = 1 # energy / meter
    # consumption idle state
    idleConsumption =1 # consuming / s 
    
    # charge rate for charging state
    chargeRate = 1 # batterylvl / s 
    BatteryThreshold = 0.3
    def __init__(self, level =1.0):
        self.BatteryLevel = level
        
        
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

    def IdleConsumption(self,interval):
        print(f"Currently using {self.idleConsumption} Energy/s")
        self.BatteryLevel -= interval * self.idleConsumption
        if self.BatteryLevel < 0: 
            self.BatteryLevel = 0

    def changeBatterylevelMoving(self,dx):
        
        self.BatteryLevel -= self.Energy_consumed_per_Meter * dx
        
        return None
        
        

    def goalReachable(self):

        pass



if __name__== "__main__":
    bat = BatteryManager()
    
