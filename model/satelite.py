from typing import List
import math
import matplotlib.pyplot as plt
from constants import GM, PI


class Satellite:
    def __init__(self, name: str, orbit_radius: float, color='red') -> None:
        self.name = name
        self.orbit_radius = orbit_radius  # in meters
        self.velocity = math.sqrt(GM / self.orbit_radius)
        self.is_transmitting: bool = False
        self.data_path: str = ...  # TO DO
        self.current_image: str = ...  # TO DO
        self.position: List = [0, self.orbit_radius]
        self.alpha = self.velocity / self.orbit_radius
        self.color = color

    def calculate_next_position(self):
        phi = math.atan2(self.position[1], self.position[0])
        beta = phi - self.alpha
        self.position = [self.orbit_radius * math.cos(beta), self.orbit_radius * math.sin(beta)]

    def transmit_data(self, pixel_coordinates: List):
        ...

    def is_available(self):
        return -2 * self.position[0] <= self.position[1] >= 2 * self.position[0]
