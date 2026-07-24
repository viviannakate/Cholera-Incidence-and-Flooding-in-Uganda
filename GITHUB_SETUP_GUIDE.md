# Step-by-Step: Publishing This Project to GitHub

This guide walks through getting this project onto GitHub and live as a public dashboard, from zero. Two paths are given — pick whichever you're more comfortable with.

---

## Option A: Using the GitHub website only (no command line)

1. **Create the repository**
   - Go to [github.com](https://github.com) → click the **+** icon (top right) → **New repository**
   - Name it e.g. `uganda-flooding-cholera`
   - Set to **Public** (required for free GitHub Pages)
   - Do **not** initialize with a README (you already have one) → **Create repository**

2. **Upload the files**
   - On your new empty repo page, click **uploading an existing file**
   - Unzip `uganda-flooding-cholera-github-project.zip` on your computer
   - Drag the *entire contents* of the `uganda_cholera_project` folder (not the folder itself — its contents: `data/`, `scripts/`, `docs/`, `outputs/`, `docs_background/`, `README.md`, etc.) into the upload box
   - GitHub preserves subfolders when you drag a folder structure in most modern browsers; if it doesn't, upload folder-by-folder
   - Scroll down, add a commit message like "Initial commit", click **Commit changes**

3. **Enable GitHub Pages**
   - Go to your repo → **Settings** tab → **Pages** (left sidebar, under "Code and automation")
   - Under **Build and deployment → Source**, choose **Deploy from a branch**
   - Under **Branch**, select `main` and folder `/docs` → **Save**
   - Wait ~30–60 seconds; refresh the Pages settings page and you'll see a green banner with your live URL:
     ```
     https://YOUR-USERNAME.github.io/uganda-flooding-cholera/
     ```

4. **Done.** Visit that URL — your interactive dashboard is live.

---

## Option B: Using Git on the command line

1. **Install Git** if you don't have it: [git-scm.com/downloads](https://git-scm.com/downloads)

2. **Create the repository on GitHub** (same as Option A, step 1), but leave it empty — no upload needed yet.

3. **From your terminal**, navigate to the unzipped project folder:
   ```bash
   cd path/to/uganda_cholera_project
   ```

4. **Initialize and push:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Uganda flooding & cholera hotspot analysis"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/uganda-flooding-cholera.git
   git push -u origin main
   ```
   (Replace `YOUR-USERNAME` with your actual GitHub username. You may be prompted to log in or provide a [personal access token](https://github.com/settings/tokens) instead of a password.)

5. **Enable GitHub Pages** — same as Option A, step 3.

6. **Future updates**: whenever you re-run `python scripts/analysis.py` and get new outputs, push the changes:
   ```bash
   git add .
   git commit -m "Update analysis with refreshed data"
   git push
   ```
   GitHub Pages automatically redeploys within about a minute.

---

## Verifying the Dashboard Works

Before pushing, you can preview the dashboard locally:

```bash
cd uganda_cholera_project/docs
python3 -m http.server 8000
```

Then open `http://localhost:8000` in your browser. You should see:
- Six summary stat cards at the top
- An interactive Leaflet map of Uganda with colored district markers
- A layer selector (cholera rate / flood frequency / LISA cluster / WASH score)
- Three Chart.js charts on the right (time series, top districts, WASH scatter)
- A sortable, searchable data table at the bottom

If the map or charts don't load locally, it's almost always because the browser is blocking `fetch('data.json')` under the `file://` protocol — this is why you need the `python3 -m http.server` step (or any local server) rather than double-clicking `index.html` directly. On the deployed GitHub Pages site, this isn't an issue.

---

## Customizing Before/After Publishing

- **Repo name**: any name works, it just changes the URL. Keep it lowercase with hyphens for a clean URL.
- **Custom domain**: if you own a domain, GitHub Pages supports it via **Settings → Pages → Custom domain**.
- **Updating the "Live Dashboard" link in README.md**: after your first successful deploy, edit the link at the top of `README.md` to your real URL, commit, and push.
- **Adding more years of data**: extend `data/uganda_flooding_cholera.xlsx` with new columns (e.g. `flood17`, `cas17`), add `2017` to the `YEARS` list in `scripts/analysis.py`, and re-run the pipeline. The dashboard's year dropdown will need a matching `<option value="2017">2017</option>` added in `docs/index.html`.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| Pages settings won't let you select `/docs` | Make sure you've pushed at least one commit containing the `docs/` folder first — the dropdown only shows folders that exist in the branch. |
| 404 at the Pages URL | Double-check the repo is **Public**, and that `docs/index.html` (lowercase) exists at that exact path. |
| Map is blank / grey | Check your browser's console (F12) for errors — usually a sign `data.json` failed to load (see local server note above), or an ad-blocker is blocking `openstreetmap.org` tiles. |
| Charts don't render | Make sure `docs/data.json` isn't empty/corrupted — re-run `python scripts/analysis.py` to regenerate it. |
