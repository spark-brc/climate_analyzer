import streamlit as st

st.write("My app test")

import plotly.graph_objects as go
from plotly.colors import n_colors
import numpy as np
np.random.seed(1)



import numpy as np
from ridgeplot import ridgeplot
from ridgeplot.datasets import load_lincoln_weather


def yay():
    # Load test data
    df = load_lincoln_weather()

    # Transform the data into a 3D (ragged) array format of
    # daily min and max temperature samples per month
    months = df.index.month_name().unique()
    samples = [
        [
            df[df.index.month_name() == month]["Min Temperature [F]"],
            df[df.index.month_name() == month]["Max Temperature [F]"],
        ]
        for month in months
    ]
    print(samples)
    st.dataframe(samples)
    # And finish by styling it up to your liking!
    fig = ridgeplot(
        samples=samples,
        labels=months,
        coloralpha=0.5,
        bandwidth=4,
        kde_points=np.linspace(-25, 110, 400),
        spacing=0.33,
        linewidth=2,
    )
    fig.update_layout(
        title="Minimum and maximum daily temperatures in Lincoln, NE (2016)",
        height=650,
        width=950,
        font_size=14,
        plot_bgcolor="rgb(245, 245, 245)",
        colorscale="viridis",
        colormode="row-index",
        xaxis_gridcolor="white",
        yaxis_gridcolor="white",
        xaxis_gridwidth=2,
        yaxis_title="Month",
        xaxis_title="Temperature [F]",
        showlegend=False,
    )
    return fig



def yay2(df):
    tmin = df.min().min()
    tmax = df.max().max()
    fig = ridgeplot(
        samples=df.dropna().to_numpy(),
        labels=[str(i) for i in df.columns],
        coloralpha=0.5,
        colorscale="viridis",
        colormode="row-index",
        bandwidth=1,
        kde_points=np.linspace(tmin, tmax, 400),
        spacing=0.5,
        linewidth=1,
    )
    fig.update_layout(
        title="Minimum and maximum daily temperatures in Lincoln, NE (2016)",
        height=1000,
        width=950,
        font_size=14,
        plot_bgcolor="rgb(245, 245, 245)",
        xaxis_gridcolor="white",
        yaxis_gridcolor="white",
        xaxis_gridwidth=2,
        yaxis_title="Month",
        xaxis_title="Temperature [F]",
        showlegend=False,
    )
    return fig