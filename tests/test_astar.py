
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from python_engine.navigation.astar import astar
from python_engine.terrain.generator import generate_terrain


def create_flat_terrain(size=30):
    return {
        "elevation": np.zeros((size, size)),
        "slope": np.zeros((size, size)),
        "roughness": np.zeros((size, size)),
        "hazard": np.zeros((size, size)),
        "traversable": np.ones((size, size), dtype=bool)
    }


def test_rover_can_find_route():
    terrain = create_flat_terrain()

    path, cost, distance = astar(
        terrain, (0, 0), (29, 29)
    )

    assert path is not None
    assert path[0] == (0, 0)
    assert path[-1] == (29, 29)
    assert cost > 0
    assert distance > 0


def test_invalid_coordinates():
    terrain = create_flat_terrain()

    try:
        astar(terrain, (-1, 0), (29, 29))
    except ValueError:
        return

    assert False, "Expected ValueError"


def test_generated_terrain_has_valid_dimensions():
    terrain = generate_terrain(size=30, seed=42)

    assert terrain["elevation"].shape == (30, 30)
    assert terrain["slope"].shape == (30, 30)
    assert terrain["traversable"].shape == (30, 30)


def test_start_equals_goal():
    terrain = create_flat_terrain()

    path, cost, distance = astar(
        terrain, (5, 5), (5, 5)
    )

    assert path == [(5, 5)]
    assert cost == 0
    assert distance == 0


def test_blocked_destination():
    terrain = create_flat_terrain()
    terrain["traversable"][29, 29] = False

    path, cost, distance = astar(
        terrain, (0, 0), (29, 29)
    )

    assert path is None
    assert cost == float("inf")
    assert distance == float("inf")


def test_diagonal_corner_cutting_prevented():
    terrain = create_flat_terrain(size=3)

    terrain["traversable"][0, 1] = False
    terrain["traversable"][1, 0] = False

    path, cost, distance = astar(
        terrain, (0, 0), (1, 1)
    )

    assert path is None
