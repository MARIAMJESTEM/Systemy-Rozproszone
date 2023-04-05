from typing import List, Tuple, Dict, Union
from satelite import Satellite


def simulate(satellites: List[Satellite], time_end: int) -> Tuple[Dict[str, Dict[str, List[Union[float, bool]]]], int]:
    satellites_data: Dict[str, Dict[str, List[Union[float, bool]]]] = {}
    samples: int = 0
    for S in satellites:
        satellites_data[S.name] = {'x': [], 'y': [], 'transmitting': []}

    for t in range(time_end):
        for S in satellites:
            if t % 1000 == 0:
                satellites_data[S.name]['x'].append(S.position[0])
                satellites_data[S.name]['y'].append(S.position[1])
                satellites_data[S.name]['transmitting'].append(S.is_available())
                samples += 1
            S.calculate_next_position()

    return satellites_data, samples // len(satellites)
