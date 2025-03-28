import streamlit as st
import folium
import pandas as pd
import numpy as np
from streamlit_folium import st_folium
import altair as alt
import plotly.express as px
from scipy import stats
from datetime import datetime
import os
from project_analyser import ProjectData
from project_cost_estimator import ProjectCost

def display_map(df, variable, variable_name, count=None):
    map = folium.Map(location=[10, 0], zoom_start=1, control_scale=True, scrollWheelZoom=True, tiles='CartoDB positron')
    df = df.rename(columns={"ISO3":"iso3_code"})
    if count is not None:
        threshold_scale = [1, 5, 15, 50, 100, max(df[variable])]
    else:
        threshold_scale=None
    choropleth = folium.Choropleth(
        geo_data='./DATA/country_boundaries.geojson',
        data=df,
        columns=('iso3_code', variable),
        key_on='feature.properties.iso3_code',
        line_opacity=0.8,
        highlight=True,
        fill_color="YlGnBu",
        nan_fill_color = "grey",
        legend_name="Datapoints",
        threshold_scale=threshold_scale,
    )
    choropleth.geojson.add_to(map)

    df_indexed = df.set_index('iso3_code')
    df_indexed = df_indexed.dropna(subset=variable)
    df_indexed = df_indexed[~df_indexed.index.duplicated(keep='first')]  # Remove duplicates

    for feature in choropleth.geojson.data['features']:
        iso3_code = feature['properties']['iso3_code']
        feature['properties'][variable] = (
            f"{df_indexed.loc[iso3_code, variable]:0.0f}" if iso3_code in df_indexed.index else "N/A"
        )


    choropleth.geojson.add_child(
    folium.features.GeoJsonTooltip(
        fields=['english_short', variable],  # Display these fields
        aliases=["Country:", variable_name],         # Display names for the fields
        localize=True,
        style="""
        background-color: #F0EFEF;
        border: 2px solid black;
        border-radius: 3px;
        box-shadow: 3px;
    """,
    max_width=400,
    )
)
    
    st_map = st_folium(map, width=700, height=350)

    country_name = ''
    if st_map['last_active_drawing']:
        country_name = st_map['last_active_drawing']['properties']['english_short']
    return country_name


## Set up title 
st.title("🏭 Policy Interventions for Industrial Decarbonisation")


# Set up selection for sector and tabs
sector = st.selectbox("Hard-to-abate sector", ["Iron and Steel"])
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🌐Policy Interventions", "🌎Existing Plants", "🏭Market Mechanisms",  "💳Cost Estimates", "📝Changelog", "ℹ️About"])

# Read in data
policy_df = pd.read_csv("./DATA/Country_Policy_Tracker.csv")
steel_df = pd.read_csv("./DATA/Iron_and_Steel.csv")
carbon_df = pd.read_csv("./DATA/CarbonData.csv")


# Call object to evaluate project level data
project_data_class = ProjectData(project_df=steel_df)
project_cost_class = ProjectCost(project_df=steel_df)


# Plot the map of policy interventions for tab1
with tab1:
    st.header("Existing Policy Interventions")
    intervention = st.selectbox("Policy Intervention", ["Carbon Tax", "Emissions Allowance", "EOR Tax Credit", "H2 Tax Credit", "Carbon Price"], key="Policy")
    intervention_name = {"Carbon Tax": "Carbon Tax\n(US/t)", "Emissions Allowance":"Emissions Allowance\n(US/t)", "EOR Tax Credit":"EOR Tax Credit\n(US/t)", "H2 Tax Credit":"H2 Tax Credit\n(US/kg)", "Carbon Price":"Carbon Price\n(US/tonne)"}
    display_map(policy_df, intervention, intervention_name[intervention])
with tab2:
    st.header("Global Plant Capacities")
    project_data_class.visualise_project_capacity()
with tab3:
    st.header("Carbon Pricing Instruments")
    st.write("TBC - Timeseries of emissions pricing in major markets")
    st.line_chart(data=carbon_df, x="Year", y=["EU", "US","UK"],y_label="Carbon Price (USD/t)")
with tab4:
    st.header("Cost Estimates")
    plant = st.selectbox("Country", options=sorted(steel_df["Plant Name"].unique()))
    project_cost_class.visualise_cost_estimates(plant)


with tab5: 
    st.header("About")
    st.header("Methods")
    st.header("Funding")
    st.header("License and Data Use Permissions")
    st.write("The data available here is licensed as Creative Commons Attribution-NonCommercial International (CC BY-NC 4.0), which means you are free to copy, " + 
            "redistribute and adapt it for non-commercial purposes, provided you give appropriate credit. If you wish to use the data for commercial purposes, " +
            "please get in touch to discuss commercial license pricing.")   
