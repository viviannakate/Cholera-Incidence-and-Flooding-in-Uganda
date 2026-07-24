"""
Uganda Flooding & Cholera Hotspot Analysis
============================================
Reproducible analysis pipeline: reshapes raw district-level data (2011-2016),
computes hotspot statistics (quartile classification + LISA spatial clusters),
generates static charts/maps, and builds the JSON feed used by the interactive
dashboard in docs/index.html.

Usage:
    python scripts/analysis.py

Requires: pandas, numpy, matplotlib, seaborn, scipy (see requirements.txt)
"""
import json
import sys
from math import radians, cos, sin, asin, sqrt
from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from district_coords import DISTRICT_COORDS  # noqa: E402

DATA_XLSX = ROOT / "data" / "uganda_flooding_cholera.xlsx"
OUT = ROOT / "outputs"
DOCS = ROOT / "docs"
OUT.mkdir(exist_ok=True)
DOCS.mkdir(exist_ok=True)

sns.set_style("whitegrid")

REGION_MAP = {
    'Abim': 'Northern', 'Adjumani': 'Northern', 'Agago': 'Northern', 'Alebtong': 'Northern', 'Amolatar': 'Northern',
    'Amudat': 'Eastern', 'Amuria': 'Eastern', 'Amuru': 'Northern', 'Apac': 'Northern', 'Arua': 'Northern',
    'Budaka': 'Eastern', 'Bududa': 'Eastern', 'Bugiri': 'Eastern', 'Buhweju': 'Western', 'Buikwe': 'Central',
    'Bukedea': 'Eastern', 'Bukomansimbi': 'Central', 'Bukwa': 'Eastern', 'Bulambuli': 'Eastern', 'Buliisa': 'Western',
    'Bundibugyo': 'Western', 'Bushenyi': 'Western', 'Busia': 'Eastern', 'Butaleja': 'Eastern', 'Butambala': 'Central',
    'Buvuma': 'Central', 'Buyende': 'Eastern', 'Dokolo': 'Northern', 'Gomba': 'Central', 'Gulu': 'Northern',
    'Hoima': 'Western', 'Ibanda': 'Western', 'Iganga': 'Eastern', 'Isingiro': 'Western', 'Jinja': 'Eastern',
    'Kaabong': 'Northern', 'Kabale': 'Western', 'Kabarole': 'Western', 'Kaberamaido': 'Eastern', 'Kalangala': 'Central',
    'Kaliro': 'Eastern', 'Kalungu': 'Central', 'Kampala': 'Central', 'Kamuli': 'Eastern', 'Kamwenge': 'Western',
    'Kanungu': 'Western', 'Kapchorwa': 'Eastern', 'Kasese': 'Western', 'Katakwi': 'Eastern', 'Kayunga': 'Central',
    'Kibaale': 'Western', 'Kiboga': 'Central', 'Kibuku': 'Eastern', 'Kiruhura': 'Western', 'Kiryandongo': 'Western',
    'Kisoro': 'Western', 'Kitgum': 'Northern', 'Koboko': 'Northern', 'Kole': 'Northern', 'Kotido': 'Northern',
    'Kumi': 'Eastern', 'Kween': 'Eastern', 'Kyankwanzi': 'Central', 'Kyegegwa': 'Western', 'Kyenjojo': 'Western',
    'Lamwo': 'Northern', 'Lira': 'Northern', 'Luuka': 'Eastern', 'Luwero': 'Central', 'Lwengo': 'Central',
    'Lyantonde': 'Central', 'Manafwa': 'Eastern', 'Maracha': 'Northern', 'Masaka': 'Central', 'Masindi': 'Western',
    'Mayuge': 'Eastern', 'Mbale': 'Eastern', 'Mbarara': 'Western', 'Mitooma': 'Western', 'Mityana': 'Central',
    'Moroto': 'Eastern', 'Moyo': 'Northern', 'Mpigi': 'Central', 'Mubende': 'Central', 'Mukono': 'Central',
    'Nakapiripirit': 'Eastern', 'Nakaseke': 'Central', 'Nakasongola': 'Central', 'Namayingo': 'Eastern',
    'Namutumba': 'Eastern', 'Napak': 'Eastern', 'Nebbi': 'Western', 'Ngora': 'Eastern', 'Ntoroko': 'Western',
    'Ntungamo': 'Western', 'Nwoya': 'Northern', 'Otuke': 'Northern', 'Oyam': 'Northern', 'Pader': 'Northern',
    'Pallisa': 'Eastern', 'Rakai': 'Central', 'Rubirizi': 'Western', 'Rukungiri': 'Western', 'Serere': 'Eastern',
    'Sheema': 'Western', 'Sironko': 'Eastern', 'Soroti': 'Eastern', 'Ssembabule': 'Central', 'Tororo': 'Eastern',
    'Wakiso': 'Central', 'Yumbe': 'Northern', 'Zombo': 'Western',
}

YEARS = [2011, 2012, 2013, 2014, 2015, 2016]


def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 6371 * 2 * asin(sqrt(a))


def load_and_reshape():
    df = pd.read_excel(DATA_XLSX)
    df['lat'] = df['district'].map(lambda d: DISTRICT_COORDS[d][0])
    df['lon'] = df['district'].map(lambda d: DISTRICT_COORDS[d][1])
    df['region'] = df['district'].map(REGION_MAP)

    flood_cols = [c for c in df.columns if c.startswith('flood')]
    cas_cols = [c for c in df.columns if c.startswith('cas')]

    records = []
    for _, row in df.iterrows():
        for i, yr in enumerate(YEARS):
            records.append({
                'dist_id': row['dist_id'], 'district': row['district'],
                'lat': row['lat'], 'lon': row['lon'], 'region': row['region'], 'year': yr,
                'flooded': row[flood_cols[i]], 'cases': row[cas_cols[i]],
                'population': row['Popl'], 'wat_cov': row['wat_cov'],
                'san_cov': row['san_cov'], 'hw_cov': row['hw_cov'], 'score': row['score'],
            })
    long_df = pd.DataFrame(records)
    long_df['case_rate_per_100k'] = (long_df['cases'] / long_df['population']) * 100000
    long_df.to_csv(OUT / 'uganda_long_format.csv', index=False)

    summary = df.copy()
    summary['total_flood_years'] = summary[flood_cols].sum(axis=1)
    summary['total_cases'] = summary[cas_cols].sum(axis=1)
    summary['cases_per_100k'] = (summary['total_cases'] / summary['Popl']) * 100000
    summary['flood_years_pct'] = summary['total_flood_years'] / 6 * 100
    return summary, long_df


def compute_hotspots(df, k=5):
    """LISA-style (Local Moran's I quadrant) hotspot classification using a
    k-nearest-neighbor spatial weights matrix built from haversine distance
    between district centroids."""
    coords = df[['lat', 'lon']].values
    rates = df['cases_per_100k'].values
    n = len(df)
    neighbor_mean = np.zeros(n)

    for i in range(n):
        dists = [haversine(*coords[i], *coords[j]) for j in range(n) if j != i]
        order = np.argsort(dists)[:k]
        others = [j for j in range(n) if j != i]
        nearest = [others[o] for o in order]
        neighbor_mean[i] = rates[nearest].mean()

    df = df.copy()
    df['neighbor_mean_rate'] = neighbor_mean
    med_own, med_neigh = np.median(rates), np.median(neighbor_mean)

    def classify(own, neigh):
        if own > med_own and neigh > med_neigh:
            return 'High-High (Hotspot Cluster)'
        if own <= med_own and neigh <= med_neigh:
            return 'Low-Low (Coldspot Cluster)'
        if own > med_own and neigh <= med_neigh:
            return 'High-Low (Outlier)'
        return 'Low-High (Outlier)'

    df['lisa_class'] = [classify(o, ng) for o, ng in zip(rates, neighbor_mean)]

    z_own = (df['cases_per_100k'] - df['cases_per_100k'].mean()) / df['cases_per_100k'].std()
    z_neigh = (df['neighbor_mean_rate'] - df['neighbor_mean_rate'].mean()) / df['neighbor_mean_rate'].std()
    df['local_morans_i'] = z_own * z_neigh
    return df


def make_charts(df, long_df):
    # 1. Time series
    fig, ax1 = plt.subplots(figsize=(12, 6))
    yearly = long_df.groupby('year').agg(flooded_districts=('flooded', 'sum'),
                                          total_cases=('cases', 'sum')).reset_index()
    ax1.bar(yearly['year'], yearly['flooded_districts'], color='#2980b9', alpha=0.6, label='Flooded Districts')
    ax1.set_xlabel('Year', fontweight='bold')
    ax1.set_ylabel('Number of Flooded Districts', color='#2980b9', fontweight='bold')
    ax2 = ax1.twinx()
    ax2.plot(yearly['year'], yearly['total_cases'], color='#c0392b', marker='o', linewidth=3, markersize=10)
    ax2.set_ylabel('Total Cholera Cases', color='#c0392b', fontweight='bold')
    plt.title('Uganda: Flooding Extent vs Cholera Cases by Year (2011-2016)', fontweight='bold')
    fig.tight_layout()
    plt.savefig(OUT / '01_flood_cholera_timeseries.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 2. Top 20 districts
    fig, ax = plt.subplots(figsize=(10, 10))
    top20 = df.nlargest(20, 'total_cases').sort_values('total_cases')
    colors = ['#e74c3c' if x == 'High-High (Hotspot Cluster)' else '#95a5a6' for x in top20['lisa_class']]
    ax.barh(top20['district'], top20['total_cases'], color=colors, edgecolor='black')
    ax.set_xlabel('Total Cholera Cases (2011-2016)', fontweight='bold')
    ax.set_title('Top 20 Districts by Cumulative Cholera Cases', fontweight='bold')
    ax.legend(handles=[mpatches.Patch(facecolor='#e74c3c', label='LISA Hotspot Cluster'),
                        mpatches.Patch(facecolor='#95a5a6', label='Other')], loc='lower right')
    plt.tight_layout()
    plt.savefig(OUT / '02_top20_districts_cases.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 3. WASH scatter
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    for ax, col, label in zip(axes, ['wat_cov', 'san_cov', 'hw_cov'],
                               ['Water Coverage (%)', 'Sanitation Coverage (%)', 'Handwashing Coverage (%)']):
        ax.scatter(df[col], df['cases_per_100k'], alpha=0.6, s=60, c=df['total_flood_years'],
                   cmap='YlOrRd', edgecolor='black', linewidth=0.5)
        r = df[col].corr(df['cases_per_100k'])
        ax.set_xlabel(label, fontweight='bold')
        ax.set_ylabel('Cholera Rate (per 100,000)', fontweight='bold')
        ax.set_title(f'r = {r:.3f}', fontweight='bold')
    plt.suptitle('WASH Coverage vs Cholera Burden (colored by flood exposure)', fontweight='bold', y=1.05)
    plt.savefig(OUT / '03_wash_vs_cholera_scatter.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 4. LISA cluster map
    fig, ax = plt.subplots(figsize=(10, 12))
    cluster_colors = {'High-High (Hotspot Cluster)': '#e74c3c', 'Low-Low (Coldspot Cluster)': '#3498db',
                       'High-Low (Outlier)': '#f39c12', 'Low-High (Outlier)': '#9b59b6'}
    for cluster, color in cluster_colors.items():
        subset = df[df['lisa_class'] == cluster]
        ax.scatter(subset['lon'], subset['lat'], c=color, label=cluster, s=100, alpha=0.8, edgecolor='black')
    for _, row in df[df['lisa_class'] == 'High-High (Hotspot Cluster)'].iterrows():
        ax.annotate(row['district'], (row['lon'], row['lat']), fontsize=7, xytext=(3, 3), textcoords='offset points')
    ax.set_xlabel('Longitude', fontweight='bold')
    ax.set_ylabel('Latitude', fontweight='bold')
    ax.set_title('Spatial Cluster Analysis (LISA): Cholera Hotspots in Uganda\n(District Centroids, 2011-2016)',
                 fontweight='bold')
    ax.legend(loc='upper left', fontsize=9)
    ax.set_aspect('equal')
    plt.tight_layout()
    plt.savefig(OUT / '04_lisa_cluster_map.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 5. Flood bubble map
    fig, ax = plt.subplots(figsize=(10, 12))
    sc = ax.scatter(df['lon'], df['lat'], s=df['total_flood_years'] * 80 + 20, c=df['cases_per_100k'],
                    cmap='YlOrRd', alpha=0.75, edgecolor='black', linewidth=0.8)
    plt.colorbar(sc, ax=ax, label='Cholera Rate per 100,000')
    ax.set_xlabel('Longitude', fontweight='bold')
    ax.set_ylabel('Latitude', fontweight='bold')
    ax.set_title('Flood Frequency (bubble size) & Cholera Burden (color)\nUganda Districts, 2011-2016',
                 fontweight='bold')
    ax.set_aspect('equal')
    plt.tight_layout()
    plt.savefig(OUT / '05_flood_bubble_map.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 6. Regional breakdown
    region_summary = df.groupby('region').agg(total_cases=('total_cases', 'sum'),
                                               avg_flood_years=('total_flood_years', 'mean')).reset_index()
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    palette = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12']
    axes[0].bar(region_summary['region'], region_summary['total_cases'], color=palette, edgecolor='black')
    axes[0].set_title('Total Cholera Cases by Region (2011-2016)', fontweight='bold')
    axes[1].bar(region_summary['region'], region_summary['avg_flood_years'], color=palette, edgecolor='black')
    axes[1].set_title('Average Flood Years by Region', fontweight='bold')
    plt.tight_layout()
    plt.savefig(OUT / '06_regional_breakdown.png', dpi=300, bbox_inches='tight')
    plt.close()


def build_dashboard_json(df, long_df):
    records = []
    for _, row in df.iterrows():
        yearly = long_df[long_df['district'] == row['district']][['year', 'flooded', 'cases']].to_dict('records')
        records.append({
            'district': row['district'], 'lat': round(row['lat'], 4), 'lon': round(row['lon'], 4),
            'region': row['region'], 'population': int(row['Popl']),
            'total_flood_years': int(row['total_flood_years']), 'total_cases': int(row['total_cases']),
            'cases_per_100k': round(row['cases_per_100k'], 2), 'wat_cov': row['wat_cov'],
            'san_cov': row['san_cov'], 'hw_cov': row['hw_cov'], 'score': row['score'],
            'lisa_class': row['lisa_class'], 'yearly': yearly,
        })
    with open(DOCS / 'data.json', 'w') as f:
        json.dump(records, f)
    with open(OUT / 'dashboard_data.json', 'w') as f:
        json.dump(records, f)


def main():
    print("Loading & reshaping data...")
    df, long_df = load_and_reshape()
    print(f"  {len(df)} districts, {len(long_df)} district-year records")

    print("Computing LISA spatial hotspot clusters...")
    df = compute_hotspots(df)
    df.to_csv(OUT / 'district_hotspot_analysis.csv', index=False)
    print(df['lisa_class'].value_counts().to_string())

    print("Generating charts & maps...")
    make_charts(df, long_df)

    print("Building dashboard JSON feed...")
    build_dashboard_json(df, long_df)

    print("\nDone. Outputs in ./outputs, dashboard data in ./docs/data.json")


if __name__ == '__main__':
    main()
