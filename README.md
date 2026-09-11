# Visualizing all of the world’s 258 countries and regions

Last updated: Feb 06th 2026

Bookstores have a lot of printed world atlases, which are nice to look at but have the trade off that each country is shown either once with a tradeoff of physical and political attributes, or in multiple maps that are not overlaid. Online maps often have impressive visualizations of particular places, but rarely cover all of the world’s countries at a consistent level. Using online vector and raster data along with QGIS and PyQGIS enables viewing of each of the world’s 258 countries and regions with a variety of combinations of data. Dask-Leaflet enables these per-country views to be displayed in a webapp in the browser. ([Blogpost](https://nickballdatascience.com/visualizing-all-of-the-worlds-258-countries-and-regions/))

## Disclaimer

This is a personal project built as part of my transition from generalist data scientist to specializing in geospatial data science, GIS, and GeoAI. The aim is for this project to be shareable, but it is not designed for production use.

## Requirements

Countries

- QGIS application
- Email for Landscan Global population data

Webapp

- Web browser
- Machine that can run Conda virtualenv and Python, e.g., Visual Studio code with Python extension

## Setup

Countries

- Install QGIS, e.g., QGIS-LTR 3.34
- Create QGIS project
- Download data
  - Natural Earth from https://www.naturalearthdata.com/downloads: navigate to below names, unzip downloaded directories
    - `ne_10m_admin_0_countries.shp` (+ files associated to .shp shapefiles)
    - `ne_10m_admin_1_states_provinces.shp`
    - `ne_10m_populated_places_simple.shp`
    - `ne_10m_urban_areas.shp`
    - `ne_10m_railroads.shp`
    - `ne_10m_roads.shp`
    - `ne_10m_lakes.shp`
    - `ne_10m_rivers_lake_centerlines.shp`
    - `HYP_SR_HR.tif`
    - `SR_HR.tif`
  - Landscan global population density from https://landscan.ornl.gov -> Download (requires email)
    - `landscan-global-2023-colorized.tif`
  - Daylightmap Landcover from https://daylightmap.org/2023/10/11/landcover.html
    - https://daylight-openstreetmap.s3.us-west-2.amazonaws.com/landcover/low.shp
    - https://daylight-openstreetmap.s3.us-west-2.amazonaws.com/landcover/low.dbf
    - https://daylight-openstreetmap.s3.us-west-2.amazonaws.com/landcover/low.prj
    - https://daylight-openstreetmap.s3.us-west-2.amazonaws.com/landcover/low.shx
  - Climate zones from https://www.gloh2o.org/koppen -> https://figshare.com/ndownloader/files/45057352
    - `1991_2020/koppen_geiger_0p00833333.tif`
- Add as layers to project using GUI
- In `countries.py`, change output directory from `out_dir = f"/Users/nball/Common/Geo/projects/countries/output_countries/{country}"` to a suitable location

Webapp

- Create virtualenv, e.g., `.venv` in current directory in VSCode
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

To existing features

- Some webapp layers are offset from the basemap; project layers to Mercator
- Webapp legend
- Better symbology for some layers: roads, states/provinces
- Set layer opacities so no color mixing when overlaid
- For land cover, can't tell between snow and no data -> set no data to white/gray stripes
- GDAL and OGR commands fail on countries with spaces in webapp
- Some webapp countries, e.g., Canada, fail on `gdal_info` `awk` because no gap `(` to `long`: need to parse out of brackets
- Add setup so data downloading and adding initial layers in the QGIS GUI are done programmatically: requires resolving known issues with `qgis.processing`
- Antarctica and Cote d'Ivoire fail: Antarctica requires a suitable CRS, Code d'Ivoire is character handling
- Remove large separations in some countries, e.g., France / French Guyana by case-by-case masking on states/provinces
- Correct invalid polygons using QGIS’s fix geometries or PostGIS’s ST_MakeValid rather than QGIS Do Not Filter on invalid features
- Threshold populated places to only large places (abs value not country %) so the names don't get overwritten by small places
- Show names of features: rivers, etc.
- Higher resolution data for smaller countries, especially the borders and digital elevation models (DEM)
- Other datasets, e.g., Satellite Embedding V1 from DeepMind’s AlphaEarth Foundations GeoAI model
- Other information such as industries, geology, mark the capital city, mountain heights, national parks, World Heritage sites, scale, etc.
- Country-specific CRSs: some countries such as Canada are still distorted in Mercator projection, and might benefit from a more “looking down at the globe” view, or a country-specific CRS
- Enable printer-friendly or PDF views for each country
- Enhance the webapp with pictures, text, etc.

## Extensions

Add new features

- Cloud-native workflow to tile and serve such larger data at an appropriate resolution for the chosen country being viewed, using formats like cloud-optimized GeoTIFF (COG); e.g., TiTiler
- Project as a QGIS plugin
- Qgis2web as alternative display to QGIS or webapp
- Combine DEM data and QGIS 3D for a 3D view of each country

## Data licenses

NaturalEarth = [Public domain](https://www.naturalearthdata.com/about/terms-of-use/)  
Landscan Global = [CC BY 4.0](https://landscan.ornl.gov/licensing)  
Koppen Geiger = [CC BY 4.0](https://www.gloh2o.org/koppen/)  
Daylightmap = [ODbL](https://daylightmap.org/attribution.html)  
