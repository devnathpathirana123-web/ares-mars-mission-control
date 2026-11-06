
from terrain.generator import generate_terrain
from navigation.astar import astar
from analysis.suitability import plot_terrain
from analysis.rover_performance import (
    analyze_rover_performance,
    print_performance_report
)


def find_nearest_reachable_destination(
    terrain,
    start,
    intended_goal
):
    """
    Find the traversable destination closest to the
    intended goal that A* can actually reach.
    """

    rows, cols = terrain["traversable"].shape

    candidates = []

    for row in range(rows):
        for col in range(cols):

            candidate = (row, col)

            if candidate == start:
                continue

            if not terrain["traversable"][candidate]:
                continue

            distance_to_goal = (
                (row - intended_goal[0]) ** 2
                + (col - intended_goal[1]) ** 2
            )

            candidates.append(
                (distance_to_goal, candidate)
            )

    candidates.sort(key=lambda item: item[0])

    for _, candidate in candidates:

        path, cost, distance = astar(
            terrain,
            start,
            candidate
        )

        if path is not None:
            return candidate, path, cost, distance

    return None, None, None, None


def main():

    print("=============================================")
    print("       NASA MARS ROVER NAVIGATION")
    print("=============================================")

    # 1. Generate terrain.
    terrain = generate_terrain()

    print("\nMartian terrain generated successfully.")

    # 2. Define start and destination.
    intended_start = (0, 0)
    intended_goal = (29, 29)

    start = intended_start

    print("Intended starting position:", start)
    print("Intended destination:", intended_goal)

    # 3. Find a traversable starting position.
    if not terrain["traversable"][start]:

        print("\nStarting position is impassable.")
        print("Searching for a nearby traversable starting point...")

        safe_cells = list(
            zip(*terrain["traversable"].nonzero())
        )

        if not safe_cells:
            print("ERROR: No traversable terrain exists.")
            return

        start = min(
            safe_cells,
            key=lambda point: (
                (point[0] - intended_start[0]) ** 2
                + (point[1] - intended_start[1]) ** 2
            )
        )

        print("New starting position:", start)

    # 4. Attempt the intended destination.
    print("\nCalculating rover route...")

    if terrain["traversable"][intended_goal]:

        path, navigation_cost, route_distance = astar(
            terrain,
            start,
            intended_goal
        )

    else:
        path = None
        navigation_cost = None
        route_distance = None

    # 5. Find an alternative if necessary.
    if path is None:

        print("Intended destination is unreachable.")
        print("Searching for the nearest reachable destination...")

        (
            alternative_goal,
            path,
            navigation_cost,
            route_distance
        ) = find_nearest_reachable_destination(
            terrain,
            start,
            intended_goal
        )

        if path is None:
            print("ERROR: No reachable destination found.")
            return

        intended_goal = alternative_goal

        print(
            "Alternative destination selected:",
            intended_goal
        )

    # 6. Display route results.
    print("\n=============================================")
    print("             ROUTE FOUND")
    print("=============================================")

    print("Starting position:", start)
    print("Final destination:", intended_goal)
    print("Route points:", len(path))
    print("A* grid distance:", round(route_distance, 2))
    print("Navigation cost:", round(navigation_cost, 2))

    # 7. Analyse rover performance.
    performance = analyze_rover_performance(
        terrain,
        path,
        navigation_cost=navigation_cost,
        cell_size_m=100.0
    )

    print_performance_report(performance)

    # 8. Display 3D terrain and route.
    print("Opening terrain visualisation...")

    plot_terrain(
        terrain,
        path=path,
        start=start,
        goal=intended_goal,
        performance=performance

    )


if __name__ == "__main__":
    main()
