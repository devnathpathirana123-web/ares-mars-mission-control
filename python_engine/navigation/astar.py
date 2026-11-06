
import heapq
import math
from itertools import count

# Support both direct execution and package imports.
try:
    from analysis.suitability import calculate_suitability
except ModuleNotFoundError:
    from python_engine.analysis.suitability import calculate_suitability


def heuristic(a, b):
    dr = abs(a[0] - b[0])
    dc = abs(a[1] - b[1])

    diagonal = min(dr, dc)
    straight = max(dr, dc) - diagonal

    return diagonal * math.sqrt(2) + straight


def calculate_cell_cost(terrain, row, col, suitability):
    slope = float(terrain["slope"][row, col])
    roughness = float(terrain["roughness"][row, col])
    hazard = float(terrain["hazard"][row, col])

    if "terrain_class" in terrain:
        terrain_class = int(
            terrain["terrain_class"][row, col]
        )
    else:
        if (
            slope < 15
            and roughness < 10
            and hazard < 0.65
        ):
            terrain_class = 2
        else:
            terrain_class = 1

    if terrain_class == 0:
        return math.inf

    slope_cost = slope / 30.0
    roughness_cost = roughness / 20.0
    hazard_cost = hazard

    suitability_cost = 1.0 - float(
        suitability[row, col]
    )

    classification_cost = (
        0.0 if terrain_class == 2 else 2.0
    )

    return (
        1.0
        + 2.0 * slope_cost
        + 1.5 * roughness_cost
        + 3.0 * hazard_cost
        + 2.0 * suitability_cost
        + classification_cost
    )


def astar(terrain, start, goal):

    traversable = terrain["traversable"]
    rows, cols = traversable.shape

    for point in (start, goal):
        if not (
            0 <= point[0] < rows
            and 0 <= point[1] < cols
        ):
            raise ValueError(
                "Coordinate is outside the terrain grid."
            )

    if not traversable[start] or not traversable[goal]:
        return None, math.inf, math.inf

    if start == goal:
        return [start], 0.0, 0.0

    suitability = calculate_suitability(terrain)

    frontier = []
    tie_breaker = count()

    heapq.heappush(
        frontier,
        (
            heuristic(start, goal),
            next(tie_breaker),
            0.0,
            start
        )
    )

    came_from = {}
    cost_so_far = {start: 0.0}
    distance_so_far = {start: 0.0}

    movements = [
        (-1, 0), (1, 0),
        (0, -1), (0, 1),
        (-1, -1), (-1, 1),
        (1, -1), (1, 1)
    ]

    while frontier:

        _, _, current_cost, current = heapq.heappop(
            frontier
        )

        if current_cost > cost_so_far.get(
            current, math.inf
        ):
            continue

        if current == goal:
            break

        for dr, dc in movements:

            nr = current[0] + dr
            nc = current[1] + dc

            if not (
                0 <= nr < rows
                and 0 <= nc < cols
            ):
                continue

            neighbour = (nr, nc)

            if not traversable[neighbour]:
                continue

            # Prevent diagonal corner-cutting.
            if dr != 0 and dc != 0:

                if (
                    not traversable[current[0] + dr, current[1]]
                    or not traversable[current[0], current[1] + dc]
                ):
                    continue

            step_distance = math.sqrt(
                dr ** 2 + dc ** 2
            )

            current_cell_cost = calculate_cell_cost(
                terrain,
                current[0],
                current[1],
                suitability
            )

            next_cell_cost = calculate_cell_cost(
                terrain,
                nr,
                nc,
                suitability
            )

            step_cost = (
                step_distance
                * (current_cell_cost + next_cell_cost)
                / 2.0
            )

            new_cost = cost_so_far[current] + step_cost

            if new_cost < cost_so_far.get(
                neighbour, math.inf
            ):

                cost_so_far[neighbour] = new_cost

                distance_so_far[neighbour] = (
                    distance_so_far[current]
                    + step_distance
                )

                came_from[neighbour] = current

                priority = (
                    new_cost + heuristic(neighbour, goal)
                )

                heapq.heappush(
                    frontier,
                    (
                        priority,
                        next(tie_breaker),
                        new_cost,
                        neighbour
                    )
                )

    if goal not in came_from:
        return None, math.inf, math.inf

    path = []
    current = goal

    while current != start:
        path.append(current)
        current = came_from[current]

    path.append(start)
    path.reverse()

    return (
        path,
        cost_so_far[goal],
        distance_so_far[goal]
    )
