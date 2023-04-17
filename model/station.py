from typing import List, Dict
from satelite import Satellite
import numpy as np
import os
from PIL import Image


class Station:
    def __init__(self) -> None:
        self.satellitesDict: Dict[Satellite, List] = {}

    def transmit_data(self, satellite: Satellite):
        path_to_save = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/base")) + "\\{}".format(
            satellite.name) + "\\" + satellite.current_image
        buffer = self.satellitesDict[satellite]
        pixel_coordinates = satellite.pixel_coordinates
        buffer[1][pixel_coordinates[0], pixel_coordinates[1], 0] = buffer[0][pixel_coordinates[0], pixel_coordinates[1], 0]
        buffer[1][pixel_coordinates[0], pixel_coordinates[1], 1] = buffer[0][pixel_coordinates[0], pixel_coordinates[1], 1]
        buffer[1][pixel_coordinates[0], pixel_coordinates[1], 2] = buffer[0][pixel_coordinates[0], pixel_coordinates[1], 2]
        if pixel_coordinates[0] +1 == buffer[0].shape[0]:
            if pixel_coordinates[1] + 1 == buffer[0].shape[1]:
                satellite.pixel_coordinates[0] = 0
                satellite.pixel_coordinates[1] = 0
                destination_image = Image.fromarray(buffer[1])
                destination_image.save(path_to_save)
                satellite.delete_image(satellite.current_image)
                satellite.current_image = satellite.get_current_image()
                buffer = self.create_new_buffer(satellite)
            else:
                satellite.pixel_coordinates[1] += 1
        else:
            if pixel_coordinates[1] + 1 == buffer[0].shape[1]:
                satellite.pixel_coordinates[1] = 0
                satellite.pixel_coordinates[0] += 1

            else:
                satellite.pixel_coordinates[1] += 1
        self.satellitesDict[satellite] = buffer

    def create_new_buffer(self, satellite: Satellite):
        satelite_image_path = satellite.data_path + "\\" + satellite.current_image
        source_image = np.array(Image.open(satelite_image_path))
        destination_image = np.empty_like(source_image)
        return [source_image, destination_image]

    def addSatelite(self, satellite: Satellite):
        # Możemy tutaj dodać, więcej ograniczeń co do dodawania stacji. Jakiś kraj pochodzenia satelity czy coś innego

        if satellite not in self.satellitesDict:
            self.satellitesDict[satellite] = self.create_new_buffer(satellite)
            # creating space in database for satelite
            path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/base")) + "\\{}".format(
                satellite.name)
            if os.path.exists(path):
                raise FileExistsError(f"The directory {path} already exist!")
            else:
                os.makedirs(path)

    def deleteSatelite(self, satellite: Satellite):
        if satellite in self.satellitesDict:
            del self.satellitesList[satellite]
            # here can be added moving data gathered from this satelite to archive 


