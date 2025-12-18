# Visualizing all of the world’s 258 countries and regions

Last updated: Dec 18th 2025

Bookstores have a lot of printed world atlases, which are nice to look at but have the trade off that each country is shown either once with a mix of physical and political attributes, or in multiple maps that are not overlaid. Online maps often have impressive visualizations of particular places, but rarely cover all of the world’s countries at a consistent level. Using online vector and raster data along with QGIS and PyQGIS enables viewing of each of the world’s 258 countries and regions with a variety of combinations of data. Dask-Leaflet enables these per-country views to be displayed in a webapp in the browser.

## Disclaimer

This is a personal project built as part of my transition from generalist data scientist to specializing in geospatial data science, GIS, and GeoAI. The aim is for this project to be shareable, but it is not designed for production use.

## Requirements

Countries

- QGIS application

Webapp

- Web browser
- Machine that can run Conda virtualenv and Python, e.g., Visual Studio code with Python extension

## Setup

Countries

- Install QGIS, e.g., QGIS-LTR 3.34
- Create QGIS project
- Download data
  - Natural Earth
    - `ne_10m_admin_0_countries`
    - `ne_10m_admin_1_states_provinces`
    - `ne_10m_populated_places_simple`
    - `ne_10m_urban_areas`
    - `ne_10m_railroads`
    - `ne_10m_roads`
    - `ne_10m_lakes`
    - `ne_10m_rivers_lake_centerlines`
    - `HYP_SR_HR`
    - `SR_HR`
  - Landscan population density
    - `landscan-global-2023-colorized`
  - Daylightmap Landcover 
    - `low`
  - Climate zones
    - `koppen_geiger_0p00833333`
- Add as layers to project using GUI
- In `countries.py`, change output directory from `out_dir = f"/Users/nball/Common/Geo/projects/countries/output_countries/{country}"` to a suitable location

Webapp

- Create virtualenv, e.g., `.conda` in current directory in VSCode
- `pip install dash-leaflet`
- In `dash_leaflet_countries.py` set `country`, `datadir` and `assetsdir` in setup section
- Open web browser, e.g., Chrome (used for webapp)

## Run

Countries

- Navigate to QGIS Python console, show editor
- Open and run `countries.py`
- Click on the first layer in the Layers navigation bar with the name of the country
- Click Zoom to Layer on the toolbar
- Display or hide other layers from the country as desired

The country shown can be varied by changing `country = 'Uzbekistan'` to any country named in the `ne_10m_admin_0_countries` layer.
When overlaid on the digital elevation terrain, the colored layers, e.g., `_low`, work best on the b/w `_SR_HR` vs. the color `_HYP_HR_SR`

Webapp

- Run `python dash_leaflet_countries.py`
- Webapp will be visible on http://127.0.0.1:8050/ in the browser

## Improvements

- Add setup so data downloading and adding initial layers in the QGIS GUI are done programmatically
- Webapp legend
- Better symbology for some layers: roads, states/provinces
- Antarctica and Cote d'Ivoire fail
- Remove large separations in some countries by masking on states/provinces
- Higher resolution data for smaller countries, especially the borders and digital elevation models (DEM)
- Cloud-native workflow to tile and serve such larger data at an appropriate resolution for the chosen country being viewed, using formats like cloud-optimized GeoTIFF (COG)
- Other datasets, e.g., Satellite Embedding V1 from DeepMind’s AlphaEarth Foundations GeoAI model
- Other information such as industries, geology, mark the capital city, some photos, major attractions or events, etc.
- Country-specific CRSs: some countries such as Canada are still distorted in Mercator projection, and might benefit from a more “looking down at the globe” view, or a country-specific CRS
- Enable printer-friendly or PDF views for each country
- Enhance the webapp with pictures, text, etc.
