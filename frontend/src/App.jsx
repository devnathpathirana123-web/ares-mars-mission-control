import { useEffect, useMemo, useState } from "react";
import Plot from "react-plotly.js";
import "./App.css";

const API_URL = "http://localhost:8000";

const DEFAULT_CONFIG = {
  grid_size: 30,
  seed: 42,
  start_row: 0,
  start_col: 0,
  goal_row: 29,
  goal_col: 29,
  cell_size_m: 100,
  max_slope: 30,
  max_roughness: 20,
  max_hazard: 0.92,
};

const NAV_ITEMS = [
  { id: "overview", label: "Overview", icon: "◫" },
  { id: "terrain", label: "Terrain model", icon: "◇" },
  { id: "analysis", label: "Terrain analysis", icon: "▦" },
  { id: "performance", label: "Performance", icon: "⌁" },
  { id: "configuration", label: "Mission setup", icon: "⚙" },
];

function App() {
  const [mission, setMission] = useState(null);
  const [config, setConfig] = useState(DEFAULT_CONFIG);
  const [layer, setLayer] = useState("elevation");
  const [loading, setLoading] = useState(true);
  const [running, setRunning] = useState(false);
  const [error, setError] = useState("");
  const [activeSection, setActiveSection] = useState("overview");
  const [sidebarOpen, setSidebarOpen] = useState(false);

  useEffect(() => {
    async function loadInitialMission() {
      try {
        const response = await fetch(`${API_URL}/api/mission`);
        const data = await response.json();
        if (!response.ok) {
          throw new Error(data.detail || `API returned ${response.status}`);
        }
        setMission(data);
        if (data.configuration) {
          setConfig((previous) => ({
            ...previous,
            ...data.configuration,
            start_row: data.start[0],
            start_col: data.start[1],
            goal_row: data.goal[0],
            goal_col: data.goal[1],
          }));
        }
      } catch (err) {
        setError(err.message || "Unable to connect to the Python API.");
      } finally {
        setLoading(false);
      }
    }
    loadInitialMission();
  }, []);

  const terrain = mission?.terrain;
  const performance = mission?.performance;
  const path = mission?.path || [];
  const start = mission?.start || [0, 0];
  const goal = mission?.goal || [0, 0];

  const layerSettings = useMemo(() => {
    if (!terrain) return {};
    return {
      elevation: {
        title: "Elevation",
        unit: "m",
        data: terrain.elevation,
        colorscale: [
          [0, "#171d35"],
          [0.28, "#453d62"],
          [0.58, "#a45b48"],
          [0.82, "#e3a36c"],
          [1, "#f2dfb0"],
        ],
      },
      slope: {
        title: "Slope",
        unit: "degrees",
        data: terrain.slope,
        colorscale: "YlOrRd",
      },
      hazard: {
        title: "Hazard",
        unit: "index",
        data: terrain.hazard,
        colorscale: "Inferno",
      },
      roughness: {
        title: "Roughness",
        unit: "index",
        data: terrain.roughness,
        colorscale: "Viridis",
      },
      terrain_class: {
        title: "Terrain class",
        unit: "class",
        data: terrain.terrain_class,
        colorscale: "Portland",
      },
    };
  }, [terrain]);

  function updateConfig(event) {
    const { name, value } = event.target;
    setConfig((previous) => {
      const next = { ...previous, [name]: value };
      if (name === "grid_size") {
        const size = Number(value);
        if (Number.isInteger(size) && size >= 5) {
          next.goal_row = Math.min(Number(previous.goal_row), size - 1);
          next.goal_col = Math.min(Number(previous.goal_col), size - 1);
          next.start_row = Math.min(Number(previous.start_row), size - 1);
          next.start_col = Math.min(Number(previous.start_col), size - 1);
        }
      }
      return next;
    });
  }

  async function runMission(event) {
    event.preventDefault();
    const payload = {
      grid_size: Number(config.grid_size),
      seed: Number(config.seed),
      start: [Number(config.start_row), Number(config.start_col)],
      goal: [Number(config.goal_row), Number(config.goal_col)],
      cell_size_m: Number(config.cell_size_m),
      max_slope: Number(config.max_slope),
      max_roughness: Number(config.max_roughness),
      max_hazard: Number(config.max_hazard),
    };

    const n = payload.grid_size;
    if (!Number.isInteger(n) || n < 5 || n > 150) {
      setError("Grid size must be an integer between 5 and 150.");
      return;
    }
    if (!Number.isInteger(payload.seed) || payload.seed < 0 || payload.seed > 4294967295) {
      setError("Seed must be an integer from 0 to 4294967295.");
      return;
    }
    for (const [row, col] of [payload.start, payload.goal]) {
      if (!Number.isInteger(row) || !Number.isInteger(col) || row < 0 || col < 0 || row >= n || col >= n) {
        setError("Start and destination coordinates must be whole numbers inside the grid.");
        return;
      }
    }
    if (!Number.isFinite(payload.cell_size_m) || payload.cell_size_m <= 0 || payload.cell_size_m > 10000) {
      setError("Cell size must be greater than 0 and no more than 10000 metres.");
      return;
    }
    if (!Number.isFinite(payload.max_slope) || payload.max_slope <= 0 || payload.max_slope > 90) {
      setError("Maximum slope must be greater than 0 and no more than 90 degrees.");
      return;
    }
    if (!Number.isFinite(payload.max_roughness) || payload.max_roughness <= 0) {
      setError("Maximum roughness must be greater than 0.");
      return;
    }
    if (!Number.isFinite(payload.max_hazard) || payload.max_hazard <= 0 || payload.max_hazard > 1) {
      setError("Maximum hazard must be greater than 0 and no more than 1.");
      return;
    }

    setRunning(true);
    setError("");
    try {
      const response = await fetch(`${API_URL}/api/mission`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || `Mission failed: ${response.status}`);
      }
      setMission(data);
      setConfig((previous) => ({
        ...previous,
        start_row: data.start[0],
        start_col: data.start[1],
        goal_row: data.goal[0],
        goal_col: data.goal[1],
      }));
      document.getElementById("overview")?.scrollIntoView({ behavior: "smooth" });
      setActiveSection("overview");
    } catch (err) {
      setError(err.message || "Mission request failed.");
    } finally {
      setRunning(false);
    }
  }

  function navigateTo(id) {
    setActiveSection(id);
    setSidebarOpen(false);
    document.getElementById(id)?.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  if (loading) {
    return (
      <div className="boot-screen">
        <div className="boot-mark">M</div>
        <p className="eyebrow">MARS AUTONOMOUS SYSTEMS</p>
        <h1>Establishing mission link</h1>
        <div className="boot-track"><span /></div>
        <p className="muted">Connecting to Python navigation engine · localhost:8000</p>
      </div>
    );
  }

  if (!mission) {
    return (
      <div className="boot-screen">
        <div className="boot-mark warning">!</div>
        <p className="eyebrow">LINK FAILURE</p>
        <h1>Mission engine unavailable</h1>
        <p className="muted">{error}</p>
        <p className="muted">Start the FastAPI server on port 8000, then refresh this page.</p>
      </div>
    );
  }

  const rows = terrain.elevation.length;
  const cols = terrain.elevation[0].length;
  const routeRows = path.map(([r]) => r);
  const routeCols = path.map(([, c]) => c);
  const selectedLayer = layerSettings[layer];

  const plotLayout = {
    autosize: true,
    paper_bgcolor: "rgba(0,0,0,0)",
    plot_bgcolor: "rgba(0,0,0,0)",
    font: { family: "Inter, sans-serif", color: "#a9b8ca", size: 11 },
    margin: { l: 48, r: 25, t: 18, b: 42 },
  };

  return (
    <div className="app-shell">
      <aside className={`sidebar ${sidebarOpen ? "sidebar-open" : ""}`}>
        <div className="brand">
          <div className="brand-symbol"><span /></div>
          <div className="brand-copy">
            <strong>ARES<span>/</span></strong>
            <small>MARS OPERATIONS</small>
          </div>
        </div>

        <div className="sidebar-label">MISSION SYSTEM</div>
        <nav className="side-nav" aria-label="Main navigation">
          {NAV_ITEMS.map((item) => (
            <button
              key={item.id}
              className={`nav-item ${activeSection === item.id ? "active" : ""}`}
              onClick={() => navigateTo(item.id)}
            >
              <span className="nav-icon">{item.icon}</span>
              <span>{item.label}</span>
              {activeSection === item.id && <i />}
            </button>
          ))}
        </nav>

        <div className="sidebar-bottom">
          <div className="connection-card">
            <span className="connection-light" />
            <div>
              <strong>ENGINE ONLINE</strong>
              <small>API · PORT 8000</small>
            </div>
          </div>
          <div className="sidebar-version">ARES MISSION SYSTEM <span>v2.0</span></div>
        </div>
      </aside>

      {sidebarOpen && <button className="mobile-scrim" onClick={() => setSidebarOpen(false)} aria-label="Close navigation" />}

      <main className="main-area">
        <header className="topbar">
          <button className="mobile-menu" onClick={() => setSidebarOpen(true)} aria-label="Open navigation">☰</button>
          <div className="breadcrumb">OPERATIONS <span>/</span> MARS ROVER <span>/</span> <b>MISSION CONSOLE</b></div>
          <div className="topbar-right">
            <span className="utc-label">SIMULATION ENVIRONMENT</span>
            <span className="top-status"><i /> SYSTEM NOMINAL</span>
          </div>
        </header>

        <div className="page-content">
          <section className="page-heading" id="overview">
            <div>
              <p className="eyebrow">AUTONOMOUS EXPLORATION PROGRAM <span>·</span> MISSION 001</p>
              <h1>Mission <em>overview</em></h1>
              <p className="page-description">Terrain intelligence, autonomous path planning and rover performance monitoring.</p>
            </div>
            <div className="mission-chip">
              <span className="chip-dot" />
              LIVE SIMULATION
            </div>
          </section>

          <section className="metric-grid" aria-label="Mission summary">
            <MetricCard label="ROUTE DISTANCE" value={`${performance.distance_km.toFixed(3)}`} unit="KM" detail="Calculated path length" />
            <MetricCard label="ENERGY ESTIMATE" value={performance.estimated_energy_wh.toFixed(1)} unit="WH" detail="Model-based estimate" />
            <MetricCard label="MEAN SLOPE" value={performance.average_slope.toFixed(2)} unit="DEG" detail={`Maximum ${performance.maximum_slope.toFixed(2)}°`} />
            <MetricCard label="HAZARD EXPOSURE" value={performance.hazard_exposure.toFixed(4)} unit="INDEX" detail={`${performance.difficult_terrain_percentage.toFixed(1)}% difficult terrain`} />
          </section>

          <section className="panel-section" id="terrain">
            <div className="section-title-row">
              <div>
                <p className="eyebrow">01 / SPATIAL INTELLIGENCE</p>
                <h2>Terrain <em>topography</em></h2>
              </div>
              <div className="section-meta">
                <span className="meta-pip" /> {rows} × {cols} GRID
                <span className="meta-divider" />
                {mission.configuration?.cell_size_m ?? config.cell_size_m} M / CELL
              </div>
            </div>
            <div className="panel chart-panel terrain-panel">
              <div className="panel-topline">
                <div><span className="live-square" /> ELEVATION SURFACE</div>
                <span>3D DIGITAL TERRAIN MODEL</span>
              </div>
              <Plot
                data={[
                  {
                    type: "surface",
                    z: terrain.elevation,
                    colorscale: [[0, "#171d35"], [0.28, "#453d62"], [0.58, "#a45b48"], [0.82, "#e3a36c"], [1, "#f2dfb0"]],
                    showscale: true,
                    colorbar: { title: { text: "METRES", side: "right" }, tickfont: { color: "#8797aa", size: 9 }, titlefont: { color: "#8797aa", size: 9 }, thickness: 10 },
                    contours: { z: { show: true, usecolormap: true, project: { z: true } } },
                    hovertemplate: "ROW %{y}<br>COL %{x}<br>ELEVATION %{z:.2f} M<extra></extra>",
                  },
                  {
                    type: "scatter3d",
                    mode: "lines",
                    x: routeCols,
                    y: routeRows,
                    z: path.map(([r, c]) => terrain.elevation[r][c] + 8),
                    line: { color: "#ff765c", width: 7 },
                    name: "Rover route",
                    hoverinfo: "skip",
                  },
                  {
                    type: "scatter3d",
                    mode: "markers",
                    x: [start[1], goal[1]],
                    y: [start[0], goal[0]],
                    z: [terrain.elevation[start[0]][start[1]] + 10, terrain.elevation[goal[0]][goal[1]] + 10],
                    marker: { size: 6, color: ["#6be0bb", "#ff765c"], line: { color: "#101722", width: 1 } },
                    text: ["ROVER START", "TARGET"],
                    hovertemplate: "%{text}<extra></extra>",
                    name: "Mission points",
                  },
                ]}
                layout={{
                  ...plotLayout,
                  height: 500,
                  margin: { l: 0, r: 0, t: 12, b: 0 },
                  scene: {
                    bgcolor: "rgba(0,0,0,0)",
                    xaxis: { title: "COLUMN", color: "#718197", gridcolor: "#263345", zerolinecolor: "#263345", backgroundcolor: "rgba(0,0,0,0)" },
                    yaxis: { title: "ROW", color: "#718197", gridcolor: "#263345", zerolinecolor: "#263345", backgroundcolor: "rgba(0,0,0,0)" },
                    zaxis: { title: "ELEVATION (M)", color: "#718197", gridcolor: "#263345", zerolinecolor: "#263345", backgroundcolor: "rgba(0,0,0,0)" },
                    camera: { eye: { x: 1.55, y: 1.55, z: 1.05 } },
                  },
                }}
                config={{ responsive: true, displaylogo: false }}
                style={{ width: "100%" }}
                useResizeHandler
              />
              <div className="chart-footer">
                <span><i className="legend-dot start-dot" /> START {start.join(", ")}</span>
                <span><i className="legend-dot route-dot" /> COMPUTED ROUTE</span>
                <span><i className="legend-dot target-dot" /> TARGET {goal.join(", ")}</span>
              </div>
            </div>
          </section>

          <section className="panel-section" id="analysis">
            <div className="section-title-row">
              <div>
                <p className="eyebrow">02 / TERRAIN INTELLIGENCE</p>
                <h2>Environmental <em>analysis</em></h2>
              </div>
              <span className="section-meta">CELL-LEVEL DATA</span>
            </div>
            <div className="panel">
              <div className="layer-toolbar">
                <div className="layer-tabs">
                  {Object.entries(layerSettings).map(([key, item]) => (
                    <button key={key} className={layer === key ? "layer-tab selected" : "layer-tab"} onClick={() => setLayer(key)}>
                      {item.title}
                    </button>
                  ))}
                </div>
                <span className="layer-unit">DISPLAY: {selectedLayer.unit.toUpperCase()}</span>
              </div>
              <Plot
                data={[
                  {
                    type: "heatmap",
                    z: selectedLayer.data,
                    colorscale: selectedLayer.colorscale,
                    colorbar: { title: { text: selectedLayer.unit.toUpperCase() }, tickfont: { color: "#8797aa", size: 9 }, thickness: 10 },
                    hovertemplate: "ROW %{y}<br>COL %{x}<br>VALUE %{z:.3f}<extra></extra>",
                  },
                  {
                    type: "scatter",
                    mode: "lines",
                    x: routeCols,
                    y: routeRows,
                    line: { color: "#f7f8fc", width: 2.5 },
                    name: "Rover route",
                    hoverinfo: "skip",
                  },
                  {
                    type: "scatter",
                    mode: "markers",
                    x: [start[1], goal[1]],
                    y: [start[0], goal[0]],
                    marker: { size: 10, color: ["#6be0bb", "#ff765c"], line: { color: "#111a27", width: 1.5 } },
                    text: ["START", "DESTINATION"],
                    hovertemplate: "%{text}<extra></extra>",
                    name: "Mission points",
                  },
                ]}
                layout={{
                  ...plotLayout,
                  height: 430,
                  margin: { l: 48, r: 30, t: 12, b: 42 },
                  xaxis: { title: "COLUMN", autorange: "reversed", color: "#718197", gridcolor: "#263345" },
                  yaxis: { title: "ROW", autorange: "reversed", scaleanchor: "x", color: "#718197", gridcolor: "#263345" },
                }}
                config={{ responsive: true, displaylogo: false }}
                style={{ width: "100%" }}
                useResizeHandler
              />
            </div>
          </section>

          <section className="panel-section" id="performance">
            <div className="section-title-row">
              <div>
                <p className="eyebrow">03 / ROVER TELEMETRY</p>
                <h2>Mission <em>performance</em></h2>
              </div>
              <span className="section-meta">POST-ROUTE ANALYSIS</span>
            </div>
            <div className="performance-grid">
              <div className="panel performance-chart">
                <div className="panel-topline"><div>ROUTE CHARACTERISTICS</div><span>MEASURED VALUES</span></div>
                <Plot
                  data={[
                    { type: "bar", x: ["Mean slope", "Maximum slope"], y: [performance.average_slope, performance.maximum_slope], marker: { color: ["#f18a70", "#b85c54"] }, name: "Slope" },
                    { type: "bar", x: ["Mean hazard × 100", "Difficult terrain"], y: [performance.average_hazard * 100, performance.difficult_terrain_percentage], marker: { color: ["#67b9c8", "#8b83c8"] }, name: "Terrain risk" },
                  ]}
                  layout={{
                    ...plotLayout,
                    barmode: "group",
                    height: 330,
                    margin: { l: 48, r: 18, t: 12, b: 55 },
                    yaxis: { title: "VALUE", gridcolor: "#263345", zerolinecolor: "#344256" },
                    xaxis: { color: "#8c9bb0", gridcolor: "#263345" },
                    legend: { orientation: "h", y: 1.12, font: { color: "#a9b8ca", size: 10 } },
                  }}
                  config={{ responsive: true, displaylogo: false }}
                  style={{ width: "100%" }}
                  useResizeHandler
                />
              </div>
              <div className="panel telemetry-panel">
                <div className="panel-topline"><div>TELEMETRY SNAPSHOT</div><span>PYTHON ENGINE</span></div>
                <TelemetryRow label="Navigation cost" value={performance.navigation_cost.toFixed(3)} />
                <TelemetryRow label="Average roughness" value={performance.average_roughness.toFixed(3)} />
                <TelemetryRow label="Average hazard" value={performance.average_hazard.toFixed(4)} />
                <TelemetryRow label="Hazard exposure" value={performance.hazard_exposure.toFixed(4)} />
                <TelemetryRow label="Route distance" value={`${performance.distance_m.toFixed(1)} m`} />
                <TelemetryRow label="Estimated energy" value={`${performance.estimated_energy_wh.toFixed(2)} Wh`} />
                <p className="telemetry-note">Energy is an illustrative model estimate, not a calibrated rover power prediction.</p>
              </div>
            </div>
          </section>

          <section className="panel-section" id="configuration">
            <div className="section-title-row">
              <div>
                <p className="eyebrow">04 / CONTROL INPUTS</p>
                <h2>Mission <em>configuration</em></h2>
              </div>
              <span className="section-meta">ENGINE PARAMETERS</span>
            </div>
            <form className="panel config-panel" onSubmit={runMission}>
              <div className="config-block">
                <div className="config-block-heading"><span>01</span><div><strong>Environment</strong><small>Terrain grid and spatial resolution</small></div></div>
                <div className="config-fields">
                  <ConfigInput label="GRID SIZE" name="grid_size" value={config.grid_size} onChange={updateConfig} min="5" max="150" />
                  <ConfigInput label="RANDOM SEED" name="seed" value={config.seed} onChange={updateConfig} min="0" max="4294967295" />
                  <ConfigInput label="CELL SIZE · METRES" name="cell_size_m" value={config.cell_size_m} onChange={updateConfig} min="0.01" max="10000" step="any" />
                </div>
              </div>
              <div className="config-block">
                <div className="config-block-heading"><span>02</span><div><strong>Rover coordinates</strong><small>Grid positions for departure and target</small></div></div>
                <div className="config-fields">
                  <ConfigInput label="START ROW" name="start_row" value={config.start_row} onChange={updateConfig} min="0" max={Number(config.grid_size) - 1} />
                  <ConfigInput label="START COLUMN" name="start_col" value={config.start_col} onChange={updateConfig} min="0" max={Number(config.grid_size) - 1} />
                  <ConfigInput label="TARGET ROW" name="goal_row" value={config.goal_row} onChange={updateConfig} min="0" max={Number(config.grid_size) - 1} />
                  <ConfigInput label="TARGET COLUMN" name="goal_col" value={config.goal_col} onChange={updateConfig} min="0" max={Number(config.grid_size) - 1} />
                </div>
              </div>
              <div className="config-block">
                <div className="config-block-heading"><span>03</span><div><strong>Terrain constraints</strong><small>Traversability thresholds used by terrain generation</small></div></div>
                <div className="config-fields">
                  <ConfigInput label="MAXIMUM SLOPE · DEG" name="max_slope" value={config.max_slope} onChange={updateConfig} min="0.01" max="90" step="any" />
                  <ConfigInput label="MAXIMUM ROUGHNESS" name="max_roughness" value={config.max_roughness} onChange={updateConfig} min="0.01" step="any" />
                  <ConfigInput label="MAXIMUM HAZARD · 0–1" name="max_hazard" value={config.max_hazard} onChange={updateConfig} min="0.01" max="1" step="any" />
                </div>
              </div>
              {error && <div className="form-error"><strong>MISSION REQUEST FAILED</strong><span>{error}</span></div>}
              <div className="config-actions">
                <p>Executing a new mission replaces the current terrain and route analysis.</p>
                <button className="execute-button" type="submit" disabled={running}>
                  <span className="execute-icon">{running ? "…" : "▶"}</span>
                  {running ? "GENERATING MISSION" : "EXECUTE MISSION"}
                </button>
              </div>
            </form>
          </section>

          <footer className="app-footer">
            <span>ARES / MARS AUTONOMOUS SYSTEMS</span>
            <span>SIMULATED TERRAIN DATA · PYTHON NAVIGATION ENGINE</span>
            <span>MISSION CONSOLE v2.0</span>
          </footer>
        </div>
      </main>
    </div>
  );
}

function MetricCard({ label, value, unit, detail }) {
  return (
    <article className="metric-card">
      <div className="metric-label">{label}</div>
      <div className="metric-value">{value}<span>{unit}</span></div>
      <div className="metric-detail">{detail}</div>
      <div className="metric-accent" />
    </article>
  );
}

function ConfigInput({ label, name, value, onChange, min, max, step = "1" }) {
  return (
    <label className="config-field">
      <span>{label}</span>
      <input type="number" name={name} value={value} onChange={onChange} min={min} max={max} step={step} required />
    </label>
  );
}

function TelemetryRow({ label, value }) {
  return (
    <div className="telemetry-row">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

export default App;
