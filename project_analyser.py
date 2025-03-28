import streamlit as st
import folium
import pandas as pd
import numpy as np
import re
from streamlit_folium import st_folium
import altair as alt
import plotly.express as px
from scipy import stats
from datetime import datetime
from datetime import datetime
import os


class ProjectData():

    def __init__(self, project_df):
        """
        project_df: Dataframe with information on location, scale and cost of projects
        
        """

        # Read in projects
        self.project_df = project_df


    def visualise_project_capacity(self):

        # Add in information
        def generate_tooltip(row):
            plant_name = row['Plant Name']
            capacity = f"{row['Plant Capacity (Mtpa)']:.2f}"  
            emissions = f"{row['CO2 emitted per plant (without CCUS) (MtCO2/yr)']:.2f}"
            emission_intensity = f"{row['CO2 emitted per plant (without CCUS) (MtCO2/yr)']/row['Plant Capacity (Mtpa)']:0.2f}"
            tooltip_text = f"{plant_name}<br>Capacity: {capacity} Mtpa<br>Annual Emissions: {emissions} MtCO2/yr"
            tooltip_text =  re.sub(r'([\(])', r'<br>\1', tooltip_text)
            return tooltip_text
        

        # Create map
        map = folium.Map(location=[10, 0], zoom_start=1, control_scale=True, scrollWheelZoom=True, tiles='CartoDB positron')

        
        # Read in df
        df = self.project_df
        df.apply(lambda row:folium.CircleMarker(location=[row["Latitude"], row["Longitude"]], 
                                              radius=row["Plant Capacity (Mtpa)"], color="crimson", fill=True, fill_opacity=0.5, opacity=1, tooltip=generate_tooltip(row))
                                             .add_to(map).add_child(folium.Tooltip(generate_tooltip(row), max_width=10)), axis=1)
        
        
        # Display map
        st_map = st_folium(map, width=700, height=350)

        
