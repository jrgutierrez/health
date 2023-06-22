import streamlit as st
import plotly.express as px
from data import get_data

st.set_page_config(layout="wide")



# Perform SQL query on the Google Sheet.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
#@st.cache_data(ttl=600)

data = get_data()


initial_date = st.sidebar.date_input(
    "Selecciona fecha inicio",
    data.index[0])

final_date = st.sidebar.date_input(
    "Selecciona fecha fin",
    data.index[-1])


data = data.loc[initial_date:final_date]

fig = px.line(data, x = data.index, y = 'weight', markers = True)
fig.update_layout(legend=dict(
    yanchor="top",
    y=1.5,
    xanchor="left",
    x=0.01
))

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