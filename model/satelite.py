from typing import List
import math

class Satelite:
    def __init__(self, name: str, orbitRadius: float ) -> None:
        self.name = name
        self.orbitRadius = orbitRadius #in meters
        self.velocity = math.sqrt((39,8866*math.pow(10,13))/self.orbitRadius)
        self.position: List = [0, self.orbitRadius] #TO DO: add starting position 
        self.isTransmiting: bool = False 
        self.dataPath:str = ... #TO DO
        self.currentimage:str = ... #TO DO
        self.timePeriod = int((2*math.pi)/self.velocity) 

    def calculatePosition(self, time) -> List[int,int]:
        # TODO: nie testowałam jeszcze tego ale chciałam dodać żeby było widac że jest zaczete
        if time%self.timePeriod == 0: # if satelite is were it started:
            self.position = [0,self.orbitRadius]
            return self.position
        alpha = time*360/self.timePeriod
        self.position = [int(self.position[0]+self.orbitRadius*math.cos(alpha)),int(self.position[1]+self.orbitRadius*math.sin(alpha))]
        return self.position
        
    def transmitData(self, pixel_coordinates: List):
        ...