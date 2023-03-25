import numpy as np
from .satelite import Satelite

class Buffer:
    def __init__(self) -> None:
        self.matrix = np.array([])
        self.satelite: Satelite

    def add(self,posX: int, posY: int):
        ...