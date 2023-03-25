from typing import List
from .satelite import Satelite
from .buffer import Buffer

class Station:
    def __init__(self) -> None:
        self.satelitesList: List[Satelite]
        self.buffortList: List[Buffer]

    def addSatelite(self):
        ...
    def deleteSatelite(self):
        ...
    