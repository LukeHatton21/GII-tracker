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


# Read in data
policy_df = pd.read_csv("./DATA/Country_Policy_Tracker.csv")

## Set up title and tables
st.title("🏭 Policy Interventions for Industrial Decarbonisation")
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🌐Policy Interventions", "🏭Cement", "🏭Steel", "🏭Chemicals",  "📝Changelog", "ℹ️About"])

# Plot the map of policy interventions for tab1
with tab1:
    st.header("Existing Policy Interventions")
    intervention = st.selectbox("Policy Intervention", ["Carbon Tax", "Emissions Allowance", "EOR Tax Credit", "H2 Tax Credit", "Carbon Price"], key="Policy")
    intervention_name = {"Carbon Tax": "Carbon Tax\n(US/tonne)", "Emissions Allowance":"Emissions Allowance\n(US/tonne)", "EOR Tax Credit":"EOR Tax Credit\n(US/tonne)", "H2 Tax Credit":"H2 Tax Credit\n(US/kg)", "Carbon Price":"Carbon Price\n(US/tonne)"}
    display_map(policy_df, intervention, intervention_name[intervention)
