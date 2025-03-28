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


class ProjectCost():

    def __init__(self, project_df):
        """
        project_df: Dataframe with information on location, scale and cost of projects
        
        """

        # Read in projects
        self.project_df = project_df


    def visualise_cost_estimates(self, plant):

        # Get data from project
        selected_df = self.project_df[self.project_df["Plant Name"]==plant]
        
        # Get data
        investment_cost = selected_df["Average production accounting for clean technology (billion $)"].astype(float) * 1000 / selected_df["Plant Capacity (Mtpa)"].astype(float) 
        tax_cost = selected_df["Carbon Tax per plant ($)"].astype(float)  / selected_df["Plant Capacity (Mtpa)"].astype(float)  / 1e+06
        subsidies = (selected_df["Emission Allowance per plant ($)"].astype(float) + selected_df["45Q: Tax Credit for Storage per Plant ($)"].astype(float) \
        + selected_df["45Q: Tax Credit for Enhanced Oil Recovery per Plant ($)"].astype(float) + selected_df["45V: Clean H2 production per plant"].astype(float)) / selected_df["Plant Capacity (Mtpa)"].astype(float)  / 1e+06 * -1

        # Produce visualisation
        df_visual = pd.DataFrame([[700, investment_cost.values[0], 0, subsidies.values[0]],[700, 0, tax_cost.values[0], 0]], columns=["Production Cost", "Cost of Decarbonisation Measures", "Carbon Tax", "Subsidy Support"], index=["Green", "Conventional"])

        # Select country
        st.bar_chart(df_visual)