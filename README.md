# ARES — Autonomous Rover Exploration System

**A Mars Terrain Intelligence, Rover Navigation and Mission Analysis Platform**

ARES is a Python-powered Mars rover mission simulation and terrain intelligence system. It generates terrain environments, evaluates surface conditions, identifies traversable regions and calculates navigation routes using the A* pathfinding algorithm.

The system combines a Python scientific computing backend with an interactive React dashboard to provide a mission-control-style interface for exploring terrain, planning rover routes and analysing mission performance.

> **Project status:** Local development version  
> **Deployment:** Runs locally on the user's computer  
> **Backend:** Python / FastAPI  
> **Frontend:** React / Vite  
> **Visualisation:** Plotly

---

# Table of Contents

1. [Project Overview](#1-project-overview)
2. [Key Features](#2-key-features)
3. [System Architecture](#3-system-architecture)
4. [Technology Stack](#4-technology-stack)
5. [Project Structure](#5-project-structure)
6. [System Requirements](#6-system-requirements)
7. [Installation Guide](#7-installation-guide)
8. [Running ARES](#8-running-ares)
9. [Using the Dashboard](#9-using-the-dashboard)
10. [Backend API Documentation](#10-backend-api-documentation)
11. [Terrain Generation and Analysis](#11-terrain-generation-and-analysis)
12. [Rover Navigation](#12-rover-navigation)
13. [Mission Performance Analysis](#13-mission-performance-analysis)
14. [Testing](#14-testing)
15. [Configuration](#15-configuration)
16. [Troubleshooting](#16-troubleshooting)
17. [Scientific Limitations](#17-scientific-limitations)
18. [Future Development](#18-future-development)
19. [Contributing](#19-contributing)
20. [License](#20-license)

---

# 1. Project Overview

Mars rover exploration presents several challenges, particularly when navigating unpredictable terrain.

A rover must account for:

- Elevation changes.
- Surface gradients and slopes.
- Uneven terrain and roughness.
- Potential surface hazards.
- Navigation distance and route efficiency.
- Energy consumption and mission constraints.

ARES addresses these challenges through a computational terrain analysis and route-planning environment.

The system generates a terrain grid, evaluates the characteristics of individual terrain cells, determines which locations are traversable and applies a weighted A* algorithm to identify a suitable route between a starting position and a destination.

The resulting mission is visualised through an interactive dashboard containing terrain maps, 3D surface representations, route overlays and rover performance statistics.

ARES is designed as an extensible platform for experimenting with autonomous navigation and terrain intelligence.

# 2. Key Features

## 2.1 Terrain Generation

ARES generates configurable terrain environments using NumPy.

Each terrain environment contains several datasets:

- Elevation.
- Slope.
- Surface roughness.
- Hazard intensity.
- Rock distribution.
- Terrain classification.
- Traversability.

Terrain generation can be configured using parameters such as grid dimensions, random seed, cell size and terrain safety thresholds.

## 2.2 Terrain Intelligence

The terrain analysis system evaluates individual grid cells using multiple environmental characteristics.

The system identifies difficult and traversable regions based on configured terrain constraints.

## 2.3 Weighted A* Navigation

ARES uses a weighted A* pathfinding algorithm to calculate rover navigation routes.

The algorithm evaluates movement costs while accounting for terrain characteristics and movement restrictions.

It supports:

- Eight-directional grid movement.
- Diagonal movement restrictions.
- Terrain-dependent movement costs.
- Hazard-aware route planning.
- Slope and roughness penalties.
- Route distance and navigation cost calculations.

## 2.4 Interactive 3D Terrain Visualisation

The dashboard includes an interactive 3D representation of the generated terrain.

Users can explore the terrain surface and examine its spatial characteristics.

## 2.5 Scientific Heatmaps

ARES provides interactive terrain heatmaps for examining:

- Elevation.
- Slope.
- Roughness.
- Hazard intensity.
- Terrain classification.

These visualisations help identify challenging terrain and understand the relationship between environmental conditions and rover navigation.

## 2.6 Rover Performance Analysis

The mission analysis system calculates several performance indicators, including:

- Total navigation distance.
- Navigation cost.
- Average slope.
- Maximum slope.
- Average roughness.
- Average hazard intensity.
- Difficult terrain percentage.
- Hazard exposure.
- Estimated energy consumption.

## 2.7 Configurable Mission Parameters

Users can configure mission parameters through the dashboard, including:

- Terrain grid size.
- Random seed.
- Starting coordinates.
- Destination coordinates.
- Terrain cell size.
- Maximum permitted slope.
- Maximum roughness threshold.
- Maximum hazard threshold.

---

# 3. System Architecture

ARES uses a two-part architecture.

### Backend — Python

The backend handles the computational components of the system.

It is responsible for:

1. Generating terrain.
2. Analysing terrain characteristics.
3. Identifying traversable locations.
4. Calculating navigation routes.
5. Analysing rover performance.
6. Returning mission data through a REST API.

### Frontend — React

The frontend provides the user interface.

It is responsible for:

1. Displaying mission information.
2. Requesting mission data from the backend.
3. Rendering 3D terrain visualisations.
4. Displaying terrain heatmaps.
5. Showing navigation routes.
6. Presenting mission performance statistics.
7. Sending updated mission configurations to the backend.

### Communication

The frontend communicates with the backend through HTTP requests.

The local development configuration uses:

- Frontend: `http://localhost:5173`
- Backend: `http://localhost:8000`

The backend exposes its API through FastAPI.

---

# 4. Technology Stack

| Component | Technology |
|---|---|
| Programming language | Python |
| Numerical computation | NumPy |
| Backend framework | FastAPI |
| API validation | Pydantic |
| ASGI server | Uvicorn |
| Frontend framework | React |
| Frontend tooling | Vite |
| Frontend language | JavaScript |
| Scientific visualisation | Plotly |
| Pathfinding | Weighted A* |
| Version control | Git |
| Repository hosting | GitHub |

---

# 5. Project Structure

```text
mars-mission-control/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── synthetic/
│   └── real/
│
├── research/
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   │
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
│
├── python_engine/
│   ├── __init__.py
│   │
│   ├── terrain/
│   │   ├── __init__.py
│   │   └── generator.py
│   │
│   ├── navigation/
│   │   ├── __init__.py
│   │   └── astar.py
│   │
│   ├── analysis/
│   │   ├── rover_performance.py
│   │   └── suitability.py
│   │
│   ├── api/
│   │   └── server.py
│   │
│   └── main.py
│
└── tests/
    └── test_astar.py
```

### Important directories

**`python_engine/terrain/`**

Contains the terrain generation algorithms and environmental data calculations.

**`python_engine/navigation/`**

Contains the A* pathfinding implementation.

**`python_engine/analysis/`**

Contains terrain suitability and rover performance analysis.

**`python_engine/api/`**

Contains the FastAPI application used by the frontend.

**`frontend/`**

Contains the React dashboard and interactive visualisation components.

**`tests/`**

Contains automated tests for the navigation system.

**`data/`**

Reserved for terrain datasets and other project data.

---

# 6. System Requirements

Before installing ARES, ensure the following software is available.

| Software | Purpose |
|---|---|
| Python 3.12 or compatible version | Backend execution |
| Node.js LTS | Frontend execution |
| npm | JavaScript package management |
| Git | Repository cloning and version control |
| Visual Studio Code | Recommended development environment |

Python 3.12 is a recommended starting point for a clean installation. Other versions may work depending on dependency compatibility.

Check your installations:

### Check Python

```bash
python3 --version
```

### Check Node.js

```bash
node --version
```

### Check npm

```bash
npm --version
```

### Check Git

```bash
git --version
```

If these commands return version numbers, the corresponding software is installed.

---

# 7. Installation Guide

The following instructions explain how to download, configure and install ARES from scratch.

## Step 1 — Clone the repository

Open a terminal and navigate to the directory where you want to store the project.

Clone the repository:

```bash
git clone https://github.com/devnathpathirana123-web/ares-mars-mission-control.git
```

Enter the project directory:

```bash
cd ares-mars-mission-control
```

## Step 2 — Create a Python virtual environment

A virtual environment isolates the Python dependencies used by ARES from other Python projects.

On macOS and Linux:

```bash
python3 -m venv .venv
```

On Windows:

```bash
py -m venv .venv
```

## Step 3 — Activate the virtual environment

On macOS and Linux:

```bash
source .venv/bin/activate
```

On Windows Command Prompt:

```cmd
.venv\Scripts\activate.bat
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

When activated, the terminal should display `(.venv)` at the beginning of the command prompt.

## Step 4 — Upgrade pip

Upgrade the Python package installer:

```bash
python -m pip install --upgrade pip
```

## Step 5 — Install Python dependencies

Install the backend dependencies:

```bash
pip install -r requirements.txt
```

Wait until the installation finishes.

## Step 6 — Install frontend dependencies

Navigate into the frontend directory:

```bash
cd frontend
```

Install the JavaScript dependencies:

```bash
npm install
```

This reads `package.json` and installs the required frontend packages.

Once installation is complete, return to the main project directory:

```bash
cd ..
```

ARES is now installed.

---

# 8. Running ARES

ARES requires two separate development servers:

1. The Python backend.
2. The React frontend.

Both must be running simultaneously for the complete dashboard to function.

## Step 1 — Start the backend

Open a terminal in the main project directory.

Activate the virtual environment if it is not already active:

```bash
source .venv/bin/activate
```

Start the FastAPI server:

```bash
uvicorn python_engine.api.server:app --reload --port 8000
```

On successful startup, the terminal should display a message indicating that Uvicorn is running.

The backend is now accessible at:

```text
http://localhost:8000
```

### Access the API documentation

Open:

```text
http://localhost:8000/docs
```

This opens the automatically generated FastAPI Swagger interface.

You can inspect and test the available API endpoints from this page.

**Keep this terminal open while using ARES.**

## Step 2 — Start the frontend

Open a second terminal in Visual Studio Code.

Navigate to the frontend directory:

```bash
cd frontend
```

Start the Vite development server:

```bash
npm run dev
```

The terminal should display a local development URL, normally:

```text
http://localhost:5173
```

Open this address in your browser.

The ARES Mission Control dashboard should now load.

**Keep this terminal open as well.**

## Step 3 — Access ARES

Open:

```text
http://localhost:5173
```

Both servers must remain active.

The backend processes mission calculations, while the frontend displays the results.

### Stopping the servers

To stop either server, focus its terminal and press:

```text
CTRL + C
```

On macOS, this is also `Control + C`, not Command + C.

---

# 9. Using the Dashboard

Once ARES has started, the dashboard provides access to the mission analysis environment.

### Mission Overview

Displays key mission information and performance indicators.

### Terrain Visualisation

Provides an interactive 3D representation of the generated terrain.

Users can rotate, zoom and inspect the terrain surface.

### Terrain Analysis

Displays heatmaps representing different terrain properties.

Available layers include elevation, slope, roughness, hazard intensity and terrain classification.

### Navigation

Displays the calculated rover route across the terrain grid.

The route is generated by the Python navigation engine.

### Mission Performance

Displays calculated mission indicators such as navigation distance, terrain difficulty and estimated energy consumption.

### Mission Configuration

Allows users to change the terrain generation and navigation parameters.

Submitting a new configuration sends a request to the backend, which generates and analyses a new mission.

---

# 10. Backend API Documentation

ARES uses FastAPI to expose its computational functionality through a REST API.

The default backend address is:

```text
http://localhost:8000
```

## Available endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/health` | Checks backend availability |
| GET | `/api/mission` | Generates or returns a default mission |
| POST | `/api/mission` | Generates a mission using custom parameters |
| GET | `/docs` | Interactive Swagger documentation |

## Health check

Request:

```http
GET /api/health
```

Used to check whether the backend is responding.

## Default mission

Request:

```http
GET /api/mission
```

Generates the default mission configuration.

## Custom mission

Request:

```http
POST /api/mission
```

Example request body:

```json
{
  "grid_size": 50,
  "seed": 123,
  "start": [0, 0],
  "goal": [49, 49],
  "cell_size_m": 100,
  "max_slope": 25,
  "max_roughness": 15,
  "max_hazard": 0.8
}
```

### Parameter descriptions

| Parameter | Description |
|---|---|
| `grid_size` | Width and height of the terrain grid |
| `seed` | Random seed used for terrain generation |
| `start` | Rover starting coordinates |
| `goal` | Intended destination coordinates |
| `cell_size_m` | Physical distance represented by each grid cell |
| `max_slope` | Maximum slope threshold |
| `max_roughness` | Maximum roughness threshold |
| `max_hazard` | Maximum hazard threshold |

The backend returns the mission configuration, navigation path, terrain datasets and rover performance results.

For the complete request and response schemas, use:

```text
http://localhost:8000/docs
```

---

# 11. Terrain Generation and Analysis

The terrain generation module is located at:

```text
python_engine/terrain/generator.py
```

The primary terrain generation function is:

```python
generate_terrain(
    size=30,
    seed=42,
    cell_size_m=100.0,
    max_slope=30.0,
    max_roughness=20.0,
    max_hazard=0.92
)
```

## Terrain datasets

### Elevation

Represents the height of each terrain cell.

### Slope

Represents the gradient of the terrain surface.

Steeper terrain generally increases rover navigation difficulty.

### Roughness

Represents local surface variation.

Higher roughness values indicate more uneven terrain.

### Hazard intensity

Represents the generated hazard level associated with a terrain cell.

### Rock distribution

Represents the distribution of generated rock features.

### Terrain classification

Categorises terrain cells according to their characteristics.

### Traversability

Identifies whether a terrain cell satisfies the configured navigation constraints.

These datasets are used by the navigation algorithm and the dashboard visualisations.

---

# 12. Rover Navigation

The navigation algorithm is located at:

```text
python_engine/navigation/astar.py
```

ARES uses a weighted A* pathfinding algorithm.

A* combines the known cost of reaching a location with an estimated remaining cost to the destination.

The general evaluation function is:

\[
f(n)=g(n)+h(n)
\]

Where:

- \(f(n)\) is the estimated total route cost.
- \(g(n)\) is the accumulated cost from the starting location.
- \(h(n)\) is the estimated remaining cost to the destination.

ARES extends basic grid-based pathfinding by incorporating terrain-dependent movement costs.

These include:

- Slope penalties.
- Roughness penalties.
- Hazard penalties.
- Terrain suitability.
- Terrain classification penalties.

The algorithm supports eight-directional movement while preventing diagonal corner-cutting through blocked cells.

The resulting route is returned to the backend for performance analysis and dashboard visualisation.

If the intended destination cannot be reached, the mission logic attempts to identify an alternative reachable destination.

---

# 13. Mission Performance Analysis

The performance analysis module is located at:

```text
python_engine/analysis/rover_performance.py
```

It evaluates the calculated route and produces mission performance indicators.

### Distance

Calculated from the movement between consecutive route cells and the configured cell size.

### Average slope

Represents the mean slope encountered along the route.

### Maximum slope

Identifies the steepest terrain encountered.

### Average roughness

Represents the average surface roughness along the route.

### Average hazard

Represents the average hazard intensity encountered.

### Difficult terrain percentage

Represents the proportion of route cells classified as difficult.

### Hazard exposure

A route-level indicator combining average hazard intensity and navigation distance.

### Estimated energy consumption

An illustrative energy estimate based on route distance and terrain characteristics.

The energy model uses simplified assumptions and should not be interpreted as a physically calibrated model of an actual Mars rover.

---

# 14. Testing

ARES includes automated tests for the navigation system.

The tests are located in:

```text
tests/
```

## Install pytest

If it is not already installed:

```bash
pip install pytest
```

## Run the test suite

From the main project directory:

```bash
pytest
```

To display more detailed test output:

```bash
pytest -v
```

The tests help verify the behaviour of the navigation implementation.

## Test terrain generation independently

You can also run a simple terrain generation check:

```bash
python -c "from python_engine.terrain.generator import generate_terrain; t = generate_terrain(size=50, seed=123, cell_size_m=100, max_slope=25, max_roughness=15, max_hazard=0.8); print('GRID:', t['elevation'].shape); print('TRAVERSABLE:', t['traversable'].sum())"
```

This generates a 50 × 50 terrain grid and prints its dimensions and number of traversable cells.

## Run the standalone simulation

From the main project directory:

```bash
python python_engine/main.py
```

This runs the standalone Python simulation and its associated mission analysis.

---

# 15. Configuration

ARES supports several configurable terrain and mission parameters.

The main configuration options include:

| Parameter | Default | Description |
|---|---:|---|
| Grid size | 30 | Terrain grid dimensions |
| Random seed | 42 | Controls terrain generation |
| Cell size | 100 m | Physical cell resolution |
| Maximum slope | 30° | Slope threshold |
| Maximum roughness | 20 | Roughness threshold |
| Maximum hazard | 0.92 | Hazard threshold |

The API also validates parameter ranges to prevent invalid mission configurations.

For example, the grid size is restricted to a supported range and the maximum slope cannot exceed 90 degrees.

The exact accepted values are defined in the FastAPI request model.

---

# 16. Troubleshooting

## Problem: `uvicorn: command not found`

The Python virtual environment may not be activated, or the dependencies may not have been installed.

Activate the environment:

```bash
source .venv/bin/activate
```

Reinstall the dependencies:

```bash
pip install -r requirements.txt
```

## Problem: `ModuleNotFoundError`

Ensure that you are running backend commands from the main project directory.

Also verify that the virtual environment is activated.

## Problem: Port 8000 is already in use

Another process may already be using the backend port.

Stop the existing server or use another port:

```bash
uvicorn python_engine.api.server:app --reload --port 8001
```

If you change the backend port, update the frontend API address accordingly.

## Problem: Frontend cannot connect to the backend

Check the following:

1. The backend server is running.
2. The frontend is using the correct backend URL.
3. The FastAPI CORS configuration permits the frontend origin.
4. The API endpoint is accessible through the browser.

Test the backend directly:

```text
http://localhost:8000/api/health
```

## Problem: `npm: command not found`

Node.js may not be installed correctly.

Check:

```bash
node --version
npm --version
```

Install Node.js LTS if necessary.

## Problem: Frontend dependencies are missing

Navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies again:

```bash
npm install
```

## Problem: Changes are not appearing

Vite normally refreshes the frontend automatically.

If necessary, stop the frontend server with `CTRL + C` and restart it:

```bash
npm run dev
```

## Problem: Python package installation fails

Check your Python version:

```bash
python --version
```

If the installed Python version is incompatible with a dependency, try using Python 3.12 and recreate the virtual environment.

---

# 17. Scientific Limitations

ARES is an experimental terrain intelligence and rover navigation platform.

The current terrain generator creates synthetic terrain environments for testing and simulation.

These environments should not be interpreted as actual measurements of the Martian surface.

The current system does not claim to reproduce the complete physical behaviour of a real Mars rover.

In particular:

- Terrain generation is synthetic.
- Hazard values are generated simulation parameters.
- Terrain classification uses configured thresholds.
- Navigation costs are algorithmic estimates.
- Energy consumption is based on illustrative assumptions.
- The system does not currently constitute a flight-certified rover navigation system.

Real mission deployment would require validated terrain datasets, calibrated rover dynamics, environmental modelling and extensive testing.

---

# 18. Future Development

Potential future improvements include:

- Integration of real Mars terrain datasets.
- Digital elevation model processing.
- Improved terrain classification.
- More advanced rover movement models.
- Energy-aware route optimisation.
- Dynamic hazard avoidance.
- Improved mission planning algorithms.
- Comparative analysis of different navigation strategies.
- Expanded automated testing.
- Additional scientific visualisation layers.

These developments would extend ARES from a synthetic terrain simulation into a more comprehensive planetary exploration research environment.

---

# 19. Contributing

Contributions, suggestions and improvements are welcome.

To contribute:

1. Fork the repository.
2. Create a new feature branch.
3. Implement your changes.
4. Test the implementation.
5. Submit a pull request.

Example:

```bash
git checkout -b feature/new-terrain-model
```

Commit your changes:

```bash
git add .
git commit -m "Add new terrain model"
```

Push the branch:

```bash
git push origin feature/new-terrain-model
```

Then create a pull request through GitHub.

Please ensure that new features are tested and that changes do not break existing functionality.

---

# 20. License

No open-source license has been specified yet. Please check the repository for a `LICENSE` file before reusing or redistributing this project.

---

**ARES — Autonomous Rover Exploration System**

*Advancing autonomous navigation and terrain intelligence for planetary exploration.*
