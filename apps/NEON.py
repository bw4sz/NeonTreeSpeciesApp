import ee
import streamlit as st
import geemap.foliumap as geemap

# Get an NLCD image by year.
def getRGB(year, site):
    # Import the NEON image collection.
    start_date = ee.Date.fromYMD(year, 1, 1) 
    end_date = start_date.advance(1, "year")
    dataset = ee.ImageCollection("projects/neon-prod-earthengine/assets/DP3-30010-001").filterDate(start_date, end_date).filterMetadata('NEON_SITE', 'equals', site).mosaic()
    print(dataset)
    
    return dataset

# The main app.
def app():

    st.header("NEON RGB data (NLCD)")

    # Create a layout containing two columns, one for the map and one for the layer dropdown list.
    row1_col1, row1_col2 = st.columns([3, 1])

    # Create an interactive map
    Map = geemap.Map()

    years = [2018, 2019, 2020, 2021, 2022]
    sites = ["HARV", "BART", "OSBS"]

    # Add a dropdown list and checkbox to the second column.
    with row1_col2:
        selected_year = st.multiselect("Select a year", years, default=2019)
        selected_site = st.multiselect("Select a site", sites, default="HARV")
        add_legend = st.checkbox("Show legend")

    # Add selected image to the map based on the selected year.
    if selected_year:
        for year in selected_year:
            selected_RGB = getRGB(year, selected_site), {}, str(selected_site) + str(year)
            Map.addLayer(selected_RGB)
            Map.centerObject(selected_RGB, 11);

        if add_legend:
            Map.add_legend(
                title="NEON RGB", builtin_legend="RGB"
            )
        with row1_col1:
            Map.to_streamlit(height=600)

    else:
        with row1_col1:
            Map.to_streamlit(height=600)