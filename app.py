import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

dataframe = pd.read_csv('co2emissions.csv')

st.set_page_config(
    page_title="EMISSÃO DE CO2",
    page_icon=":bar_chart:",
    layout="wide"
)

st.title("Visualização de Consumo de Combustível")
st.markdown("---")



st.sidebar.title("Filtros")
selected_brandings = st.sidebar.multiselect(
    label="Select a car brand",
    options=dataframe["Make"].unique()
)

car_type = st.sidebar.multiselect(
    label="Select a car class",
    options=dataframe["Vehicle Class"].unique()
)

dataframe_filtrado = dataframe[
    dataframe["Make"].isin(selected_brandings) &
    dataframe["Vehicle Class"].isin(car_type)
]

st.title("Visualização de Emissão de CO2")
st.markdown("---")

emissions_by_brand = dataframe.groupby("Make")["CO2 Emissions(g/km)"].mean().reset_index()
brand_fig = px.bar(emissions_by_brand, x="Make", y="CO2 Emissions(g/km)", title="Emissão Média de CO2 por Marca")
st.plotly_chart(brand_fig)

red_color = ['#FF0000'] 

consume_by_car = dataframe.groupby("Model")["Fuel Consumption Comb (mpg)"].mean().reset_index()
brand_fig = px.area(consume_by_car, x="Model", y="Fuel Consumption Comb (mpg)", title="Consumo médio por carro", color_discrete_sequence=red_color)
st.plotly_chart(brand_fig)

st.header("Comparação de Tipos de Carro por Marca")
selected_make = st.selectbox("Selecione uma marca para comparar tipos de carro", dataframe["Make"].unique())
make_filtered = dataframe[dataframe["Make"] == selected_make]
emissions_by_type = make_filtered.groupby("Vehicle Class")["CO2 Emissions(g/km)"].mean().reset_index()
type_fig = px.bar(emissions_by_type, x="Vehicle Class", y="CO2 Emissions(g/km)", title=f"Emissão Média de CO2 por Tipo de Carro - {selected_make}")
st.plotly_chart(type_fig)

# Métricas Gerais
total_emission = dataframe["CO2 Emissions(g/km)"].sum()
st.metric("Emissão total", total_emission)

total_cars = len(dataframe)
emission_average = round((total_emission / total_cars), 3)
st.metric("Média da emissão", emission_average)

# Dados Filtrados
st.header("Dados Filtrados")
st.dataframe(dataframe_filtrado)

# Conjunto de Dados Completo
st.markdown("---")
st.header("Conjunto de Dados Completo")
st.dataframe(dataframe)
