import ee
import streamlit as st
import geemap.foliumap as geemap

# Get an NLCD image by year.
def getRGB(year):
    # Import the NLCD collection.
    dataset = ee.ImageCollection("projects/neon-prod-earthengine/assets/DP3-30010-001").filterMetadata('NEON_SITE', 'equals', "HARV") 
    # Filter the collection by year.
    RGB = dataset.filter(ee.Filter.eq("system:index", year)).first()

    return RGB

# The main app.
def app():

    st.header("National Land Cover Database (NLCD)")

    # Create a layout containing two columns, one for the map and one for the layer dropdown list.
    row1_col1, row1_col2 = st.columns([3, 1])

    # Create an interactive map
    Map = geemap.Map()

    years = ["2018", "2019", "2020", "2021", "2022"]
    
    # Add a dropdown list and checkbox to the second column.
    with row1_col2:
        selected_year = st.multiselect("Select a year", years)
        add_legend = st.checkbox("Show legend")

    # Add selected NLCD image to the map based on the selected year.
    if selected_year:
        for year in selected_year:
            Map.addLayer(getRGB(year), {}, "NLCD " + year)

        if add_legend:
            Map.add_legend(
                title="NEON RGB", builtin_legend="RGB"
            )
        with row1_col1:
            Map.to_streamlit(height=600)

    else:
        with row1_col1:
            Map.to_streamlit(height=600)