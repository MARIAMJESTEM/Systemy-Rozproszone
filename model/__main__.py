from satelite import Satellite
from station import Station
from simulation import simulate
from animation import make_animation
from PyQt5.QtWidgets import QApplication, QGridLayout, QGroupBox, QDialog, QPushButton, QVBoxLayout, QLabel, QTextEdit
from PyQt5.QtGui import QFont, QIcon
import random as rm
import time
import sys
import threading
from copy import deepcopy

time_end = 40000000
station = Station()


class StationWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.label_name = 'Satellite name'
        self.label_radius = 'Satellite radius'
        self.textbox_name = QTextEdit()
        self.textbox_orbit_radius = QTextEdit()
        self.add_button = QPushButton('Add')
        self.add_button.clicked.connect(self.add)

        self.textbox_name_del = QTextEdit()
        self.del_button = QPushButton('Delete')
        self.del_button.clicked.connect(self.delete)

        self.AddGroupBox = QGroupBox('Adding satellite')
        self.DeleteGroupBox = QGroupBox('Deleting satellite')

        self.createAddGroupBox()
        self.createDeleteGroupBox()

        self.satellites = {}

        self.initUI()

    def initUI(self):
        self.setGeometry(500, 300, 800, 500)
        main_layout = QGridLayout()
        main_layout.addWidget(self.AddGroupBox, 0, 0)
        main_layout.addWidget(self.DeleteGroupBox, 0, 1)
        self.setLayout(main_layout)
        self.setWindowTitle('Menu')
        self.show()

    def createAddGroupBox(self):
        layout = QVBoxLayout()
        layout.addWidget(self.textbox_name)
        layout.addWidget(self.textbox_orbit_radius)
        layout.addWidget(self.add_button)
        self.AddGroupBox.setLayout(layout)

    def createDeleteGroupBox(self):
        layout = QVBoxLayout()
        layout.addWidget(self.textbox_name_del)
        layout.addWidget(self.del_button)
        self.DeleteGroupBox.setLayout(layout)

    def add(self):
        global time_end, station
        S = Satellite(name=self.textbox_name.toPlainText(),
                      orbit_radius=int(self.textbox_orbit_radius.toPlainText()),
                      end_time=time_end,
                      station=station)

        self.satellites[self.textbox_name.toPlainText()] = S

        self.textbox_name.setText('')
        self.textbox_orbit_radius.setText('')
        S.start()

    def delete(self):
        global station
        # self.satellites[self.textbox_name_del.toPlainText()]
        try:
            station.deleteSatelite(self.satellites[self.textbox_name_del.toPlainText()])
            del self.satellites[self.textbox_name_del.toPlainText()]
        except KeyError:
            pass
        self.textbox_name_del.setText('')


class MainWindow(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        rules_window = QApplication(sys.argv)
        my_window = StationWindow()
        rules_window.exec_()
        rules_window.closeAllWindows()
        rules_window.exit()


MW = MainWindow()
MW.start()
