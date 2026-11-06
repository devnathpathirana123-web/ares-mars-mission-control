
import matplotlib.pyplot as plt
import numpy as np


def calculate_suitability(terrain):

    slope = terrain["slope"]
    roughness = terrain["roughness"]
    hazard = terrain["hazard"]

    slope_score = np.clip(1 - slope / 30, 0, 1)
    roughness_score = np.clip(1 - roughness / 20, 0, 1)
    hazard_score = np.clip(1 - hazard, 0, 1)

    suitability = (
        0.4 * slope_score
        + 0.3 * roughness_score
        + 0.3 * hazard_score
    )

    suitability[~terrain["traversable"]] = 0

    return suitability


def plot_terrain(
    terrain,
    path=None,
    start=None,
    goal=None,
    performance=None
):

    elevation = terrain["elevation"]
    slope = terrain["slope"]
    hazard = terrain["hazard"]
    terrain_class = terrain["terrain_class"]

    rows, cols = elevation.shape

    x, y = np.meshgrid(
        np.arange(cols),
        np.arange(rows)
    )

    fig = plt.figure(figsize=(20, 15))

    ax3d = fig.add_subplot(2, 3, 1, projection="3d")
    ax1 = fig.add_subplot(2, 3, 2)
    ax2 = fig.add_subplot(2, 3, 3)
    ax3 = fig.add_subplot(2, 3, 4)
    ax4 = fig.add_subplot(2, 3, 5)
    ax5 = fig.add_subplot(2, 3, 6)

    # 1. 3D TERRAIN

    surface = ax3d.plot_surface(
        x,
        y,
        elevation,
        cmap="terrain",
        linewidth=0,
        antialiased=True
    )

    ax3d.set_title("3D Martian Terrain")
    ax3d.set_xlabel("Grid Column")
    ax3d.set_ylabel("Grid Row")
    ax3d.set_zlabel("Elevation (m)")

    ax3d.view_init(elev=35, azim=-60)
    ax3d.set_box_aspect((1, 1, 0.45))

    fig.colorbar(
        surface,
        ax=ax3d,
        shrink=0.6,
        label="Elevation (m)"
    )

    # 2D ROUTE DATA

    if path is not None:

        route_rows = [point[0] for point in path]
        route_cols = [point[1] for point in path]

        route_heights = elevation[
            route_rows,
            route_cols
        ] + 3

        ax3d.plot(
            route_cols,
            route_rows,
            route_heights,
            color="blue",
            linewidth=3,
            label="Rover route"
        )

    if start is not None:

        ax3d.scatter(
            start[1],
            start[0],
            elevation[start] + 5,
            color="cyan",
            edgecolors="black",
            s=100,
            label="Start"
        )

    if goal is not None:

        ax3d.scatter(
            goal[1],
            goal[0],
            elevation[goal] + 5,
            color="red",
            edgecolors="black",
            s=100,
            label="Destination"
        )

    ax3d.legend()

    # 3. ELEVATION MAP

    image1 = ax1.imshow(
        elevation,
        cmap="terrain",
        origin="upper"
    )

    ax1.set_title("Elevation Map")

    fig.colorbar(image1, ax=ax1, label="Elevation (m)")

    # 4. SLOPE MAP

    image2 = ax2.imshow(
        slope,
        cmap="inferno",
        origin="upper"
    )

    ax2.set_title("Slope Map")

    fig.colorbar(image2, ax=ax2, label="Slope (degrees)")

    # 5. HAZARD MAP

    image3 = ax3.imshow(
        hazard,
        cmap="YlOrRd",
        vmin=0,
        vmax=1,
        origin="upper"
    )

    ax3.set_title("Environmental Hazard Map")

    fig.colorbar(image3, ax=ax3, label="Hazard score")

    # 6. TERRAIN CLASSIFICATION

    image4 = ax4.imshow(
        terrain_class,
        cmap="RdYlGn",
        vmin=0,
        vmax=2,
        origin="upper"
    )

    ax4.set_title("Terrain Classification")

    fig.colorbar(
        image4,
        ax=ax4,
        ticks=[0, 1, 2],
        label="0 = Impassable, 1 = Difficult, 2 = Safe"
    )

    # DISPLAY ROUTE ON ALL 2D MAPS

    for ax in (ax1, ax2, ax3, ax4):

        if path is not None:
            ax.plot(
                route_cols,
                route_rows,
                color="blue",
                linewidth=2,
                label="Rover route"
            )

        if start is not None:
            ax.scatter(
                start[1],
                start[0],
                color="cyan",
                edgecolors="black",
                s=80,
                label="Start"
            )

        if goal is not None:
            ax.scatter(
                goal[1],
                goal[0],
                color="red",
                edgecolors="black",
                s=80,
                label="Destination"
            )

        ax.set_xlabel("Grid Column")
        ax.set_ylabel("Grid Row")
        ax.legend(loc="upper right")

    # 7. ROVER PERFORMANCE PANEL

    ax5.axis("off")
    ax5.set_title(
        "ROVER PERFORMANCE REPORT",
        fontsize=14,
        fontweight="bold",
        pad=15
    )

    if performance is not None:

        report = [
            ("Route Distance",
             f"{performance['distance_km']:.3f} km"),

            ("Navigation Cost",
             f"{performance['navigation_cost']:.2f}"),

            ("Average Slope",
             f"{performance['average_slope']:.2f} degrees"),

            ("Maximum Slope",
             f"{performance['maximum_slope']:.2f} degrees"),

            ("Average Roughness",
             f"{performance['average_roughness']:.2f}"),

            ("Average Hazard",
             f"{performance['average_hazard']:.3f}"),

            ("Difficult Terrain",
             f"{performance['difficult_terrain_percentage']:.1f}%"),

            ("Hazard Exposure",
             f"{performance['hazard_exposure']:.4f}"),

            ("Estimated Energy",
             f"{performance['estimated_energy_wh']:.2f} Wh")
        ]

        y_position = 0.88

        for label, value in report:

            ax5.text(
                0.05,
                y_position,
                label,
                fontsize=11,
                fontweight="bold",
                transform=ax5.transAxes
            )

            ax5.text(
                0.95,
                y_position,
                value,
                fontsize=11,
                horizontalalignment="right",
                transform=ax5.transAxes
            )

            y_position -= 0.095

    else:

        ax5.text(
            0.5,
            0.5,
            "Performance data unavailable",
            ha="center",
            va="center",
            transform=ax5.transAxes
        )

    fig.suptitle(
        "NASA MARS ROVER — TERRAIN INTELLIGENCE SYSTEM",
        fontsize=18,
        fontweight="bold"
    )

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()
