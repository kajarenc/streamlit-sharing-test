import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.title("🥑 Avocado Analytics")


@st.cache
def load_data():
    data = pd.read_csv("avocado.csv")
    data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")
    data.sort_values("Date", inplace=True)
    return data


data = load_data()

region = st.sidebar.selectbox("Region", np.sort(data.region.unique()))
avocado_type = st.sidebar.selectbox("Avocado Type", data.type.unique())

start_date = st.sidebar.date_input("Start Date",
                                   data.Date.min().date(),
                                   min_value=data.Date.min().date(),
                                   max_value=data.Date.max().date(),
                                   )

end_date = st.sidebar.date_input("End Date",
                                 data.Date.max().date(),
                                 min_value=data.Date.min().date(),
                                 max_value=data.Date.max().date(),
                                 )

mask = ((data.region == region) &
        (data.type == avocado_type) &
        (data.Date >= pd.Timestamp(start_date)) &
        (data.Date <= pd.Timestamp(end_date)))
filtered_data = data.loc[mask, :]

price_chart_figure = {
    "data": [
        {
            "x": filtered_data["Date"],
            "y": filtered_data["AveragePrice"],
            "type": "scatter",
            "hovertemplate": "$%{y:.2f}<extra></extra>",
        },
    ],
    "layout": {
        "title": {
            "text": "Average Price of Avocados",
            "x": 0.05,
            "xanchor": "left"
        },
        "xaxis": {"fixedrange": True},
        "yaxis": {"tickprefix": "$", "fixedrange": True},
        "colorway": ["#17B897"],
    },
}

volume_chart_figure = {
    "data": [
        {
            "x": filtered_data["Date"],
            "y": filtered_data["Total Volume"],
            "type": "scatter",
        },
    ],
    "layout": {
        "title": {"text": "Avocados Sold", "x": 0.05, "xanchor": "left"},
        "xaxis": {"fixedrange": True},
        "yaxis": {"fixedrange": True},
        "colorway": ["#E12D39"],
    },
}

fig1 = go.Figure(price_chart_figure)
fig2 = go.Figure(volume_chart_figure)

st.plotly_chart(fig1)
st.plotly_chart(fig2)
