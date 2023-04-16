import numpy as np
from satelite import Satellite

class Buffer:
    def __init__(self, img_shape, satellite_name: Satellite) -> None:
        self.matrix: np.ndarray = np.zeros(img_shape) #np.array([])
        self.satelite: Satellite = satellite_name

    def addToBuffer(self, posX: int, posY: int, posZ: int, val: int):
        self.matrix[posZ][posX][posY] = val
        # Jeżeli będzie indeksowanie od 1
        # self.matrix[posZ-1][posX-1][posY-1] = val