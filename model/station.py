from typing import List, Dict
from satelite import Satellite
import numpy as np
import os
from PIL import Image
import shutil


class Station:
    def __init__(self) -> None:
        self.satellitesDict: Dict[Satellite, List] = {}
        self.occupied_by = None

    def transmit_data(self, satellite: Satellite):
        if satellite not in self.satellitesDict:
            return

        if self.occupied_by != satellite.name and self.occupied_by is not None:
            return

        if self.occupied_by is None:
            self.occupied_by = satellite.name
            print(f'Satellite {satellite.name} starts transmission')

        if self.occupied_by is None:
            return

        if not satellite.is_available():
            self.occupied_by = None
            print(f'Satellite {satellite.name} ends transmission (not available)')
            return

        if satellite.get_image_count() == 0:
            self.occupied_by = None
            print(f'Satellite {satellite.name} ends transmission (no images to send)')
            return

        try:
            path_to_save = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/base")) + "\\{}".format(
                satellite.name) + "\\" + satellite.current_image
            buffer = self.satellitesDict[satellite]
            pixel_coordinates = satellite.pixel_coordinates
            buffer[1][pixel_coordinates[0], pixel_coordinates[1], 0] = buffer[0][pixel_coordinates[0], pixel_coordinates[1], 0]
            buffer[1][pixel_coordinates[0], pixel_coordinates[1], 1] = buffer[0][pixel_coordinates[0], pixel_coordinates[1], 1]
            buffer[1][pixel_coordinates[0], pixel_coordinates[1], 2] = buffer[0][pixel_coordinates[0], pixel_coordinates[1], 2]
            if pixel_coordinates[0] + 1 == buffer[0].shape[0]:
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
        except KeyError:
            self.occupied_by = None
        except TypeError:
            self.occupied_by = None
            try:
                satellite.current_image = satellite.get_current_image()
                self.satellitesDict[satellite] = self.create_new_buffer(satellite)
            except PermissionError:
                pass

    def create_new_buffer(self, satellite: Satellite):
        if satellite.current_image is not None:
            satelite_image_path = satellite.data_path + "\\" + satellite.current_image
            source_image = np.array(Image.open(satelite_image_path))
            destination_image = np.empty_like(source_image)
            return [source_image, destination_image]

    def addSatelite(self, satellite: Satellite):
        if satellite not in self.satellitesDict:
            self.satellitesDict[satellite] = self.create_new_buffer(satellite)
            # creating space in database for satelite
            path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/base")) + "\\{}".format(
                satellite.name)
            try:
                os.makedirs(path)
            except FileExistsError:
                pass

    def deleteSatelite(self, satellite: Satellite):
        if satellite not in self.satellitesDict:
            return

        if self.occupied_by == satellite.name:
            self.occupied_by = None

        db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/base") + "\\{}".format(
            satellite.name))
        archived_db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/base/Archived") +
                                           "\\{}".format(satellite.name))

        try:
            os.mkdir(archived_db_path)
        except FileExistsError:
            pass

        for file_name in os.listdir(db_path):
            source = db_path + "\\" + file_name
            destination = archived_db_path + "\\" + file_name
            if os.path.isfile(source):
                shutil.move(source, destination)

        del self.satellitesDict[satellite]
        satellite.station = None
        os.rmdir(db_path)
        shutil.rmtree(os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/satelites")) + "\\{}".format(satellite.name))
