from typing import List
import math
import matplotlib.pyplot as plt


class Satellite:
    def __init__(self, name: str, orbit_radius: float) -> None:
        self.name = name
        self.orbit_radius = orbit_radius  # in meters
        self.velocity = math.sqrt(39.8866e13 / self.orbit_radius)
        self.is_transmitting: bool = False
        self.dataPath: str = ...  # TO DO
        self.current_image: str = ...  # TO DO
        self.position: List = [0, self.orbit_radius]
        self.alpha = self.velocity / self.orbit_radius

    def calculate_next_position(self):
        if self.position[0] == 0 and self.position[1] > 0:
            phi = math.pi / 2
        elif self.position[0] == 0 and self.position[1] < 0:
            phi = 1.5 * math.pi
        else:
            phi = math.atan2(self.position[1], self.position[0])
        beta = phi - self.alpha
        self.position = [self.orbit_radius * math.cos(beta), self.orbit_radius * math.sin(beta)]

    def transmit_data(self, pixel_coordinates: List):
        ...


S = Satellite('Andrzej', 42160000)

X, Y = [], []
for i in range(86000):
    X.append(S.position[0])
    Y.append(S.position[1])
    S.calculate_next_position()

plt.plot(X, Y, '-.')
plt.show()
