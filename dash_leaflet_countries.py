# Show countries in Dash-Leaflet
#
# cd /Users/nball/Common/Geo/projects/countries
# code .
# Run in VS Code using .conda, to access gdal (conda) and dash-leaflet (pip in conda)
#
# (was source .venv/bin/activate
# python dash_leaflet_countries.py)
#
# App visible on http://127.0.0.1:8050/
#
# Oct 07th 2025+

import os
import subprocess

import dash_leaflet as dl

from dash import html
from dash_extensions.enrich import DashProxy
from dash_extensions.javascript import assign

app = DashProxy()


# Setup
# -----

# Files need to be in assets/ not file://

print('Setup ...')

country = 'China'  # Country name

datadir = f"/Users/nball/Common/Geo/projects/countries/output_countries/{country}"
assetsdir = "/Users/nball/Common/Geo/projects/countries/assets"


# Convert images
# --------------

# Raster TIF to PNG

print('Converting rasters ...')

# Run commands like this in bash: gdal_translate -of PNG -ot Byte -scale .../Afghanistan_HYP_HR_SR.tif .../Afghanistan_HYP_HR_SR.png (AI)
# Can use os since output is files
# AI function but would have written similar

def raster_to_png(input_tif, output_png):
    cmdstring = f"gdal_translate -of PNG -ot Byte -scale {input_tif} {output_png}"
    print(f"{cmdstring}")
    exit_code = os.system(cmdstring)
    print(f"Command exited with code: {exit_code}")

raster_to_png(f"{datadir}/{country}_HYP_HR_SR.tif",                      f"{assetsdir}/{country}_HYP_HR_SR.png")
raster_to_png(f"{datadir}/{country}_koppen_geiger_0p00833333.tif",       f"{assetsdir}/{country}_koppen_geiger_0p00833333.png")
raster_to_png(f"{datadir}/{country}_landscan-global-2023-colorized.tif", f"{assetsdir}/{country}_landscan-global-2023-colorized.png")
raster_to_png(f"{datadir}/{country}_SR_HR.tif",                          f"{assetsdir}/{country}_SR_HR.png")

# Vector SHP to GeoJSON

print('Converting vectors ...')

# Run this command in bash: ogr2ogr -f GeoJSON Afghanistan_low.geojson Afghanistan_low.shp (AI)
# ogr2ogr is <output> <input>
# AI function but would have written similar

def vector_shp_to_geojson(input_shp, output_geojson):
    cmdstring = f"ogr2ogr -f GeoJSON {output_geojson} {input_shp}"
    print(f"{cmdstring}")
    exit_code = os.system(cmdstring)
    print(f"Command exited with code: {exit_code}")

vector_shp_to_geojson(f"{datadir}/{country}_low.shp",                             f"{assetsdir}/{country}_low.geojson")
vector_shp_to_geojson(f"{datadir}/{country}_ne_10m_admin_1_states_provinces.shp", f"{assetsdir}/{country}_ne_10m_admin_1_states_provinces.geojson")
vector_shp_to_geojson(f"{datadir}/{country}_ne_10m_lakes.shp",                    f"{assetsdir}/{country}_ne_10m_lakes.geojson")
vector_shp_to_geojson(f"{datadir}/{country}_ne_10m_populated_places_simple.shp",  f"{assetsdir}/{country}_ne_10m_populated_places_simple.geojson")
vector_shp_to_geojson(f"{datadir}/{country}_ne_10m_railroads.shp",                f"{assetsdir}/{country}_ne_10m_railroads.geojson")
vector_shp_to_geojson(f"{datadir}/{country}_ne_10m_rivers_lake_centerlines.shp",  f"{assetsdir}/{country}_ne_10m_rivers_lake_centerlines.geojson")
vector_shp_to_geojson(f"{datadir}/{country}_ne_10m_roads.shp",                    f"{assetsdir}/{country}_ne_10m_roads.geojson")
vector_shp_to_geojson(f"{datadir}/{country}_ne_10m_urban_areas.shp",              f"{assetsdir}/{country}_ne_10m_urban_areas.geojson")


# Image bounds
# ------------

# To show correctly, we need the image bounds (lat/lon) for the raster layers

print('Image bounds ...')

# Cf. hardwired /Users/nball/Common/Geo/projects/countries/output_countries/Afghanistan/Afghanistan_HYP_HR_SR.tif from QGIS GUI tif properties
# image_bounds = [[29.3999999999878909, 60.5000000000481180], [38.4666666666563728, 74.8833333333843143]]

# Get image bounds from one of the raster images using gdalinfo
# Need to capture output so use subprocess
# Assumes gdalinfo output is in expected format
# Cf. https://gis.stackexchange.com/questions/104362/how-to-get-extent-out-of-geotiff
# https://www.geeksforgeeks.org/python/print-output-from-os-system-in-python/

# AI generated code to use datadir and country variables, based on my verbatim command string
# Presumably works because f substitutes variables but rest is verbatim, but double braces in awk command

cmdstring = f"""gdalinfo {datadir}/{country}_HYP_HR_SR.tif | grep 'Lower Left' | awk '{{print "[" $5,$4 "]"}}' | sed s/,//g | sed s/\)//g | sed s/\ /', '/g"""
print(f"{cmdstring}")

try:
    lower_left = subprocess.check_output(cmdstring, shell=True, text=True) # Output as string like [29.4000000, 60.5000000] (Afghanistan)
except subprocess.CalledProcessError as e:
    print(f"Error executing command: {e}")

cmdstring = f"""gdalinfo {datadir}/{country}_HYP_HR_SR.tif | grep 'Upper Right' | awk '{{print "[" $5,$4 "]"}}' | sed s/,//g | sed s/\)//g | sed s/\ /', '/g"""
print(f"{cmdstring}")

try:
    upper_right = subprocess.check_output(cmdstring, shell=True, text=True) # Output as string like [38.4666667, 74.8833333] (Afghanistan)
except subprocess.CalledProcessError as e:
    print(f"Error executing command: {e}")

# Convert subprocess output strings to list (AI code)

image_bounds = []
image_bounds.append([float(x) for x in lower_left.strip().strip('[]').split(',')])
image_bounds.append([float(x) for x in upper_right.strip().strip('[]').split(',')])
print(f"Image bounds: {image_bounds}")

# Better might be to get bounds from country border shapefile using ogrinfo
# Or extent directly from QGIS (AI code below), but needs QGIS environment access

#layer = QgsProject.instance().mapLayersByName('Afghanistan')[0]
#extent = layer.extent()
#image_bounds = [[extent.yMinimum(), extent.xMinimum()], [extent.yMaximum(), extent.xMaximum()]]
#print(f"Image bounds: {image_bounds}")


# Raster layers
# -------------

print('Raster layers ...')

raster_HYP_HR_SR                      = app.get_asset_url(country + '_HYP_HR_SR.png')
raster_koppen_geiger_0p00833333       = app.get_asset_url(country + '_koppen_geiger_0p00833333.png')
raster_landscan_global_2023_colorized = app.get_asset_url(country + '_landscan-global-2023-colorized.png') # Underscores in variable name
raster_SR_HR                          = app.get_asset_url(country + '_SR_HR.png')


# Vector layers
# -------------

print('Vector layers ...')

vector_low                             = app.get_asset_url(country + '_low.geojson')
vector_ne_10m_admin_1_states_provinces = app.get_asset_url(country + '_ne_10m_admin_1_states_provinces.geojson')
vector_ne_10m_lakes                    = app.get_asset_url(country + '_ne_10m_lakes.geojson')
vector_ne_10m_populated_places_simple  = app.get_asset_url(country + '_ne_10m_populated_places_simple.geojson')  # IN PROGRESS
vector_ne_10m_railroads                = app.get_asset_url(country + '_ne_10m_railroads.geojson')                # IN PROGRESS
vector_ne_10m_rivers_lake_centerlines  = app.get_asset_url(country + '_ne_10m_rivers_lake_centerlines.geojson')
vector_ne_10m_roads                    = app.get_asset_url(country + '_ne_10m_roads.geojson')                    # IN PROGRESS
vector_ne_10m_urban_areas              = app.get_asset_url(country + '_ne_10m_urban_areas.geojson')

# JavaScript function to style vector_low polygons based on the 'category' property (AI code, modified)

style_handle_low = assign("""function(feature, context){
    const category = feature.properties.class;
    if (category === 'trees') {
        return {fillColor: 'green', color: 'green', weight: 1};
    } else if (category === 'crop') {
        return {fillColor: 'orange', color: 'orange', weight: 1};
    } else if (category === 'snow') {
        return {fillColor: 'white', color: 'white', weight: 1};
    } else if (category === 'grass') {
        return {fillColor: 'gray', color: 'gray', weight: 1};
    } else if (category === 'urban') {
        return {fillColor: 'red', color: 'red', weight: 1};
    } else if (category === 'shrub') {
        return {fillColor: 'pink', color: 'pink', weight: 1};
    } else if (category === 'barren') {
        return {fillColor: 'brown', color: 'brown', weight: 1};
    }
    return {fillColor: 'grey', color: 'black', weight: 1}; // Default style
}""")

# JavaScript function to style vector_ne_10m_lakes as blue polygons (AI code)

style_handle_ne_10m_lakes = assign("""function(feature, context){
    return {fillColor: 'blue', color: 'blue', weight: 1};
}""")

# Rivers are already blue lines, so no style needed

# JavaScript function to style states/provinces as polygons with no fill and green dashed line borders (AI code)

style_handle_ne_10m_admin_1_states_provinces = assign("""function(feature, context){
    return {fillColor: 'transparent', color: 'green', weight: 2, dashArray: '5, 5'};
}""")

# JavaScript function to style vector_ne_10m_populated_places_simple as red circles (AI code)
# Replace teardrop markers with circles for simplicity

style_handle_ne_10m_populated_places_simple = assign("""function(feature, context){
    return {radius: 5, fillColor: 'red', color: 'red', weight: 1, fillOpacity: 0.8};
}""")

# JavaScript function to style vector_ne_10m_railroads as black lines with ticks (AI code)

style_handle_ne_10m_railroads = assign("""function(feature, context){
    return {color: 'black', weight: 2};
}""")

# JavaScript function to style vector_ne_10m_roads as white lines with black borders (AI code)

style_handle_ne_10m_roads = assign("""function(feature, context){
    return {color: 'white', weight: 3, opacity: 0.8};
}""")

# JavaScript function to style vector_ne_10m_urban_areas as gray polygons (AI code)

style_handle_ne_10m_urban_areas = assign("""function(feature, context){
    return {fillColor: 'gray', color: 'gray', weight: 1, fillOpacity: 0.5};
}""")


# App layout
# ----------

# Layers are listed in order they appear: first is on top
# https://www.dash-leaflet.com/components/raster_layers/image_overlay

print('App layout ...')

center_lat = (image_bounds[0][0] + image_bounds[1][0]) / 2
center_lon = (image_bounds[0][1] + image_bounds[1][1]) / 2

print(f"Center: {center_lat}, {center_lon}")

app.layout = html.Div([
    dl.Map(center=[center_lat, center_lon], zoom=8, style={"height": "100vh"}, children=[
        dl.LayersControl(children=[
            dl.Overlay(dl.GeoJSON(url=vector_ne_10m_populated_places_simple, style=style_handle_ne_10m_populated_places_simple), name="Populated places", checked=True),
            dl.Overlay(dl.GeoJSON(url=vector_ne_10m_urban_areas, style=style_handle_ne_10m_urban_areas), name="Urban areas", checked=True),
            dl.Overlay(dl.GeoJSON(url=vector_ne_10m_railroads, style=style_handle_ne_10m_railroads), name="Railroads", checked=False),
            dl.Overlay(dl.GeoJSON(url=vector_ne_10m_roads, style=style_handle_ne_10m_roads), name="Roads", checked=False),
            dl.Overlay(dl.GeoJSON(url=vector_ne_10m_lakes, style=style_handle_ne_10m_lakes), name="Lakes", checked=True),
            dl.Overlay(dl.GeoJSON(url=vector_ne_10m_rivers_lake_centerlines), name="Rivers", checked=True),
            dl.Overlay(dl.GeoJSON(url=vector_ne_10m_admin_1_states_provinces, style=style_handle_ne_10m_admin_1_states_provinces), name="States and provinces", checked=False),
            dl.Overlay(dl.GeoJSON(url=vector_low, style=style_handle_low), name="Land cover", checked=False),
            dl.Overlay(dl.ImageOverlay(opacity=0.8, url=raster_landscan_global_2023_colorized, bounds=image_bounds), name="Population", checked=False),
            dl.Overlay(dl.ImageOverlay(opacity=0.8, url=raster_koppen_geiger_0p00833333, bounds=image_bounds), name="Climate type", checked=False),
            dl.Overlay(dl.ImageOverlay(opacity=0.5, url=raster_SR_HR, bounds=image_bounds), name="Elevation (b/w)", checked=False),
            dl.Overlay(dl.ImageOverlay(opacity=0.5, url=raster_HYP_HR_SR, bounds=image_bounds), name="Elevation", checked=True),
            dl.Overlay(dl.TileLayer(), name="Base layer", checked=False),
        ])
    ])
])


# Run app
# -------

if __name__ == "__main__":
    app.run()
    #app.run_server(debug=True)
