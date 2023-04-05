from satelite import Satellite
from simulation import simulate
from animation import make_animation

if __name__ == "__main__":
    S_1 = Satellite('S1', 42160000)
    S_2 = Satellite('S2', 20000000)
    S_3 = Satellite('S3', 30000000)
    satellites = [S_1, S_2, S_3]

    satellites_data, frames = simulate(
        satellites=satellites,
        time_end=400000
    )

    make_animation(
        satellites=satellites,
        satellites_data=satellites_data,
        frames=frames,
        output_path="../animations/satellites_animation.gif"
    )
