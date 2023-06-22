import streamlit as st
import plotly.express as px
from data import get_data
from plotly.subplots import make_subplots


st.set_page_config(layout="wide")

data = get_data()

window = st.sidebar.radio(
        "Select window 👇",
        options=["Overview", "Moving Averages", "Forecasting"],
    )

initial_date = st.sidebar.date_input(
    "Selecciona fecha inicio",
    data.index[0])

final_date = st.sidebar.date_input(
    "Selecciona fecha fin",
    data.index[-1])



data = data.loc[initial_date:final_date]

def overview_plots():
    fig = px.line(data, x = data.index, y = 'weight', markers = True, title = 'Weight evolution')
    fig.update_traces(line_color='#00ff00')
    fig.update_layout(xaxis_title = 'Date', yaxis_title = 'Weight')
    st.plotly_chart(fig, use_container_width=True)


    def plotly_dual_axis(data1,data2, title="", y1="", y2=""):
        subplot_fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig1 = px.line(data1, markers = True)
        fig2 = px.line(data2, markers = True)
        fig1.update_traces(line_color='#0000ff')
        fig1.update_yaxes(title_font_color='#0000ff')
        fig2.update_traces(line_color='#ff0000', yaxis="y2")
        fig2.update_yaxes(title_font_color='#ff0000')
        subplot_fig.add_traces(fig1.data + fig2.data)
        subplot_fig.update_layout(title=title, yaxis=dict(title=y1), yaxis2=dict(title=y2))
        newnames = {'body_fat_rate': 'Fat rate', 'muscle_mass': 'Muscle mass'}
        subplot_fig.for_each_trace(lambda t: t.update(name = newnames[t.name], legendgroup = newnames[t.name], hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name])))
        #subplot_fig.for_each_trace(lambda t: t.update(line=dict(color=t.marker.color)))
        return subplot_fig

    fig = plotly_dual_axis(data['body_fat_rate'], data['muscle_mass'], title = "Fat rate - Muscle mass evolution", y1 = "Fat rate", y2 = "Muscle mass")
    st.plotly_chart(fig, use_container_width=True)


def ma_plots():
    n_roll = 4
    data_roll = data.rolling(n_roll).mean()

    fig = px.line(data, x = data.index, y = 'weight', markers = True, title = 'Weight - MA evolution', color_discrete_sequence=['red'])
    fig.add_scatter(x=data_roll.index, y=data_roll['weight'], mode='lines')
    fig.update_traces(line_color='#00ff00', showlegend=False)
    fig.update_layout(xaxis_title = 'Date', yaxis_title = 'Weight')
    st.plotly_chart(fig, use_container_width=True)


def fc_plots():
    pass








if window == 'Overview':
    overview_plots()

if window == 'Moving Averages':
    ma_plots()

if window == 'Forecasting':
    fc_plots()