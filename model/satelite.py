from typing import List
import math
import matplotlib.pyplot as plt
from constants import GM, PI
import os
import random
import shutil
import threading


class Satellite(threading.Thread):
    def __init__(self, name: str, orbit_radius: float, station, lamp_availability, lamp_transmitting, color: str = 'red') -> None:
        super().__init__()
        self.name = name
        self.orbit_radius = orbit_radius  # in meters
        self.velocity = math.sqrt(GM / self.orbit_radius)
        self.data_path: str = self.add_satellite_db()
        self.current_image: str = self.get_current_image()
        self.pixel_coordinates = [0, 0]
        self.position: List = [0, self.orbit_radius]
        self.alpha = self.velocity / self.orbit_radius
        self.color = color
        self.station = station
        self.lamp_availability = lamp_availability
        self.lamp_transmitting = lamp_transmitting

    def run(self):
        while True:
            try:
                self.calculate_next_position()
                self.manage_lamps()
                if self.is_available() and self.get_image_count() > 0:
                    self.station.transmit_data(self)
                else:
                    if self.station.occupied_by == self.name:
                        print(f'Satellite {self.name} ends transmission')
                        self.station.occupied_by = None
            except AttributeError:
                return

    def calculate_next_position(self):
        phi = math.atan2(self.position[1], self.position[0])
        beta = phi - self.alpha
        self.position = [self.orbit_radius * math.cos(beta), self.orbit_radius * math.sin(beta)]

    def add_satellite_db(self) -> str:
        num_images_at_start = 4
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/satelites")) + "\\{}".format(self.name)
        try:
            os.makedirs(path)
        except FileExistsError:
            pass
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/satelites/main_base"))
        image_count = 0
        for file_name in os.listdir(base_path):
            if os.path.isfile(os.path.join(base_path, file_name)):
                image_count += 1
        random_images_numb = random.sample(range(1, image_count), num_images_at_start)
        for img_numb in random_images_numb:
            img_name = f"{img_numb}"+".png"
            source_path = os.path.join(base_path, img_name)
            copy_path = os.path.join(path, img_name)
            shutil.copyfile(source_path, copy_path)
        return path

    def delete_satellite_db(self):
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/satelites")) + "\\{}".format(self.name)
        shutil.rmtree(path)
        
    def delete_image(self, filename):
        file_path = os.path.join(self.data_path, filename)
        if os.path.exists(file_path):
            os.remove(file_path)

    def get_current_image(self) -> str:
        files = os.listdir(self.data_path)
        if len(files) != 0:
            return files[0]

    def get_image_count(self) -> int:
        files = os.listdir(self.data_path)
        return len(files)

    def is_available(self):
        return -2 * self.position[0] <= self.position[1] >= 2 * self.position[0]

    def manage_lamps(self):
        if self.is_available():
            if self.lamp_availability.palette().button().color().name() != '#00ff00':
                self.lamp_availability.setStyleSheet("background-color:#00ff00")

            if self.station.occupied_by == self.name:
                if self.lamp_transmitting.palette().button().color().name() != '#00ff00':
                    self.lamp_transmitting.setStyleSheet("background-color:#00ff00")
            else:
                if self.lamp_transmitting.palette().button().color().name() != '#ff0000':
                    self.lamp_transmitting.setStyleSheet("background-color:#ff0000")
        else:
            if self.lamp_availability.palette().button().color().name() != '#ff0000':
                self.lamp_availability.setStyleSheet("background-color:#ff0000")
            if self.lamp_transmitting.palette().button().color().name() != '#ff0000':
                self.lamp_transmitting.setStyleSheet("background-color:#ff0000")

