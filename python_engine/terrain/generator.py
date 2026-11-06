
import numpy as np


def generate_terrain(
    size=30,
    seed=42,
    cell_size_m=100.0,
    max_slope=30.0,
    max_roughness=20.0,
    max_hazard=0.92
):
    """
    Generate configurable synthetic Martian terrain.

    Parameters:
        size: Number of rows and columns.
        seed: Random seed for reproducible terrain.
        cell_size_m: Physical distance represented by each cell.
        max_slope: Maximum traversable slope in degrees.
        max_roughness: Maximum traversable roughness.
        max_hazard: Maximum traversable hazard index.
    """

    # 1. Validate configuration

    if not isinstance(size, (int, np.integer)) or isinstance(size, bool):
        raise ValueError("Grid size must be an integer.")

    if not 5 <= size <= 300:
        raise ValueError("Grid size must be between 5 and 300.")

    if not isinstance(seed, (int, np.integer)) or isinstance(seed, bool):
        raise ValueError("Random seed must be an integer.")

    if not np.isfinite(cell_size_m) or cell_size_m <= 0:
        raise ValueError("Cell spacing must be greater than zero.")

    if not np.isfinite(max_slope) or not 0 < max_slope <= 90:
        raise ValueError("Maximum slope must be between 0 and 90 degrees.")

    if not np.isfinite(max_roughness) or max_roughness <= 0:
        raise ValueError("Maximum roughness must be greater than zero.")

    if not np.isfinite(max_hazard) or not 0 < max_hazard <= 1:
        raise ValueError("Maximum hazard must be greater than 0 and at most 1.")

    rng = np.random.default_rng(seed)

    # 2. Generate coordinate grids

    x = np.linspace(-3, 3, size)
    y = np.linspace(-3, 3, size)

    xx, yy = np.meshgrid(x, y)

    # 3. Generate base Martian elevation

    elevation = (
        1000
        + 100 * np.sin(xx)
        + 80 * np.cos(yy)
        + 30 * np.sin(xx * yy)
        + rng.normal(0, 3, (size, size))
    )

    # 4. Generate impact craters

    crater_count = max(2, size // 10)

    for _ in range(crater_count):

        crater_x = rng.integers(0, size)
        crater_y = rng.integers(0, size)

        radius = rng.uniform(2, 5)
        depth = rng.uniform(10, 30)

        distance = np.sqrt(
            (xx - xx[crater_y, crater_x]) ** 2
            + (yy - yy[crater_y, crater_x]) ** 2
        )

        crater = -depth * np.exp(
            -(distance ** 2) / (2 * (radius / 3) ** 2)
        )

        elevation += crater

    # 5. Generate rock fields using vectorised operations

    rock_map = np.zeros((size, size), dtype=float)

    rock_count = max(5, size // 2)

    row_grid, col_grid = np.indices((size, size))

    for _ in range(rock_count):

        rock_x = rng.integers(0, size)
        rock_y = rng.integers(0, size)

        rock_radius = rng.integers(1, 3)

        distance = np.sqrt(
            (row_grid - rock_y) ** 2
            + (col_grid - rock_x) ** 2
        )

        rock_cells = distance <= rock_radius

        rock_map[rock_cells] = 1

        elevation[rock_cells] += rng.uniform(5, 15)

    # 6. Calculate slope using configurable cell spacing

    dy, dx = np.gradient(
        elevation,
        cell_size_m,
        cell_size_m
    )

    slope = np.degrees(
        np.arctan(np.sqrt(dx ** 2 + dy ** 2))
    )

    # 7. Calculate surface roughness

    padded = np.pad(
        elevation,
        pad_width=1,
        mode="edge"
    )

    neighbourhoods = np.stack(
        [
            padded[i:i + size, j:j + size]
            for i in range(3)
            for j in range(3)
        ],
        axis=0
    )

    roughness = np.std(
        neighbourhoods,
        axis=0
    )

    # 8. Generate environmental hazards

    hazard = rng.random((size, size))

    hazard = np.clip(
        hazard + rock_map * 0.5,
        0,
        1
    )

    # 9. Determine traversability using user parameters

    traversable = (
        (slope < max_slope)
        & (roughness < max_roughness)
        & (hazard < max_hazard)
    )

    # 10. Classify terrain

    terrain_class = np.zeros(
        (size, size),
        dtype=int
    )

    # 0 = Impassable
    # 1 = Difficult
    # 2 = Safe

    terrain_class[
        traversable
        & (
            (slope >= max_slope * 0.5)
            | (roughness >= max_roughness * 0.5)
            | (hazard >= max_hazard * 0.7)
        )
    ] = 1

    terrain_class[
        traversable
        & (slope < max_slope * 0.5)
        & (roughness < max_roughness * 0.5)
        & (hazard < max_hazard * 0.7)
    ] = 2

    return {
        "elevation": elevation,
        "slope": slope,
        "roughness": roughness,
        "hazard": hazard,
        "rock_map": rock_map,
        "terrain_class": terrain_class,
        "traversable": traversable
    }


if __name__ == "__main__":

    terrain = generate_terrain()

    print("ADVANCED MARS TERRAIN GENERATED")

    print("Grid dimensions:", terrain["elevation"].shape)

    print(
        "Average elevation:",
        round(float(np.mean(terrain["elevation"])), 2)
    )

    print(
        "Average slope:",
        round(float(np.mean(terrain["slope"])), 2)
    )

    print(
        "Rock-covered cells:",
        int(np.sum(terrain["rock_map"]))
    )

    print(
        "Safe cells:",
        int(np.sum(terrain["terrain_class"] == 2))
    )

    print(
        "Difficult cells:",
        int(np.sum(terrain["terrain_class"] == 1))
    )

    print(
        "Impassable cells:",
        int(np.sum(terrain["terrain_class"] == 0))
    )
