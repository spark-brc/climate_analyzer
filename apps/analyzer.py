import streamlit as st

st.write("My app test")

import plotly.graph_objects as go

from plotly.subplots import make_subplots
from plotly.colors import n_colors
import numpy as np
np.random.seed(1)

import numpy as np
import pandas as pd
from ridgeplot import ridgeplot
from ridgeplot.datasets import load_lincoln_weather

import handler


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



def viz_pcp(df):
    pcp = df.iloc[:, 0].dropna().to_numpy()
    adjp = df.iloc[:, 1].dropna().to_numpy()
    neg_adjp = adjp[adjp < 0]
    fig = go.Figure()
    fig.add_trace(
        go.Violin(
            x=adjp, 
            name='Adjusted',
            legendrank=500
            ))
    fig.add_trace(
        go.Violin(
            x=pcp, 
            name='pcp',
            legendrank=1
            ))
    fig.update_traces(
                    orientation='h', 
                    side='positive', 
                    width=3, 
                    points="outliers",
                    meanline_visible=True,
                    )
    fig.add_trace(
        go.Scatter(
            x=neg_adjp, y=["Adjusted"]*len(neg_adjp), mode='markers', 
            name=f"Negative Values({len(neg_adjp)})",
            legendrank=1000
            ))
    fig.update_layout(
        # title="Minimum and maximum daily temperatures in Lincoln, NE (2016)",
        height=500,
        width=950,
        font_size=14,
        plot_bgcolor="rgb(245, 245, 245)",
        xaxis_gridcolor="white",
        yaxis_gridcolor="white",
        xaxis_gridwidth=2,
        yaxis_title="Dataset",
        # xaxis_title=xtitle,
        showlegend=True,
    )
    return fig


def viz_pcp_dec(df):
    df['decade'] = df.index.year // 10 * 10
    print(df.decade.unique())
    rows = len(df.decade.unique())
    cols = 1
    fig = make_subplots(rows=rows, cols=cols,shared_yaxes=True, shared_xaxes=True)

    for i, dc in enumerate(df.decade.unique(), start=1):
        dfd = df.loc[df["decade"]==dc]
        pcp = dfd.iloc[:, 0].dropna().to_numpy()
        adjp = dfd.iloc[:, 1].dropna().to_numpy()
        neg_adjp = adjp[adjp < 0]
        fig.add_trace(
            go.Violin(
                x=adjp, 
                name='Adjusted',
                legendrank=500
                ), row=i, col=cols)
        fig.add_trace(
            go.Violin(
                x=pcp, 
                name='pcp',
                legendrank=1
                ), row=i, col=cols)
        fig.update_traces(
                        orientation='h', 
                        side='positive', 
                        width=3, 
                        points="outliers",
                        meanline_visible=True,
                        )
    for i, dc in enumerate(df.decade.unique(), start=1):
        dfd = df.loc[df["decade"]==dc]
        pcp = dfd.iloc[:, 0].dropna().to_numpy()
        adjp = dfd.iloc[:, 1].dropna().to_numpy()
        neg_adjp = adjp[adjp < 0]      
        fig.add_trace(
            go.Scatter(
                x=neg_adjp, y=["Adjusted"]*len(neg_adjp), mode='markers', 
                name=f"Negative Values({len(neg_adjp)})",
                legendrank=1000
                ), row=i, col=cols)

        fig.update_layout(
            # title="Minimum and maximum daily temperatures in Lincoln, NE (2016)",
            height=1000,
            width=950,
            font_size=14,
            plot_bgcolor="rgb(245, 245, 245)",
            xaxis_gridcolor="white",
            yaxis_gridcolor="white",
            xaxis_gridwidth=2,
            # yaxis_title=f"{dc}'s",
            # xaxis_title=xtitle,
            # showlegend=False,
        )
    # edit axis labels
    for i, dc in enumerate(df.decade.unique(), start=1):
        fig['layout'][f'yaxis{i}']['title']=f'{dc}s'
    return fig

def fdc(df, ext_th):
    data, exd = convert_fdc_data(df.iloc[:, 0].values)
    
    idx_ext = np.argmax(exd * 100 > ext_th)
    value_ext = data[idx_ext-1]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=exd*100, y=data, mode='markers', 
            ))
    fig.add_vrect(x0=0, x1=ext_th, 
                annotation_text=f"extreme: >{value_ext:.1f} mm", 
                annotation_position="top left",
                annotation=dict(font_size=14, font_family="Times New Roman"),
                fillcolor="red", opacity=0.25, line_width=0)
    # fig.update_yaxes(type="log")
    return fig


def convert_fdc_data(data):
    data = np.sort(data)[::-1]
    exd = np.arange(1.,len(data)+1) / len(data)
    return data, exd


def table_(df, ext_th):
    data, exd = convert_fdc_data(df.iloc[:, 0].values)
    idx_ext = np.argmax(exd * 100 > ext_th)
    value_ext = data[idx_ext-1]
    dft = pd.DataFrame()
    # extreme
    ext_df = df[df >value_ext].groupby(df.index.year).agg('count')
    # dry
    dry_df = df[df <= 0].groupby(df.index.year).agg('count')
    # wet
    wet_df = df[df > 0].groupby(df.index.year).agg('count')
    # drizzle
    drz_df = df[(df > 0) & (df <= 0.1)].groupby(df.index.year).agg('count')
    # normal
    norm_df = df[(df > 0.1) & (df <=value_ext)].groupby(df.index.year).agg('count')
    # print(df.groupby(df.index.year).mean())
    dft = pd.concat([dry_df, wet_df, drz_df, norm_df, ext_df], axis=1)
    colnams = ["Dry <=0", "Wet > 0", "Drizzle 0 - 0.1", f"Normal 0.1 - {value_ext}", f"Extreme > {value_ext}"]
    dft.columns = pd.MultiIndex.from_product([colnams, df.columns])
    
    print(dft.loc[:, ("Dry <=0")])
    return dft


# def table_viz(df, ext_th):

#     fig = go.Figure()

#     fig.add_trace(
#         go.Violin(
#             x=data_line, 
#             line_color=color, 
#             # colorscale="Bluered_r",
#             # color_continuous_scale="rainbow",
#             name=y
#             )
#             # use_colorscale=True
#             )

def viz(data, colors, years, var):
    if var == "pcp":
        xtitle = r"Precipitation (mm)"
    else:
        xtitle = "Temperature (C<sup>0</sup>)"
    fig = go.Figure()
    for data_line, color, y in zip(data.T, colors, years):
        fig.add_trace(
            go.Violin(
                x=data_line, 
                line_color=color, 
                # colorscale="Bluered_r",
                # color_continuous_scale="rainbow",
                name=y
                )
                # use_colorscale=True
                )
    # fig = go.Figure()
    # for data_line, color, y in zip(data, co_df.colrs.tolist(), years):
    #     fig.add_trace(
    #         go.Violin(
    #             x=data_line, 
    #             line_color=color, 
    #             # colorscale="Bluered_r",
    #             name=y
    #             )
    #             # use_colorscale=True
    #             )
    fig.update_traces(
                    orientation='h', 
                    side='positive', 
                    width=3, 
                    points="outliers",
                    meanline_visible=True,
                    )
    fig.update_layout(
        # title="Minimum and maximum daily temperatures in Lincoln, NE (2016)",
        height=1000,
        width=950,
        font_size=14,
        plot_bgcolor="rgb(245, 245, 245)",
        xaxis_gridcolor="white",
        yaxis_gridcolor="white",
        xaxis_gridwidth=2,
        yaxis_title="Year",
        xaxis_title=xtitle,
        showlegend=True,
    )

    return fig


def viz_mon(dft, var):

    # data, colors, years = handler.read_tmp(tmp_file)
    # print(data)
    df = dft.loc[:, var]

    rows =4
    cols =3

    fig = make_subplots(rows=rows, cols=cols,shared_yaxes=True)

    x = 1
    for i in range(1, rows + 1):
        for j in range(1, cols + 1):
            dfm = df.loc[df.index.month==x]
            x = x + 1
            years = dfm.index.year.unique()
            dff = pd.DataFrame()
            for y in years:
                dfj = dfm.loc[dfm.index.year == y]
                dfj.index = dfj.index.dayofyear
                dff = pd.concat([dff, dfj], axis=1, ignore_index=True)
            dff.columns = years
            data = dff.dropna().to_numpy()
            colors = n_colors('rgb(5, 200, 200)', 'rgb(200, 10, 10)', len(years), colortype='rgb')

            for data_line, color, y in zip(data.T, colors, years):
                fig.add_trace(
                    go.Violin(
                        x=data_line, 
                        line_color=color, 
                        name=y
                            ), row=i, col=j)
                # print(f'm:{x}')
                # x = x + 1

    fig.update_traces(
                    orientation='h', 
                    side='positive', 
                    width=3, 
                    points="outliers",
                    meanline_visible=True,
                    )
    
    fig.update_layout(
        # title="Minimum and maximum daily temperatures in Lincoln, NE (2016)",
        height=3000,
        width=950,
        font_size=14,
        plot_bgcolor="rgb(245, 245, 245)",
        xaxis_gridcolor="white",
        yaxis_gridcolor="white",
        xaxis_gridwidth=2,
        yaxis_title="Year",
        showlegend=False,
    )
    return fig    
    
   
def bar_(df, ext_th):
    dft = table_(df, ext_th)
    dff = dft.loc[:, ("Dry <=0")]
    x = dft.index
    fig = go.Figure(data=[go.Bar(
        name = 'Data 1',
        x = x,
        y = dft.loc[:, ("Dry <=0", "pcp")]
    ),
        go.Bar(
        name = 'Data 2',
        x = x,
        y = dft.loc[:, ("Dry <=0", "pr")]
    )
    ])

def bar_(df, ext_th):
    data1, exd = convert_fdc_data(df.iloc[:, 0].values)
    idx_ext = np.argmax(exd * 100 > ext_th)
    value_ext = data1[idx_ext-1]


    dft = table_(df, ext_th)

    rows = 5
    cols = 1
    colnams = ["Dry <=0", "Wet > 0", "Drizzle 0 - 0.1", f"Normal 0.1 - {value_ext}", f"Extreme > {value_ext}"]
    fig = make_subplots(
        rows=rows, cols=cols,shared_yaxes=True, shared_xaxes=True,
        subplot_titles=colnams,
        y_title='Your master y-title',
        )
    for i, c in enumerate(colnams, start=1):
        dff = dft.loc[:, (c)]
        x = dft.index
        fig.add_trace(go.Bar(
            name = 'CHIRPS',
            x = x,
            y = dft.loc[:, (c, "pcp")]),
            row=i, col=cols)
        fig.add_trace(go.Bar(
            name = '팜두레',
            x = x,
            y = dft.loc[:, (c, "pr")]), 
            row=i, col=cols)

    fig.update_layout(
        # title="Minimum and maximum daily temperatures in Lincoln, NE (2016)",
        height=1000,
        width=950,
        font_size=14,
        plot_bgcolor="rgb(245, 245, 245)",
        xaxis_gridcolor="white",
        yaxis_gridcolor="white",
        xaxis_gridwidth=2,
        # yaxis_title="Number of events",
        # xaxis_title=xtitle,
        # showlegend=True,
    )

    # edit axis labels
    # for i, c in enumerate(colnams, start=1):
    #     fig['layout'][f'yaxis{i}']['title']=f'{c}'
    return fig






        # fig.add_trace(go.Bar(x=[1, 2, 3], y=[4, 5, 6],
        #                     marker=dict(color=[4, 5, 6], coloraxis="coloraxis")),
        #             1, i)

    #     # fig.add_trace(go.Bar(x=[1, 2, 3], y=[2, 3, 5],
    #     #                     marker=dict(color=[2, 3, 5], coloraxis="coloraxis")),
    #     #             1, 2)
