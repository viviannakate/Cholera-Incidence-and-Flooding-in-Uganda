# 🌊 Uganda Flooding & Cholera Hotspot Analysis (2011–2016)

A spatiotemporal analysis of the relationship between flooding, WASH (water, sanitation, hygiene) coverage, and cholera burden across Uganda's 112 districts, with an interactive web dashboard.

**[Live Dashboard →](https://viviannakate.github.io/Cholera-Incidence-and-Flooding-in-Uganda/)**

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)

---

## 📖 Background

Cholera is endemic in Uganda, with recurring outbreaks concentrated in a predictable set of high-risk districts — particularly those near lakes, rivers, and international borders. Flooding is a well-documented driver of outbreaks: it overwhelms pit latrines, contaminates water sources, displaces populations into crowded conditions, and damages WASH infrastructure. Recent outbreaks in Bududa (2019, following landslides), Kayunga (2023, following flooding near the Nile), and Hoima (2015, Lake Albert) all illustrate this pathway directly.

Full background, references, and public health context: **[docs_background/BACKGROUND.md](docs_background/BACKGROUND.md)**

## ❓ What This Project Does

Using six years (2011–2016) of district-level data on flood occurrence, cholera case counts, population, and WASH coverage, this project:

1. **Reshapes** wide-format annual data into an analysis-ready long format
2. **Computes spatial hotspots** using a LISA-style (Local Indicators of Spatial Association) cluster classification, identifying districts that are both high-burden themselves *and* surrounded by high-burden neighbors
3. **Generates static charts and maps** (time series, top-district rankings, WASH scatter plots, cluster maps, regional breakdowns)
4. **Builds an interactive dashboard** (Leaflet.js + Chart.js) for exploring the map, trends, and full district data table in a browser — no server or build step required

## 📁 Repository Structure

```
uganda-flooding-cholera/
├── data/
│   └── uganda_flooding_cholera.xlsx     # Raw source data (112 districts × 19 vars)
├── scripts/
│   ├── analysis.py                      # Main reproducible analysis pipeline
│   └── district_coords.py               # District centroid lookup (lat/lon)
├── outputs/
│   ├── district_hotspot_analysis.csv    # Full district-level results + LISA classes
│   ├── uganda_long_format.csv           # District-year long-format panel data
│   ├── dashboard_data.json              # JSON feed (copy of docs/data.json)
│   └── *.png                            # Static charts & maps (300 DPI)
├── docs/                                # ⭐ GitHub Pages source (the dashboard)
│   ├── index.html                       # Interactive dashboard (self-contained)
│   └── data.json                        # Data feed consumed by the dashboard
├── docs_background/
│   └── BACKGROUND.md                    # Cholera & flooding background/context
├── requirements.txt
├── LICENSE
└── README.md
```

## 📊 Data Dictionary

| Column | Description |
|---|---|
| `dist_id` | District numeric ID |
| `district` | District name (2016 boundaries, 112 districts) |
| `flood11`–`flood16` | Binary flood indicator per year (1 = flooding reported, 2011–2016) |
| `cas11`–`cas16` | Cholera case counts per year (2011–2016) |
| `Popl` | District population |
| `wat_cov` | Water coverage (%) |
| `san_cov` | Sanitation coverage (%) |
| `hw_cov` | Handwashing coverage (%) |
| `score` | Composite WASH score |

Derived fields (in `outputs/district_hotspot_analysis.csv`): `total_flood_years`, `total_cases`, `cases_per_100k`, `region`, `neighbor_mean_rate`, `lisa_class`, `local_morans_i`.

## 🔥 Hotspot Methodology

District cholera rates are highly skewed (75/112 districts reported zero cases over the period), so a global spatial-autocorrelation test is less informative than a **local cluster approach**. We use a **LISA-style quadrant classification**:

1. For each district, compute the mean cholera rate of its **5 nearest neighboring districts** (by haversine distance between centroids) — this is the spatial lag.
2. Classify each district relative to the **national median** rate and the **median neighbor rate**:
   - **High-High (Hotspot Cluster)**: high rate, surrounded by high-rate neighbors → priority intervention zone
   - **Low-Low (Coldspot Cluster)**: low rate, surrounded by low-rate neighbors
   - **High-Low / Low-High (Outliers)**: a district that diverges from its surroundings
3. A standardized **Local Moran's I** value is also computed for each district as a continuous measure of cluster strength.

This approach identified **31 districts as High-High hotspot clusters**, concentrated in the Lake Albert basin (Buliisa, Hoima, Ntoroko, Bundibugyo), the Nebbi/West Nile corridor, and parts of the eastern highlands (Bulambuli, Bududa, Butaleja, Mbale).

> **Note on coordinates**: district boundary polygon shapefiles were not available in this environment, so the maps use **approximate district centroids** (compiled from public geographic reference data) rather than full choropleth polygons. This is sufficient for bubble/point-based hotspot mapping and cluster analysis, but is *not* survey-grade GIS data. See [Limitations](#-limitations) below.

## 🚀 Reproducing the Analysis

```bash
git clone https://github.com/YOUR-USERNAME/uganda-flooding-cholera.git
cd uganda-flooding-cholera
pip install -r requirements.txt
python scripts/analysis.py
```

This regenerates everything in `outputs/` and refreshes `docs/data.json` (the dashboard's data feed) from the raw Excel file in `data/`.

## 🖥️ Interactive Dashboard

The dashboard (`docs/index.html`) is a **fully static, client-side** page — it fetches `docs/data.json` and renders everything in-browser with Leaflet.js (map) and Chart.js (charts). No backend, database, or build step is required, which is what makes it deployable directly via GitHub Pages.

Features:
- Switch map layer between cholera rate, flood frequency, LISA cluster class, and WASH score
- Filter by year or view 2011–2016 cumulative totals
- Search/zoom to a specific district
- Sortable, filterable full data table
- Linked charts: flooding vs. cases time series, top-10 burden districts, WASH-vs-cholera scatter

To preview locally before pushing:
```bash
cd docs
python3 -m http.server 8000
# open http://localhost:8000 in a browser
```

## 🌐 Deploying to GitHub Pages

1. **Create a new GitHub repository** (e.g. `uganda-flooding-cholera`) and push this project:
   ```bash
cd Cholera-Incidence-and-Flooding-in-Uganda
git init
git add .
git commit -m "Initial commit: Uganda flooding & cholera hotspot analysis"
git branch -M main
git remote add origin https://github.com/viviannakate/Cholera-Incidence-and-Flooding-in-Uganda.git
git push -u origin main
 ```

2. **Enable GitHub Pages**:
   - Go to your repo on GitHub → **Settings** → **Pages** (left sidebar)
   - Under "Build and deployment" → **Source**, select **Deploy from a branch**
   - Under **Branch**, select `main` and folder **`/docs`** → **Save**

3. **Wait ~1 minute**, then your dashboard will be live at:
   ```
   https://YOUR-USERNAME.github.io/uganda-flooding-cholera/
   ```

4. Update the live link at the top of this README once deployed.

> No GitHub Actions, Node build, or Jekyll config needed — `docs/index.html` is plain HTML/CSS/JS served as-is.

## ⚠️ Limitations

- District centroid coordinates are **approximate** (visualization purposes only), not authoritative GIS boundaries — a full choropleth map with true district polygons would require a shapefile/GeoJSON source (e.g. [geoBoundaries](https://www.geoboundaries.org) UGA ADM2) merged via GeoPandas.
- The dataset covers **2011–2016 only** and uses **2016 district boundaries** (112 districts); Uganda has since created additional districts (135+ as of 2020), so figures are not directly comparable to more recent district-level statistics.
- Binary yearly flood indicators do not capture flood *severity* or *duration*, only occurrence.
- WASH coverage figures are **district averages** and may mask sub-district (sub-county/parish) heterogeneity that matters more for actual outbreak risk.
- Correlational, not causal — see `docs_background/BACKGROUND.md` for why simple WASH-cholera correlations are weak despite a well-documented causal pathway.

## 📄 License

MIT — see [LICENSE](LICENSE). Cite the underlying surveillance/WASH data source appropriately if reused.
