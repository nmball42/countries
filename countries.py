# Countries
#
# Requirements
#
# Python environment with PyQGIS, e.g., the QGIS Python console
# Create QGIS project with country borders vector base map, e.g., ne_10m_admin_0_countries from Natural Earth
# Vector base map has attribute "name" with country names
# Add raster and vector layers to be clipped to the countries
# Run this script in the QGIS Python console
#
# Sep 23rd 2025+


# Setup
# -----

# Imports

import os

from qgis.core import QgsFeatureRequest, QgsProject, QgsCategorizedSymbolRenderer, QgsField, QgsRendererCategory
from qgis.core import QgsSymbol, QgsPalLayerSettings, QgsTextFormat, QgsTextBufferSettings, QgsVectorLayerSimpleLabeling
from qgis.core import QgsLineSymbol, QgsMarkerLineSymbolLayer, QgsSimpleMarkerSymbolLayer

from qgis.utils import iface
from qgis.PyQt.QtGui import QColor, QFont
from qgis.PyQt.QtCore import QVariant

# Settings

country = 'Uzbekistan' # Country name
country_borders_file = 'ne_10m_admin_0_countries' # File name of country borders shapefile, without .shp
out_dir = f"/Users/nball/Common/Geo/projects/countries/output_countries/{country}" # Output directory

# Setup

if not os.path.exists(out_dir): # Make output directory if it doesn't exist
    os.makedirs(out_dir)


# Select the country
# ------------------

# Cf. layer = iface.activeLayer()
# layer.selectByExpression(expression, QgsVectorLayer.SetSelection)

layer = QgsProject.instance().mapLayersByName(country_borders_file)[0]
expression = f'"name_long" = \'{country}\'' # e.g. '"name" = \'Sweden\'' (AI)
request = QgsFeatureRequest().setFilterExpression(expression)
new_layer = layer.materialize(request)
new_layer.setName(country)
QgsProject.instance().addMapLayer(new_layer)


# Vector data layers to be clipped to country
# -------------------------------------------

# Each layer as function, currently self-contained
# Then call in order we want them to be drawn
# Outputs shapefiles

# https://docs.qgis.org/3.40/en/docs/user_manual/processing_algs/qgis/vectoroverlay.html#clip
# "The attribute values of the features are not modified"

# Cf. (https://docs.qgis.org/3.40/en/docs/pyqgis_developer_cookbook/vector.html#modifying-vector-layers)
# if iface.mapCanvas().isCachingEnabled():
#    layer.triggerRepaint()
# else:
#    iface.mapCanvas().refresh()

# Natural Earth: States and provinces

def ne_states_and_provinces(visibility=False):

    overlay = QgsProject.instance().mapLayersByName(country)[0]
    input = QgsProject.instance().mapLayersByName('ne_10m_admin_1_states_provinces')[0]
    output = f"{out_dir}/{country}_ne_10m_admin_1_states_provinces.shp"
    params = {'INPUT': input, 'OVERLAY': overlay, 'OUTPUT': output}
    result = processing.runAndLoadResults("qgis:clip", params)

    # Set states and provinces fill color to transparent
    # AI code, modified

    layer = QgsProject.instance().mapLayersByName(f"{country}_ne_10m_admin_1_states_provinces")[0]
    fill_symbol = QgsSymbol.defaultSymbol(layer.geometryType())
    fill_symbol.setColor(QColor(0, 0, 255, 0)) # Transparent fill
    layer.setRenderer(QgsSingleSymbolRenderer(fill_symbol))
    layer.triggerRepaint()
    iface.layerTreeView().refreshLayerSymbology(layer.id())

    # Set border color and width, e.g., dark green dashed line
    # AI code, commented out
    
    #border_symbol = layer.renderer().symbol()
    #border_symbol.setStrokeColor(QColor("#0000ff"))
    #border_symbol.setStrokeWidth(0.5)
    #layer.triggerRepaint()
    #iface.layerTreeView().refreshLayerSymbology(layer.id())

    # Set layer visibility (AI, modified)
    if visibility == False:
        root = QgsProject.instance().layerTreeRoot()
        country_layer = root.findLayer(layer.id())
        if country_layer is not None:
            country_layer.setItemVisibilityChecked(False)


# Natural Earth: Rivers

def ne_rivers(visibility=False):

    overlay = QgsProject.instance().mapLayersByName(country)[0]
    input = QgsProject.instance().mapLayersByName('ne_10m_rivers_lake_centerlines')[0]
    output = f"{out_dir}/{country}_ne_10m_rivers_lake_centerlines.shp"
    params = {'INPUT': input, 'OVERLAY': overlay, 'OUTPUT': output}
    result = processing.runAndLoadResults("qgis:clip", params)

    layer = QgsProject.instance().mapLayersByName(f"{country}_ne_10m_rivers_lake_centerlines")[0]
    renderer = layer.renderer()
    symbol = renderer.symbol() # symbol = layer.renderer().symbol() ?
    symbol.setColor(QColor("#0000ff"))
    layer.triggerRepaint()
    iface.layerTreeView().refreshLayerSymbology(layer.id())

    if visibility == False:
        root = QgsProject.instance().layerTreeRoot()
        country_layer = root.findLayer(layer.id())
        if country_layer is not None:
            country_layer.setItemVisibilityChecked(False)


# Natural Earth: Lakes

def ne_lakes(visibility=False):

    overlay = QgsProject.instance().mapLayersByName(country)[0]
    input = QgsProject.instance().mapLayersByName('ne_10m_lakes')[0]
    output = f"{out_dir}/{country}_ne_10m_lakes.shp"
    params = {'INPUT': input, 'OVERLAY': overlay, 'OUTPUT': output}
    result = processing.runAndLoadResults("qgis:clip", params)

    layer = QgsProject.instance().mapLayersByName(f"{country}_ne_10m_lakes")[0]
    renderer = layer.renderer()
    symbol = renderer.symbol()
    symbol.setColor(QColor("#0000ff"))
    layer.triggerRepaint()
    iface.layerTreeView().refreshLayerSymbology(layer.id())

    if visibility == False:
        root = QgsProject.instance().layerTreeRoot()
        country_layer = root.findLayer(layer.id())
        if country_layer is not None:
            country_layer.setItemVisibilityChecked(False)


# Natural Earth: Roads

def ne_roads(visibility=False):

    overlay = QgsProject.instance().mapLayersByName(country)[0]
    input = QgsProject.instance().mapLayersByName('ne_10m_roads')[0]
    output = f"{out_dir}/{country}_ne_10m_roads.shp"
    params = {'INPUT': input, 'OVERLAY': overlay, 'OUTPUT': output}
    result = processing.runAndLoadResults("qgis:clip", params)

    # Roads as lines of width 0.5
    # AI code

    layer = QgsProject.instance().mapLayersByName(f"{country}_ne_10m_roads")[0]
    line_symbol = QgsLineSymbol.createSimple({'color': 'orange', 'width': '0.5'})
    layer.setRenderer(QgsSingleSymbolRenderer(line_symbol))
    layer.triggerRepaint()
    iface.layerTreeView().refreshLayerSymbology(layer.id())

    if visibility == False:
        root = QgsProject.instance().layerTreeRoot()
        country_layer = root.findLayer(layer.id())
        if country_layer is not None:
            country_layer.setItemVisibilityChecked(False)

                                      
# Natural Earth: Railroads

def ne_railroads(visibility=False):

    overlay = QgsProject.instance().mapLayersByName(country)[0]
    input = QgsProject.instance().mapLayersByName('ne_10m_railroads')[0]
    output = f"{out_dir}/{country}_ne_10m_railroads.shp"
    params = {'INPUT': input, 'OVERLAY': overlay, 'OUTPUT': output}
    result = processing.runAndLoadResults("qgis:clip", params)

    # Add ticks to railroads
    # AI code, modified
    # May also be a railroad symbol in QGIS by default

    layer = QgsProject.instance().mapLayersByName(f"{country}_ne_10m_railroads")[0]
    line_symbol = QgsLineSymbol.createSimple({'color': 'black', 'width': '0.5'})
    marker_line = QgsMarkerLineSymbolLayer().create({'placement': 'interval', 'interval': '10', 'offset': '0'})
    simple_marker = QgsSimpleMarkerSymbolLayer()
    simple_marker.setShape(QgsSimpleMarkerSymbolLayer.Shape.Cross)
    simple_marker.setColor(QColor('black'))
    simple_marker.setSize(2)
    simple_marker.setStrokeWidth(0.5)
    marker_line.setSubSymbol(QgsSymbol.defaultSymbol(layer.geometryType()))
    marker_line.subSymbol().changeSymbolLayer(0, simple_marker)
    line_symbol.appendSymbolLayer(marker_line)
    layer.setRenderer(QgsSingleSymbolRenderer(line_symbol))
    layer.triggerRepaint()
    iface.layerTreeView().refreshLayerSymbology(layer.id())

    if visibility == False:
        root = QgsProject.instance().layerTreeRoot()
        country_layer = root.findLayer(layer.id())
        if country_layer is not None:
            country_layer.setItemVisibilityChecked(False)


# Natural Earth: Urban areas

def ne_urban_areas(visibility=False):

    overlay = QgsProject.instance().mapLayersByName(country)[0]
    input = QgsProject.instance().mapLayersByName('ne_10m_urban_areas')[0]
    output = f"{out_dir}/{country}_ne_10m_urban_areas.shp"
    params = {'INPUT': input, 'OVERLAY': overlay, 'OUTPUT': output}
    result = processing.runAndLoadResults("qgis:clip", params)

    layer = QgsProject.instance().mapLayersByName(f"{country}_ne_10m_urban_areas")[0]
    renderer = layer.renderer()
    symbol = renderer.symbol()
    symbol.setColor(QColor("#808080"))
    layer.triggerRepaint()
    iface.layerTreeView().refreshLayerSymbology(layer.id())

    if visibility == False:
        root = QgsProject.instance().layerTreeRoot()
        country_layer = root.findLayer(layer.id())
        if country_layer is not None:
            country_layer.setItemVisibilityChecked(False)


# Natural Earth: Populated places

def ne_populated_places(visibility=False):

    overlay = QgsProject.instance().mapLayersByName(country)[0]
    input = QgsProject.instance().mapLayersByName('ne_10m_populated_places_simple')[0]
    output = f"{out_dir}/{country}_ne_10m_populated_places_simple.shp"
    params = {'INPUT': input, 'OVERLAY': overlay, 'OUTPUT': output}
    result = processing.runAndLoadResults("qgis:clip", params)

    layer = QgsProject.instance().mapLayersByName(f"{country}_ne_10m_populated_places_simple")[0]
    renderer = layer.renderer()
    symbol = renderer.symbol()
    symbol.setColor(QColor("#ff0000"))
    symbol.setSize(2)
    layer.triggerRepaint()
    iface.layerTreeView().refreshLayerSymbology(layer.id())

    # Add names to populated places
    # AI code, 2 rounds, added comments

    layer = QgsProject.instance().mapLayersByName(f"{country}_ne_10m_populated_places_simple")[0]
    layer_settings = QgsPalLayerSettings()
    layer_settings.fieldName = "name"
    layer_settings.placement = QgsPalLayerSettings.OverPoint # Place label over point
    layer_settings.enabled = True
    text_format = QgsTextFormat() # Black text
    text_format.setFont(QFont("Arial", 10))
    text_format.setSize(10)
    text_format.setColor(QColor("black"))
    buffer_settings = QgsTextBufferSettings() # White buffer
    buffer_settings.setEnabled(True)
    buffer_settings.setSize(1)
    buffer_settings.setColor(QColor("white"))
    text_format.setBuffer(buffer_settings)
    layer_settings.setFormat(text_format)
    labeling = QgsVectorLayerSimpleLabeling(layer_settings)
    layer.setLabelsEnabled(True)
    layer.setLabeling(labeling)
    layer.triggerRepaint()
    iface.layerTreeView().refreshLayerSymbology(layer.id())

    if visibility == False:
        root = QgsProject.instance().layerTreeRoot()
        country_layer = root.findLayer(layer.id())
        if country_layer is not None:
            country_layer.setItemVisibilityChecked(False)


# Daylightmap Landcover

def daylightmap_landcover(visibility=False):

    overlay = QgsProject.instance().mapLayersByName(country)[0]
    input = QgsProject.instance().mapLayersByName('low')[0]
    output = f"{out_dir}/{country}_low.shp"
    params = {'INPUT': input, 'OVERLAY': overlay, 'OUTPUT': output}
    result = processing.runAndLoadResults("qgis:clip", params)

    # Add colors by landcover type
    # AI code, modified

    # From the attribute table

    # 1 = trees
    # 2 = shrub
    # 3 = grass
    # 4 = crop
    # 5 = urban
    # 6 = barren
    # 7 = snow

    layer = QgsProject.instance().mapLayersByName(f"{country}_low")[0]
    categories = []
    landcover_types = layer.uniqueValues(layer.fields().indexFromName('class'))
    for landcover_type in landcover_types:
        if landcover_type == 'trees':
            color = '#33a02c'
        elif landcover_type == 'shrub':
            color = '#ffffb2'
        elif landcover_type == 'grass':
            color = '#b2df8a'
        elif landcover_type == 'crop':
            color = '#ff7f00'
        elif landcover_type == 'urban':
            color = '#e31a1c'
        elif landcover_type == 'barren':
            color = '#beb297'
        elif landcover_type == 'snow':
            color = '#ffffff'
        else:
            color = '#000000' # Unknown
        symbol = QgsSymbol.defaultSymbol(layer.geometryType())
        symbol.setColor(QColor(color))
        symbol.setOpacity(0.4) # Balance between visibility of colors and obscuring other layers
        category = QgsRendererCategory(landcover_type, symbol, str(landcover_type))
        categories.append(category)
    field = QgsField('class', QVariant.Int)
    renderer = QgsCategorizedSymbolRenderer(field.name(), categories)
    if renderer is not None:
        layer.setRenderer(renderer)
        layer.triggerRepaint()
        iface.layerTreeView().refreshLayerSymbology(layer.id())

    if visibility == False:
        root = QgsProject.instance().layerTreeRoot()
        country_layer = root.findLayer(layer.id())
        if country_layer is not None:
            country_layer.setItemVisibilityChecked(False)



# Raster data layers to be clipped to country
# -------------------------------------------

# Similar to vector

# https://docs.qgis.org/3.40/en/docs/user_manual/processing_algs/gdal/rasterextraction.html#clip-raster-by-mask-layer
# Derived from gdalwarp

# Elevation: Natural Earth HYP_HR_SR

def ne_elevation_hyp_hr_sr(visibility=False):

    mask = QgsProject.instance().mapLayersByName(country)[0]
    input = QgsProject.instance().mapLayersByName('HYP_HR_SR')[0]
    output = f"{out_dir}/{country}_HYP_HR_SR.tif"
    params = {'INPUT': input, 'MASK': mask, 'OUTPUT': output}
    result = processing.run("gdal:cliprasterbymasklayer", params) # This redraws the layer
    clipped_raster = QgsRasterLayer(output, "Clipped Raster")
    QgsProject.instance().addMapLayer(clipped_raster)
    raster_name = f"{country}_HYP_HR_SR"
    clipped_raster.setName(raster_name)

    # Define clipped raster zero values as no data (AI)
    # This assumes in-country values are non-zero
    # But renders zero values outside the country transparent, not black

    provider = clipped_raster.dataProvider()
    provider.setNoDataValue(1, 0) # 1 is band number, 0 is no data value
    clipped_raster.triggerRepaint()
    iface.layerTreeView().refreshLayerSymbology(clipped_raster.id())

    # Make mask country have transparent fill (AI)

    fill_symbol = QgsSymbol.defaultSymbol(mask.geometryType())
    fill_symbol.setColor(QColor(0, 0, 255, 0)) # Transparent fill
    mask.setRenderer(QgsSingleSymbolRenderer(fill_symbol))
    mask.triggerRepaint()
    iface.layerTreeView().refreshLayerSymbology(mask.id())

    if visibility == False:
        root = QgsProject.instance().layerTreeRoot()
        country_layer = root.findLayer(clipped_raster.id())
        if country_layer is not None:
            country_layer.setItemVisibilityChecked(False)


# Landscan population density
# (AI "add population density raster", point to Landscan)

def landscan_population_density(visibility=False):

    mask = QgsProject.instance().mapLayersByName(country)[0]
    input = QgsProject.instance().mapLayersByName('landscan-global-2023-colorized')[0]
    output = f"{out_dir}/{country}_landscan-global-2023-colorized.tif"
    params = {'INPUT': input, 'MASK': mask, 'OUTPUT': output}
    result = processing.run("gdal:cliprasterbymasklayer", params)
    clipped_raster = QgsRasterLayer(output, "Clipped Raster")
    QgsProject.instance().addMapLayer(clipped_raster)
    raster_name = f"{country}_gpw_v4_landscan-global-2023-colorized"
    clipped_raster.setName(raster_name)
    provider = clipped_raster.dataProvider()
    provider.setNoDataValue(1, 0)
    clipped_raster.triggerRepaint()
    iface.layerTreeView().refreshLayerSymbology(clipped_raster.id())

    if visibility == False:
        root = QgsProject.instance().layerTreeRoot()
        country_layer = root.findLayer(clipped_raster.id())
        if country_layer is not None:
            country_layer.setItemVisibilityChecked(False)


# Elevation: NOAA DEM

#mask = QgsProject.instance().mapLayersByName(country)[0]
#input = QgsProject.instance().mapLayersByName('ETOPO_2022_v1_30s_N90W180_bed')[0]
#output = f"{out_dir}/{country}_ETOPO_2022_v1_30s_N90W180_bed.tif"
#params = {'INPUT': input, 'MASK': mask, 'OUTPUT': output}
#result = processing.run("gdal:cliprasterbymasklayer", params)
#clipped_raster = QgsRasterLayer(output, "Clipped Raster")
#QgsProject.instance().addMapLayer(clipped_raster)
#raster_name = f"{country}_ETOPO_2022_v1_30s_N90W180_bed"
#clipped_raster.setName(raster_name)

# Elevation: Natural Earth SR_HR (b/w)
# Remove the black background outside the country, similar to HYP_HR_SR above

def ne_elevation_sr_hr(visibility=False):

    mask = QgsProject.instance().mapLayersByName(country)[0]
    input = QgsProject.instance().mapLayersByName('SR_HR')[0]
    output = f"{out_dir}/{country}_SR_HR.tif"
    params = {'INPUT': input, 'MASK': mask, 'OUTPUT': output}
    result = processing.run("gdal:cliprasterbymasklayer", params) # This redraws the layer
    clipped_raster = QgsRasterLayer(output, "Clipped Raster")
    QgsProject.instance().addMapLayer(clipped_raster)
    raster_name = f"{country}_SR_HR"
    clipped_raster.setName(raster_name)

    provider = clipped_raster.dataProvider()
    provider.setNoDataValue(1, 0)
    clipped_raster.triggerRepaint()
    iface.layerTreeView().refreshLayerSymbology(clipped_raster.id())

    fill_symbol = QgsSymbol.defaultSymbol(mask.geometryType())
    fill_symbol.setColor(QColor(0, 0, 255, 0))
    mask.setRenderer(QgsSingleSymbolRenderer(fill_symbol))
    mask.triggerRepaint()
    iface.layerTreeView().refreshLayerSymbology(mask.id())

    if visibility == False:
        root = QgsProject.instance().layerTreeRoot()
        country_layer = root.findLayer(clipped_raster.id())
        if country_layer is not None:
            country_layer.setItemVisibilityChecked(False)


# Climate zones
# Similar to population density above
# No data value is already defined in the original raster as 0

def koppen_geiger_climate_zones(visibility=False):

    mask = QgsProject.instance().mapLayersByName(country)[0]
    input = QgsProject.instance().mapLayersByName('koppen_geiger_0p00833333')[0]
    output = f"{out_dir}/{country}_koppen_geiger_0p00833333.tif"
    params = {'INPUT': input, 'MASK': mask, 'OUTPUT': output}
    result = processing.run("gdal:cliprasterbymasklayer", params)
    clipped_raster = QgsRasterLayer(output, "Clipped Raster")
    QgsProject.instance().addMapLayer(clipped_raster)
    raster_name = f"{country}_koppen_geiger_0p00833333"
    clipped_raster.setName(raster_name)
    if clipped_raster.isValid(): # Prevent AttributeError: 'NoneType' object has no attribute 'setOpacity' when no pixels in country
        clipped_raster.renderer().setOpacity(0.5)
    #provider = clipped_raster.dataProvider()
    #provider.setNoDataValue(1, 0)
    clipped_raster.triggerRepaint()
    iface.layerTreeView().refreshLayerSymbology(clipped_raster.id())

    if visibility == False:
        root = QgsProject.instance().layerTreeRoot()
        country_layer = root.findLayer(clipped_raster.id())
        if country_layer is not None:
            country_layer.setItemVisibilityChecked(False)


# Draw the layers
# ---------------

# With default set turned on
# Rasters get drawn below the vectors

daylightmap_landcover()
ne_states_and_provinces()
ne_rivers(visibility=True)
ne_lakes(visibility=True)
ne_roads()
ne_railroads()
ne_urban_areas(visibility=True)
ne_populated_places(visibility=True)

ne_elevation_hyp_hr_sr(visibility=True)
ne_elevation_sr_hr()
koppen_geiger_climate_zones()
landscan_population_density()

# Move the country border layer to the top
# AI code, modified
layer = QgsProject.instance().mapLayersByName(country)[0]
root = QgsProject.instance().layerTreeRoot()
country_layer = root.findLayer(layer.id())
root.insertChildNode(0, country_layer.clone())
root.removeChildNode(country_layer)
