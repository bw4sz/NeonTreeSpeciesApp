import ee
import streamlit as st
import geemap.foliumap as geemap
import geemap.colormaps as cm
import numpy as np

# Get an image by year.
def getRGB(year, site):
    # # Import the NEON image collection.
    start_date = ee.Date.fromYMD(year, 1, 1) 
    end_date = start_date.advance(1, "year")

    # Read in RGB NEON
    RGB = ee.ImageCollection('projects/neon-prod-earthengine/assets/DP3-30010-001').filterDate(start_date, end_date).filterMetadata('NEON_SITE', 'equals', site).first()

    return RGB

def getCrowns(site):
    features = ee.FeatureCollection("users/benweinstein2010/{}".format(site))
    return features

def getCentroid(feature):
        return feature.geometry().centroid()

# The main app.
def app():

    st.header("NEON RGB data")

    # Create a layout containing two columns, one for the map and one for the layer dropdown list.
    row1_col1, row1_col2 = st.columns([3, 1])

    # Create an interactive map
    Map = geemap.Map()

    years = [2018, 2019, 2020, 2021, 2022]
    sites = ["HARV", "BART", "OSBS"]

    # Add a dropdown list and checkbox to the second column.
    with row1_col2:
        selected_year = st.multiselect("Select years", years, default=2019)
        selected_site = st.selectbox("Select a site", sites)
        add_legend = st.checkbox("Show legend")

    # Add selected image to the map based on the selected year.
    crowns = getCrowns(selected_site)
    crown_centroids = crowns.map(getCentroid)

    if selected_year:
        for year in selected_year:
            selected_RGB = getRGB(year, selected_site)
            Map.addLayer(selected_RGB, {}, str(selected_site) + str(year))
        
        empty = ee.Image()
        painted_crowns = empty.paint(**{
        'featureCollection': crowns,
        'color': 'ens_label'})
        
        # Get dictionary features
        taxonID = crowns.aggregate_array("ensembleTa").getInfo()    
        taxonID = np.unique(taxonID)
        palette = cm.get_palette("Accent", n_class=len(taxonID))
        legend_dict = {x:y for x, y in zip(taxonID, palette)}
        Map.addLayer(painted_crowns, {"palette":palette, "width":1, "min":0, "max":len(taxonID)}, "Tree Species")
        
        vis_params = {
        'color': 'ff0000ff',
        'width': 2,
        'lineType': 'solid',
        'fillColor': '00000000',
        }

        Map.addLayer(crown_centroids.style(**vis_params),{}, "Tree Points")

        if add_legend:
            Map.add_legend(
                title="NEON RGB", legend_dict=legend_dict
            )
        Map.centerObject(selected_RGB,zoom=10)
        with row1_col1:
            Map.to_streamlit(height=600)

    else:
        with row1_col1:
            Map.to_streamlit(height=600)