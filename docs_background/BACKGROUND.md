# Background: Cholera and Flooding in Uganda

## Cholera as an Endemic Threat

Cholera, caused by *Vibrio cholerae*, has been endemic in Uganda for decades, with confirmed outbreaks reported nearly every year somewhere in the country. Unlike epidemic-only settings, Uganda experiences recurring, geographically clustered outbreaks concentrated in a fairly predictable set of high-risk districts — particularly those bordering Lake Albert, Lake Edward, Lake Kyoga, and the Nile, as well as districts along the Kenyan, South Sudanese, and DRC borders where cross-border population movement is high.

## The Flooding-Cholera Pathway

Cholera transmission is fundamentally a water, sanitation, and hygiene (WASH) problem. The organism spreads via the fecal-oral route, typically through water contaminated with feces from an infected person. Flooding intensifies this pathway in several well-documented ways:

- **Contamination of water sources**: Flooding overwhelms pit latrines (the dominant sanitation technology in rural Uganda) and washes fecal matter into wells, boreholes, streams, and lakes used for drinking water.
- **Displacement and crowding**: Floods and landslides displace households into transit camps or host communities with inadequate WASH infrastructure, creating conditions for rapid transmission.
- **Damage to WASH infrastructure**: Floods destroy water points, drainage, and sanitation facilities, and disrupt health service delivery precisely when it is most needed.
- **Behavioral risk factors**: In flood-affected communities, people are more likely to use unsafe surface water for drinking, cooking, and washing when normal sources are compromised.

Public health investigations in Uganda have repeatedly documented this pathway directly. Following catastrophic landslides and floods in **Bududa district (June 2019)**, a cholera outbreak was confirmed roughly two weeks later; the response required emergency oral cholera vaccination of over 90% of the target population across 22 affected parishes. A 2023 outbreak investigation in **Kayunga District** linked cases to a low-lying, flood-prone village where residents drew drinking water from the Nile and had recently experienced flooding — heavy rains and flooding were explicitly identified as recurring risk factors for cholera outbreaks across Uganda and the wider region. A separate 2015 outbreak in **Hoima District** (Kaiso Village, Lake Albert shoreline) was traced to lake water contaminated with human feces, illustrating the same lake-proximity risk pattern independent of a single flood event.

## Geographic Concentration

Cholera burden in Uganda is not evenly distributed. Historically, the districts most affected cluster in:

- **The Lake Albert basin** (Hoima, Buliisa, Ntoroko, Bundibugyo) — fishing communities with high population mobility, poor sanitation coverage relative to water access, and direct lake-water dependence.
- **The Rwenzori/western border region** (Kasese and neighbors) — flood- and landslide-prone terrain draining from the Rwenzori Mountains.
- **The West Nile / Nebbi corridor** — proximity to the Albert Nile and cross-border movement with DRC.
- **Eastern border districts** (Mbale, Bududa, Busia, Butaleja) — landslide-prone highland areas and low-lying flood plains near the Kenyan border, with high population density.

This geographic clustering is the foundation for hotspot analysis: rather than treating cholera as a uniform national risk, spatial analysis identifies which specific districts persistently carry disproportionate burden, so that WASH investment and outbreak preparedness (oral cholera vaccine stockpiles, rapid response teams) can be targeted rather than spread thinly.

## Why WASH Coverage Alone Doesn't Explain the Pattern

A recurring, somewhat counterintuitive finding in Uganda cholera analyses (echoed in this dataset) is that simple correlations between WASH coverage indicators and cholera burden are often weak. This is not because WASH is irrelevant — it is causally central to transmission — but because:

1. **Coverage statistics measure infrastructure existence, not functionality or use.** A district can report high "water coverage" from boreholes that are seasonally dry, contaminated, or too far from flood-affected communities to be used during an emergency.
2. **Handwashing coverage is systematically low nationwide** (often in the 20–40% range even in otherwise well-served districts), meaning it doesn't discriminate well between high- and low-burden districts.
3. **Flooding acts as an acute shock** that temporarily overwhelms even reasonably good baseline WASH infrastructure — so a district with decent average coverage can still experience a sharp outbreak in a bad flood year.
4. **Outbreak introduction matters as much as underlying vulnerability.** Cholera requires the pathogen to be introduced (via travel, trade, cross-border movement, funerals) before local conditions determine whether it spreads. Districts with equally poor WASH may have very different outbreak histories simply due to introduction events.

This is why spatial and temporal hotspot analysis — identifying *where* and *when* flooding and cholera co-occur repeatedly — is more actionable than cross-sectional WASH correlation alone.

## Public Health Response Framework in Uganda

Uganda's Ministry of Health, working with WHO and partners, has developed a relatively mature cholera response system built around:

- **Oral cholera vaccine (OCV) stockpiles** for rapid deployment to confirmed or high-risk outbreak areas (as used in Bududa 2019).
- **Weekly epidemiological surveillance** through the national Health Management Information System, enabling early detection of case clusters.
- **Multi-sectoral flood early warning**, coordinating meteorological flood forecasts with health-sector pre-positioning of supplies in historically high-risk districts.
- **WASH investment prioritization**, increasingly guided by burden data rather than uniform national rollout, given limited resources across 112+ districts.

## Purpose of This Analysis

This project uses district-level data (2011–2016) combining annual flood occurrence, annual cholera case counts, population, and WASH coverage indicators (water, sanitation, handwashing, and a composite score) to:

1. Quantify the flooding–cholera relationship at the district level over time.
2. Identify statistically significant spatial clusters ("hotspots") of cholera burden using Local Indicators of Spatial Association (LISA).
3. Characterize which districts combine high flood exposure, high cholera burden, and weak WASH coverage — the highest-priority districts for integrated flood/WASH/health investment.
4. Provide an open, reproducible, interactive dashboard so public health stakeholders can explore the data themselves rather than relying on static reports.

---

### Sources Consulted

- Bwire G, Tumuhairwe I, Kwagonza L, et al. *Rapid cholera outbreak control following catastrophic landslides and floods: A case study of Bududa district, Uganda.* African Health Sciences, 2023.
- Uganda National Institute of Public Health (UNIPH). *Cholera outbreak associated with drinking contaminated river water in Kayunga District, Uganda, June–August 2023.*
- Oguttu DW, Okullo A, Bwire G, Nsubuga P, Ario AR. *Cholera outbreak caused by drinking lake water contaminated with human faeces in Kaiso Village, Hoima District, Western Uganda, October 2015.* Infectious Diseases of Poverty, 2017.
- Frontiers in Public Health. *Waterborne diseases burden, determinants and health system gaps in Eastern Uganda: a mixed-methods baseline study in the Busoga region.*
