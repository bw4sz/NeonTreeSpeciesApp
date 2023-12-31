import streamlit as st
import os
import ee
from multiapp import MultiApp
from apps import home, basemaps, customize, datasets, opacity, nlcd_demo, NEON

st.set_page_config(layout="wide")

#SET EARTH ENGINE TOKEN
os.environ["EARTHENGINE_TOKEN"] = "/Users/benweinstein/.config/gcloud/application_default_credentials.json"
ee.Initialize()

apps = MultiApp()

# Add all your application here

apps.add_app("Home", home.app)
apps.add_app("Customize the default map", customize.app)
apps.add_app("Change basemaps", basemaps.app)
apps.add_app("Change opacity", opacity.app)
apps.add_app("Search datasets", datasets.app)
apps.add_app("NLCD Demo", nlcd_demo.app)
apps.add_app("NEON Trees", NEON.app)

# The main app
apps.run()
