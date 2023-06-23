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

st.number_input('label', min_value=1, max_value=60, value=15)

initial_date = st.sidebar.date_input(
    "Select initial date:",
    data.index[0])

final_date = st.sidebar.date_input(
    "Select final date:",
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
        fig1.update_traces(line_color='#ff0000')
        fig1.update_yaxes(title_font_color='#ff0000')
        fig2.update_traces(line_color='#0000ff', yaxis="y2")
        fig2.update_yaxes(title_font_color='#0000ff')
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

    fig = px.line(data, x = data.index, y = 'weight', markers = True, title = 'Weight - MA evolution', color_discrete_sequence=['#00ff00'])
    fig.add_scatter(x=data_roll.index, y=data_roll['weight'], mode='lines')
    fig.update_traces(showlegend=False)
    fig.update_layout(xaxis_title = 'Date', yaxis_title = 'Weight')
    st.plotly_chart(fig, use_container_width=True)

    fig = px.line(data, x = data.index, y = 'body_fat_rate', markers = True, title = 'Fat rate - MA evolution', color_discrete_sequence=['#00ff00'])
    fig.add_scatter(x=data_roll.index, y=data_roll['body_fat_rate'], mode='lines')
    fig.update_traces(showlegend=False)
    fig.update_layout(xaxis_title = 'Date', yaxis_title = 'Fat rate')
    st.plotly_chart(fig, use_container_width=True)

    fig = px.line(data, x = data.index, y = 'muscle_mass', markers = True, title = 'Muscle mass - MA evolution', color_discrete_sequence=['#00ff00'])
    fig.add_scatter(x=data_roll.index, y=data_roll['muscle_mass'], mode='lines')
    fig.update_traces(showlegend=False)
    fig.update_layout(xaxis_title = 'Date', yaxis_title = 'Muscle mass')
    st.plotly_chart(fig, use_container_width=True)


def forecast(data, var, forecast_days = 15):
    from statsmodels.tsa.arima.model import ARIMA
    import warnings
    warnings.filterwarnings('ignore')
    from datetime import datetime, timedelta

    y = data[var]

    ARIMAmodel = ARIMA(y, order = (5, 2, 5))
    ARIMAmodel = ARIMAmodel.fit()

    y_pred = ARIMAmodel.get_forecast(forecast_days)
    y_pred_df = y_pred.conf_int(alpha = 0.05) 
    y_pred_df["Predictions"] = ARIMAmodel.predict(start = y_pred_df.index[0], end = y_pred_df.index[-1])
    y_pred_df.index = [data.index[-1] + timedelta(days = i) for i in range(forecast_days)]
    return y_pred_df


def fc_plots():
    y_pred_out = forecast(data, 'weight')
    fig = px.line(data, x = data.index, y = 'weight', markers = True, title = 'Weight Forecast', color_discrete_sequence=['#00ff00'])
    fig.add_scatter(x=y_pred_out.index, y=y_pred_out['Predictions'], mode='markers+lines')
    fig.update_traces(showlegend=False)
    fig.update_layout(xaxis_title = 'Date', yaxis_title = 'Weight')
    st.plotly_chart(fig, use_container_width=True)

    y_pred_out = forecast(data, 'body_fat_rate')
    fig = px.line(data, x = data.index, y = 'body_fat_rate', markers = True, title = 'Fat rate Forecast', color_discrete_sequence=['#00ff00'])
    fig.add_scatter(x=y_pred_out.index, y=y_pred_out['Predictions'], mode='markers+lines')
    fig.update_traces(showlegend=False)
    fig.update_layout(xaxis_title = 'Date', yaxis_title = 'Fat rate')
    st.plotly_chart(fig, use_container_width=True)








if window == 'Overview':
    overview_plots()

if window == 'Moving Averages':
    ma_plots()

if window == 'Forecasting':
    fc_plots()