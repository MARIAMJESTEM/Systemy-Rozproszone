import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.animation import PillowWriter, FFMpegWriter
from satelite import Satellite
from constants import EARTH_RADIUS, EARTH_CENTER
import numpy as np
from typing import List


def make_animation(satellites: List[Satellite], satellites_data: dict, frames: int, output_path: str, limits: int = 45000000):
    def animate(ind):
        ax.clear()
        plt.axis('off')
        X = np.array([[-limits / 2, limits], [0, EARTH_RADIUS], [limits / 2, limits]])
        ax.add_patch(plt.Circle(EARTH_CENTER, EARTH_RADIUS, color='green'))
        ax.add_patch(plt.Polygon(X, color='white', alpha=0.3))
        for j_, s_ in enumerate(satellites):
            x, y = satellites_data[s_.name]['x'][ind], satellites_data[s_.name]['y'][ind]
            color = 'lime' if satellites_data[s_.name]['transmitting'][ind] else s_.color
            ax.plot(x, y, color=color, label=s_.name, marker='o')
            ax.annotate(s_.name, (x, y), color='white')

        ax.set_xlim([-limits, limits])
        ax.set_ylim([-limits, limits])
        ax.set_facecolor('black')

    fig, ax = plt.subplots(1, 1, facecolor='black')
    ani = FuncAnimation(fig, animate, frames=frames, interval=500, repeat=True)
    ani.save(output_path, writer=PillowWriter(fps=15))
    plt.close()
