
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

import numpy as np

from python_engine.terrain.generator import generate_terrain
from python_engine.navigation.astar import astar
from python_engine.analysis.rover_performance import (
    analyze_rover_performance
)


app = FastAPI(
    title="NASA Mars Rover Mission Control API",
    description="Configurable terrain intelligence and rover navigation API",
    version="2.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# --------------------------------------------------
# MISSION CONFIGURATION
# --------------------------------------------------

class MissionRequest(BaseModel):

    grid_size: int = Field(default=30, ge=5, le=150)

    seed: int = Field(default=42, ge=0, le=4294967295)

    start: tuple[int, int] = (0, 0)

    goal: tuple[int, int] = (29, 29)

    cell_size_m: float = Field(default=100.0, gt=0, le=10000)

    max_slope: float = Field(default=30.0, gt=0, le=90)

    max_roughness: float = Field(default=20.0, gt=0)

    max_hazard: float = Field(default=0.92, gt=0, le=1)


# --------------------------------------------------
# MISSION EXECUTION ENGINE
# --------------------------------------------------

def run_mission(request: MissionRequest):

    # 1. Generate terrain using user configuration

    terrain = generate_terrain(
        size=request.grid_size,
        seed=request.seed,
        cell_size_m=request.cell_size_m,
        max_slope=request.max_slope,
        max_roughness=request.max_roughness,
        max_hazard=request.max_hazard
    )

    rows, cols = terrain["traversable"].shape

    start = request.start
    intended_goal = request.goal

    # 2. Validate coordinates

    for point in (start, intended_goal):

        if not (
            0 <= point[0] < rows
            and 0 <= point[1] < cols
        ):
            raise HTTPException(
                status_code=400,
                detail="Start or destination is outside the terrain grid."
            )

    # 3. Find a traversable starting point if necessary

    if not terrain["traversable"][start]:

        safe_cells = list(
            zip(*terrain["traversable"].nonzero())
        )

        if not safe_cells:
            raise HTTPException(
                status_code=422,
                detail="No traversable terrain exists for this configuration."
            )

        start = min(
            safe_cells,
            key=lambda p: (
                (p[0] - start[0]) ** 2
                + (p[1] - start[1]) ** 2
            )
        )

    # 4. Attempt the requested destination

    path = None
    cost = None
    distance = None

    if terrain["traversable"][intended_goal]:

        path, cost, distance = astar(
            terrain,
            start,
            intended_goal
        )

    # 5. Find an alternative reachable destination if necessary

    if path is None:

        candidates = []

        for row in range(rows):
            for col in range(cols):

                candidate = (row, col)

                if not terrain["traversable"][candidate]:
                    continue

                if candidate == start:
                    continue

                target_distance = (
                    (row - intended_goal[0]) ** 2
                    + (col - intended_goal[1]) ** 2
                )

                candidates.append(
                    (target_distance, candidate)
                )

        candidates.sort(key=lambda item: item[0])

        for _, candidate in candidates:

            candidate_path, candidate_cost, candidate_distance = astar(
                terrain,
                start,
                candidate
            )

            if candidate_path is not None:

                intended_goal = candidate
                path = candidate_path
                cost = candidate_cost
                distance = candidate_distance
                break

    if path is None:
        raise HTTPException(
            status_code=422,
            detail="No reachable destination found for this mission."
        )

    # 6. Analyse rover performance

    performance = analyze_rover_performance(
        terrain,
        path,
        navigation_cost=cost,
        cell_size_m=request.cell_size_m
    )

    # 7. Return mission results

    return {
        "configuration": {
            "grid_size": request.grid_size,
            "seed": request.seed,
            "cell_size_m": request.cell_size_m,
            "max_slope": request.max_slope,
            "max_roughness": request.max_roughness,
            "max_hazard": request.max_hazard
        },

        "start": list(start),

        "goal": list(intended_goal),

        "path": [
            list(point) for point in path
        ],

        "terrain": {
            "elevation": terrain["elevation"].tolist(),
            "slope": terrain["slope"].tolist(),
            "roughness": terrain["roughness"].tolist(),
            "hazard": terrain["hazard"].tolist(),
            "rock_map": terrain["rock_map"].tolist(),
            "terrain_class": terrain["terrain_class"].tolist(),
            "traversable": terrain["traversable"].astype(int).tolist()
        },

        "performance": performance
    }


# --------------------------------------------------
# API ROUTES
# --------------------------------------------------

@app.get("/")
def home():

    return {
        "system": "NASA Mars Rover Mission Control",
        "status": "ONLINE",
        "api_version": "2.0"
    }


# Default mission - preserves existing dashboard compatibility

@app.get("/api/mission")
def get_mission():

    request = MissionRequest()

    return run_mission(request)


# Custom mission - accepts user configuration

@app.post("/api/mission")
def create_mission(request: MissionRequest):

    return run_mission(request)


@app.get("/api/health")
def health():

    return {
        "status": "operational",
        "engine": "Mars Rover Navigation Engine",
        "version": "2.0"
    }
