from typing import List

class Satelite:
    def __init__(self, name: str,velocity: float, orbitRadius: float ) -> None:
        self.name = name
        self.velocity = velocity
        self.orbitRadius = orbitRadius
        self.position: List = ... #TO DO: add starting position 
        self.isTransmiting: bool = False 
        self.dataPath:str = ... #TO DO
        self.currentimage:str = ... #TO DO

    def calculatePosition(self) -> List[int, int]:
        ...
    def transmitData(self):
        ...