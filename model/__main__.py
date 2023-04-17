from satelite import Satellite
from station import Station
from simulation import simulate
from animation import make_animation

if __name__ == "__main__":
    station = Station()
    S_1 = Satellite('S1', 42160000)
    # S_2 = Satellite('S2', 20000000)
    # S_3 = Satellite('S3', 30000000)
    station.addSatelite(S_1)

    satellites = [S_1]
    time_end = 40000000

    for t in range(time_end):
        for S in satellites:
            S.calculate_next_position()
            if S.is_transmitting:
                station.transmit_data(S)
    # satellites_data, frames = simulate(
    #     satellites=satellites,
    #     time_end=400000
    # )
    #
    # make_animation(
    #     satellites=satellites,
    #     satellites_data=satellites_data,
    #     frames=frames,
    #     output_path="../animations/satellites_animation.gif"
    # )
