from satelite import Satellite
from station import Station
from simulation import simulate
from animation import make_animation
from PyQt5.QtWidgets import QApplication, QGridLayout, QGroupBox, QDialog, QPushButton, QVBoxLayout, QLabel, QTextEdit, QTextBrowser
from PyQt5.QtGui import QFont, QIcon
import random as rm
import sys
import threading
from copy import deepcopy


class StationWindow(QDialog):
    def __init__(self, station):
        super().__init__()
        self.label_name = QLabel('Satellite name')
        self.label_name_del = QLabel('Satellite name')
        self.label_radius = QLabel('Satellite radius')
        self.textbox_name = QTextEdit()
        self.textbox_orbit_radius = QTextEdit()
        self.add_button = QPushButton('Add')
        self.add_button.clicked.connect(self.add)
        self.textbox_error = QTextBrowser()
        self.textbox_threads = QTextBrowser()

        self.textbox_name_del = QTextEdit()
        self.del_button = QPushButton('Delete')
        self.del_button.clicked.connect(self.delete)

        self.AddGroupBox = QGroupBox('Adding satellite')
        self.DeleteGroupBox = QGroupBox('Deleting satellite')
        self.ErrorGroupBox = QGroupBox('Error messages')
        self.ThreadsGroupBox = QGroupBox('Threads statuses')

        self.createAddGroupBox()
        self.createDeleteGroupBox()
        self.createErrorGroupBox()
        self.createThreadsGroupBox()

        self.satellites = {}
        self.station = station

        self.main_layout = QGridLayout()

        self.initUI()

    def initUI(self):
        self.setGeometry(500, 300, 800, 500)
        self.main_layout.addWidget(self.AddGroupBox, 0, 0)
        self.main_layout.addWidget(self.DeleteGroupBox, 0, 1)
        self.main_layout.addWidget(self.ErrorGroupBox, 1, 0)
        self.main_layout.addWidget(self.ThreadsGroupBox, 1, 1)
        self.setLayout(self.main_layout)
        self.setWindowTitle('Menu')
        self.show()

    def createAddGroupBox(self):
        layout = QVBoxLayout()
        layout.addWidget(self.label_name)
        layout.addWidget(self.textbox_name)
        layout.addWidget(self.label_radius)
        layout.addWidget(self.textbox_orbit_radius)
        layout.addWidget(self.add_button)
        self.AddGroupBox.setLayout(layout)

    def createDeleteGroupBox(self):
        layout = QVBoxLayout()
        layout.addWidget(self.label_name_del)
        layout.addWidget(self.textbox_name_del)
        layout.addWidget(self.del_button)
        self.DeleteGroupBox.setLayout(layout)

    def createErrorGroupBox(self):
        layout = QVBoxLayout()
        layout.addWidget(self.textbox_error)
        self.ErrorGroupBox.setLayout(layout)

    def createThreadsGroupBox(self):
        layout = QVBoxLayout()
        layout.addWidget(self.textbox_threads)
        self.ThreadsGroupBox.setLayout(layout)

    def clear_fields_and_show_error(self, text_boxes, error):
        for textbox in text_boxes:
            textbox.clear()

        self.textbox_error.setText(f'ERROR: {error}')

    def add(self):
        text_boxes = [self.textbox_name, self.textbox_orbit_radius]
        new_name = self.textbox_name.toPlainText()
        if new_name == '' or new_name in self.satellites:
            self.clear_fields_and_show_error(text_boxes=text_boxes,
                                             error=f'Satellite \'{new_name}\' already exists' if new_name != '' else
                                             'Insert satellite name')
            return

        try:
            new_radius = int(self.textbox_orbit_radius.toPlainText())
        except ValueError:
            self.clear_fields_and_show_error(text_boxes=text_boxes,
                                             error=f'Orbit radius must be integer')
            return

        if new_radius < 40000000:
            self.clear_fields_and_show_error(text_boxes=text_boxes,
                                             error=f'Orbit radius must be greater than 40000000 meters')
            return

        self.textbox_error.clear()

        button_availability = QPushButton(f'{new_name} - Availability')
        button_transmitting = QPushButton(f'{new_name} - Transmit')
        S = Satellite(name=new_name,
                      orbit_radius=new_radius,
                      station=self.station,
                      lamp_availability=button_availability,
                      lamp_transmitting=button_transmitting)

        self.main_layout.addWidget(button_availability)
        self.main_layout.addWidget(button_transmitting)
        self.setLayout(self.main_layout)
        self.show()

        S.add_satellite_db()
        self.station.addSatelite(S)
        self.satellites[new_name] = S

        self.textbox_name.setText('')
        self.textbox_orbit_radius.setText('')
        S.start()
        self.textbox_threads.append(f'Thread {S.name} started.\n')

    def delete(self):
        text_boxes = [self.textbox_name_del]
        name_to_del = self.textbox_name_del.toPlainText()
        if name_to_del not in self.satellites:
            self.clear_fields_and_show_error(text_boxes=text_boxes,
                                             error=f'Satellite \'{name_to_del}\' does not exist')
            return

        self.textbox_error.clear()

        self.station.deleteSatelite(self.satellites[name_to_del])
        self.satellites[name_to_del].lamp_availability.setStyleSheet("background-color:#000000")

        self.main_layout.removeWidget(self.satellites[name_to_del].lamp_availability)
        self.satellites[name_to_del].lamp_availability.deleteLater()
        self.satellites[name_to_del].lamp_availability = None
        self.main_layout.removeWidget(self.satellites[name_to_del].lamp_transmitting)
        self.satellites[name_to_del].lamp_transmitting.deleteLater()
        self.satellites[name_to_del].lamp_transmitting = None

        del self.satellites[name_to_del]

        self.textbox_name_del.clear()

        self.textbox_threads.append(f'Thread {name_to_del} closed.\n')


class MainWindow(threading.Thread):
    def __init__(self, station):
        super().__init__()
        self.station = station

    def run(self):
        rules_window = QApplication(sys.argv)
        _ = StationWindow(self.station)
        rules_window.exec_()
        rules_window.closeAllWindows()
        rules_window.exit()


MW = MainWindow(station=Station())
MW.start()
