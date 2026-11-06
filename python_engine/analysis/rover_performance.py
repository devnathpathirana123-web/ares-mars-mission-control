
import math
import numpy as np


def analyze_rover_performance(
    terrain,
    path,
    navigation_cost=None,
    cell_size_m=100.0
):
    """
    Analyse the performance requirements of a rover route.

    Returns:
        Route distance
        Navigation cost
        Average terrain difficulty
        Hazard exposure
        Estimated energy consumption

    Energy consumption is an illustrative model,
    not a calibrated physical rover model.
    """

    if path is None or len(path) == 0:
        raise ValueError("No valid rover route was provided.")

    slope = terrain["slope"]
    roughness = terrain["roughness"]
    hazard = terrain["hazard"]

    # Extract terrain measurements along the route.
    route_slopes = np.array([
        slope[row, col] for row, col in path
    ])

    route_roughness = np.array([
        roughness[row, col] for row, col in path
    ])

    route_hazards = np.array([
        hazard[row, col] for row, col in path
    ])

    # Calculate route distance.
    grid_distance = 0.0

    for i in range(1, len(path)):
        previous = path[i - 1]
        current = path[i]

        row_difference = current[0] - previous[0]
        col_difference = current[1] - previous[1]

        grid_distance += math.sqrt(
            row_difference ** 2
            + col_difference ** 2
        )

    distance_m = grid_distance * cell_size_m
    distance_km = distance_m / 1000.0

    # Calculate average terrain characteristics.
    average_slope = float(np.mean(route_slopes))
    maximum_slope = float(np.max(route_slopes))

    average_roughness = float(
        np.mean(route_roughness)
    )

    average_hazard = float(
        np.mean(route_hazards)
    )

    # Determine difficult terrain percentage.
    if "terrain_class" in terrain:
        terrain_classes = np.array([
            terrain["terrain_class"][row, col]
            for row, col in path
        ])
    else:
        terrain_classes = np.where(
            (route_slopes < 15)
            & (route_roughness < 10)
            & (route_hazards < 0.65),
            2,
            1
        )

    difficult_cells = np.sum(
        terrain_classes == 1
    )

    difficult_percentage = (
        difficult_cells / len(path)
    ) * 100

    # Calculate cumulative hazard exposure.
    hazard_exposure = (
        average_hazard * distance_km
    )

    # Estimate energy consumption.
    # These coefficients are illustrative assumptions.
    base_energy_per_km = 20.0

    slope_penalty = average_slope * 0.8
    roughness_penalty = average_roughness * 0.5
    hazard_penalty = average_hazard * 10.0

    energy_per_km = (
        base_energy_per_km
        + slope_penalty
        + roughness_penalty
        + hazard_penalty
    )

    estimated_energy = (
        distance_km * energy_per_km
    )

    return {
        "distance_m": distance_m,
        "distance_km": distance_km,
        "navigation_cost": navigation_cost,
        "average_slope": average_slope,
        "maximum_slope": maximum_slope,
        "average_roughness": average_roughness,
        "average_hazard": average_hazard,
        "difficult_terrain_percentage": difficult_percentage,
        "hazard_exposure": hazard_exposure,
        "estimated_energy_wh": estimated_energy
    }


def print_performance_report(results):

    print("\n========================================")
    print("       ROVER PERFORMANCE REPORT")
    print("========================================")

    print(
        f"Route distance: "
        f"{results['distance_km']:.3f} km"
    )

    print(
        f"Navigation cost: "
        f"{results['navigation_cost']:.2f}"
        if results["navigation_cost"] is not None
        else "Navigation cost: Not supplied"
    )

    print(
        f"Average slope: "
        f"{results['average_slope']:.2f} degrees"
    )

    print(
        f"Maximum slope: "
        f"{results['maximum_slope']:.2f} degrees"
    )

    print(
        f"Average roughness: "
        f"{results['average_roughness']:.2f}"
    )

    print(
        f"Average hazard: "
        f"{results['average_hazard']:.3f}"
    )

    print(
        f"Difficult terrain: "
        f"{results['difficult_terrain_percentage']:.1f}%"
    )

    print(
        f"Hazard exposure index: "
        f"{results['hazard_exposure']:.4f}"
    )

    print(
        f"Estimated energy: "
        f"{results['estimated_energy_wh']:.2f} Wh"
    )

    print("========================================\n")
