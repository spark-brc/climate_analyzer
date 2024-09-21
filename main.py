import pandas as pd
import base64
# import utils
# from hydralit import HydraApp
# import apps
import streamlit as st
from ridgeplot import ridgeplot
import numpy as np

import plotly.graph_objects as go
from plotly.colors import n_colors
import numpy as np
np.random.seed(1)



st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)
from apps import analyzer
import handler


pd.options.mode.chained_assignment = None


footer="""<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}
.footer {
position: fixed;
display:inline;
bottom: 0;
width: 170px;
background-color: transparent;
color: black;
text-align: center;
padding-bottom:140px;
}
</style>
<div class="footer">
<p>Developed by <a style='display: block; text-align: center;' href="https://spark-brc.github.io/" target="_blank">Seonggyu Park</a></p>
</div>
"""

st.sidebar.markdown(footer,unsafe_allow_html=True)


LOGO_IMAGE = "./resources/TAMUAgriLifeResearchLogo.png"
LOGO_IMAGE2 = "./resources/blm-logo.png"
st.sidebar.markdown(
    """
    <style>
    .container {
        display: flex;
    }
    .logo-text {
        font-weight:700 !important;
        font-size:50px !important;
        color: #f9a01b !important;
        padding-top: 75px !important;
    }
    .logo-img {
        z-index: 1;
        display:inline;
        position:fixed;
        bottom:0;
        padding-bottom:45px;
        width:120px;
        background-color: transparent;
        margin-left:25px;
    }
        .logo-img2 {
        z-index: 1;
        display:inline;
        position:fixed;
        bottom:0;
        margin-left:150px;
        padding-bottom:25px;
        width:90px;
        background-color: transparent;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# def main_ridgeplot():
#     pcp_file = st.sidebar.file_uploader("PCP file from SWAT")
#     if pcp_file:
#         df_pcp = handler.read_pcp(pcp_file)
#         df_pcp = df_pcp.groupby('Year')

#         fig = ridgeplot(
#             samples=df_pcp,
#             bandwidth=4,
#             # kde_points=np.linspace(-12.5, 112.5, 500),
#             colorscale="viridis",
#             colormode="row-index",
#             coloralpha=0.65,
#             # labels=column_names,
#             linewidth=2,
#             spacing=5 / 9,
#         )



#         print(df_pcp.head(5))
#         tdf = st.expander('{} Dataframe for Simulated and Observed Stream Discharge'.format("PCP"))
#         tdf.dataframe(df_pcp)


#         # st.dataframe(df.loc[:, "Precipitation"])
#         st.plotly_chart(test.yay())

#     # handler.show_df(uploaded_file)
    
#     # st.sidebar.image('./resources/TAMUAgriLifeResearchLogo.png',width=200)
#     # st.sidebar.image('./resources/blm-logo.png', width=200)
#     # st.markdown(footer,unsafe_allow_html=True)

#     # over_theme = {'txc_inactive': '#FFFFFF'}


def main2():
    pcp_file = st.sidebar.file_uploader("PCP file from SWAT")
    if pcp_file:
        df_pcp = handler.read_pcp(pcp_file)

    tmp_file = st.sidebar.file_uploader("TMP file from SWAT")
    if tmp_file:
        dff, data, colors, years = handler.read_tmp(tmp_file)
        st.plotly_chart(analyzer.viz(data, colors, years), use_container_width=True)

def main03():
    pcp_file = st.sidebar.file_uploader("PCP file from SWAT")
    tmp_file = st.sidebar.file_uploader("TMP file from SWAT")

    if tmp_file:
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(handler.get_db(tmp_file, pcp_file))
        with col2:
            var = st.selectbox(
                "How would you like to be contacted?",
                ("tmin", "tmax", "tmean", "pcp"),
                )
        dft = handler.get_db(tmp_file, pcp_file)
        # print(dft)
        data, colors, years = handler.read_tmp(dft, var)
        # handler.read_tmp(dft)
        st.plotly_chart(analyzer.viz(data, colors, years, var), use_container_width=True)
        st.plotly_chart(analyzer.viz_mon(dft, var), use_container_width=True)


def main():
    pcp_file = st.sidebar.file_uploader("PCP file from SWAT")
    fdpcp_file = st.sidebar.file_uploader("Adjusted Historical Data file from Farmdure(팜두레)")
    if pcp_file and fdpcp_file:
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(handler.get_db(pcp_file, fdpcp_file))
        st.plotly_chart(analyzer.viz_pcp(handler.get_db(pcp_file, fdpcp_file)), use_container_width=True)
        st.plotly_chart(analyzer.viz_pcp_dec(handler.get_db(pcp_file, fdpcp_file)), use_container_width=True)
        col3, col4 = st.columns([2, 3])
        with col3:
            ext_th = st.number_input(
                "Threshold for extreme event",
                min_value=1,
                value=10)
            st.plotly_chart(analyzer.fdc(handler.get_db(pcp_file, fdpcp_file), ext_th), use_container_width=True)
        with col4:
            st.dataframe(analyzer.table_(handler.get_db(pcp_file, fdpcp_file), ext_th))
        # st.line_chart(analyzer.table_(handler.get_db(pcp_file, fdpcp_file), ext_th))
        # st.dataframe(handler.table_(pcp_file, fdpcp_file))
        # analyzer.viz_pcp_dec(handler.get_db(pcp_file, fdpcp_file))
        st.plotly_chart(analyzer.bar_(handler.get_db(pcp_file, fdpcp_file), ext_th), use_container_width=True)



def main_alpha():
    
    uploaded_file = "./data/AF_468597.pcp"
    df = pd.read_csv(
                uploaded_file,
                sep=r'\s+',
                skiprows=3,
                # header=0,
                names=["Year", "j", "pcp", "lat", "lon"]
                )
    year = df.iloc[0, 0]
    df = df.loc[:, ["Year", "pcp"]]
    # st.write(info)
    df.index = pd.date_range(f'1/1/{year}', periods=len(df))
    # dff.columns = ['Precipitation']
    # st.write(dff.columns)
    df.rename(columns={"pcp":"Precipitation"}, inplace=True)
    df.index.name = "Date"


    years = df.index.year.unique()
    dff = pd.DataFrame()
    for y in years:
        dfj = df.loc[df.index.year == y, "Precipitation"]
        dfj.index = dfj.index.dayofyear
        # dfj.index = df.index.to_julian_date()
        dff = pd.concat([dff, dfj], axis=1, ignore_index=True)
        # dff[y] = df.loc[df.index.year == y]
    dff.columns = years

    # ss  = df.loc[df.index.year == 2019]
    # print(ss)
    print(dff.to_numpy())
    st.plotly_chart(analyzer.yay2(dff))

    # return df
        

def main_tmp():
    uploaded_file = "./data/AF_468597_TMP.tmp"
    df = pd.read_csv(
                uploaded_file,
                sep=r'\s+',
                skiprows=3,
                # header=0,
                names=["Year", "j", "tmax", "tmin"]
                )
    year = df.iloc[0, 0]
    df = df.loc[:, ["Year", "tmax", "tmin"]]
    # st.write(info)
    df.index = pd.date_range(f'1/1/{year}', periods=len(df))
    # dff.columns = ['Precipitation']
    # st.write(dff.columns)
    # df.rename(columns={"pcp":"Precipitation"}, inplace=True)
    df.index.name = "Date"


    years = df.index.year.unique()
    dff = pd.DataFrame()
    for y in years:
        dfj = df.loc[df.index.year == y, "tmax"]
        dfj.index = dfj.index.dayofyear
        # dfj.index = df.index.to_julian_date()
        dff = pd.concat([dff, dfj], axis=1, ignore_index=True)
        # dff[y] = df.loc[df.index.year == y]
    dff.columns = years

    # ss  = df.loc[df.index.year == 2019]
    # print(ss)
    print(dff.min().min())
    st.plotly_chart(analyzer.yay2(dff))


    #     }

    # st.sidebar.markdown(
    #     f"""
    #     <div class="container">
    #         <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open(LOGO_IMAGE, "rb").read()).decode()}">
    #         <img class="logo-img2" src="data:image/png;base64,{base64.b64encode(open(LOGO_IMAGE2, "rb").read()).decode()}">
    #     </div>
    #     """,
    #     unsafe_allow_html=True
    # )
    # complex_nav = {
    #         'Home': ['Home']
    # }
    # #and finally just the entire app and all the children.
    # app.run(complex_nav)




def create_color_list(min_val, max_val, num_colors):
    """Creates a list of colors based on min/max values."""

    cmap = plt.get_cmap('viridis')  # Choose your desired colormap
    norm = plt.Normalize(min_val, max_val)
    colors = [cmap(norm(value)) for value in np.linspace(min_val, max_val, num_colors)]
    return colors


def plotviolin():

    # 12 sets of normal distributed random data, with increasing mean and standard deviation
    # data = (np.linspace(1, 2, 12)[:, np.newaxis] * np.random.randn(12, 200) +
    #             (np.arange(12) + 2 * np.random.random(12))[:, np.newaxis])
    uploaded_file = "./data/AF_468597.pcp"
    df = pd.read_csv(
                uploaded_file,
                sep=r'\s+',
                skiprows=3,
                # header=0,
                names=["Year", "j", "pcp", "lat", "lon"]
                )
    year = df.iloc[0, 0]
    df = df.loc[:, ["Year", "pcp"]]
    df.index = pd.date_range(f'1/1/{year}', periods=len(df))
    df.index.name = "Date"
    years = df.index.year.unique()
    dff = pd.DataFrame()
    meanvals = []
    for y in years:
        dfj = df.loc[df.index.year == y, "pcp"]
        meanvals.append(dfj.mean())
        dfj.index = dfj.index.dayofyear
        dff = pd.concat([dff, dfj], axis=1, ignore_index=True)
    dff.columns = years
    data = dff.dropna().to_numpy()
    colors = n_colors('rgb(5, 200, 200)', 'rgb(200, 10, 10)', len(meanvals), colortype='rgb')
    # co_df = pd.DataFrame({"year":years, "mvals": meanvals})
    # co_df = co_df.sort_values('mvals')
    # co_df['colrs'] = colors
    # co_df = co_df.sort_values('year')

    fig = go.Figure()
    for data_line, color, y in zip(data.T, colors, years):
        print(data_line)
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




    fig.update_traces(orientation='h', side='positive', width=3, points="outliers",
                      meanline_visible=True,)
    # fig.show()

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
        showlegend=True,
    )
    return fig

if __name__ == '__main__':
    # main()
    # df = main_alpha()
    # df = df.loc[:, "Precipitation"].groupby(df.index.year)

    # print(df[2010])
    # print(df[2010])
    # main_tmp()
    # plotviolin()
    # st.plotly_chart(plotviolin(), use_container_width=True)
    main()