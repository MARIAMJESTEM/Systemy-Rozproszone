from typing import List
from satelite import Satellite
from buffer import Buffer

class Station:
    def __init__(self) -> None:
        self.satelitesList: List[Satellite] = []
        self.buffortList: List[Buffer]

    def addSatelite(self, satelite_name: Satellite):
        # Możemy tutaj dodać, więcej ograniczeń co do dodawania stacji. Jakiś kraj pochodzenia satelity czy coś innego
        if satelite_name not in self.satelitesList:
            self.satelitesList.append(satelite_name)
        
    def deleteSatelite(self, satelite_name: Satellite):
        if satelite_name in self.satelitesList:
            self.satelitesList.remove(satelite_name)
    