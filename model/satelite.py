from typing import List
import math
import matplotlib.pyplot as plt
from constants import GM, PI
import os
import random
import shutil
import threading


class Satellite(threading.Thread):
    def __init__(self, name: str, orbit_radius: float, end_time: int, station, color: str = 'red') -> None:
        super().__init__()
        self.name = name
        self.orbit_radius = orbit_radius  # in meters
        self.velocity = math.sqrt(GM / self.orbit_radius)
        self.is_transmitting: bool = True
        self.data_path: str = self.add_satellite_db()
        self.current_image: str = self.get_current_image()
        self.pixel_coordinates = [0, 0]
        self.position: List = [0, self.orbit_radius]
        self.alpha = self.velocity / self.orbit_radius
        self.color = color
        self.end_time = end_time
        self.station = station

    def run(self):
        self.add_satellite_db()
        self.station.addSatelite(self)
        for _ in range(self.end_time):
            self.calculate_next_position()
            if self.is_transmitting:
                self.station.transmit_data(self)

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
        print('In delete_satellite_db()')
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/satelites")) + "\\{}".format(self.name)
        try:
            print('In TRY delete_satellite_db()')
            os.remove(path)
            print('Path removed in delete_satellite_db()')
        except Error:
            print('In FileNotFoundError')
        
    def delete_image(self, filename):
        file_path = os.path.join(self.data_path, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            raise FileNotFoundError("No file to delete found in directory")

    def get_current_image(self) -> str:
        files = os.listdir(self.data_path)
        if len(files) != 0:
            return files[0]
        # else:
        #     raise FileNotFoundError("No files found in directory")

    def is_available(self):
        return -2 * self.position[0] <= self.position[1] >= 2 * self.position[0]
