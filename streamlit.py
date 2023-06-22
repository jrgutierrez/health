import streamlit as st
import plotly.express as px
from data import get_data

import matplotlib.pyplot as plt
import seaborn as sns
sns.set()


st.set_page_config(layout="wide")

data = get_data()

initial_date = st.sidebar.date_input(
    "Selecciona fecha inicio",
    data.index[0])

final_date = st.sidebar.date_input(
    "Selecciona fecha fin",
    data.index[-1])

data = data.loc[initial_date:final_date]


fig = px.line(data, x = data.index, y = 'weight', markers = True, color = 'green')
st.plotly_chart(fig, use_container_width=True)

fig = px.line(data, x = data.index, y = 'body_fat_rate', markers = True)
fig.update_layout(legend=dict(
    yanchor="top",
    y=1.5,
    xanchor="left",
    x=0.01
))

st.plotly_chart(fig, use_container_width=True)

fig = px.line(data, x = data.index, y = 'muscle_mass', markers = True)
fig.update_layout(legend=dict(
    yanchor="top",
    y=1.5,
    xanchor="left",
    x=0.01
))

st.plotly_chart(fig, use_container_width=True)