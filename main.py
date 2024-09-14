import pandas as pd
import base64
# import utils
# from hydralit import HydraApp
# import apps
import streamlit as st
from ridgeplot import ridgeplot
import numpy as np

'''
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
from apps import test
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

def main():
    pcp_file = st.sidebar.file_uploader("PCP file from SWAT")
    if pcp_file:
        df_pcp = handler.read_pcp(pcp_file)
        df_pcp = df_pcp.groupby('Year')

        fig = ridgeplot(
            samples=df_pcp,
            bandwidth=4,
            # kde_points=np.linspace(-12.5, 112.5, 500),
            colorscale="viridis",
            colormode="row-index",
            coloralpha=0.65,
            # labels=column_names,
            linewidth=2,
            spacing=5 / 9,
        )



        print(df_pcp.head(5))
        tdf = st.expander('{} Dataframe for Simulated and Observed Stream Discharge'.format("PCP"))
        tdf.dataframe(df_pcp)


        # st.dataframe(df.loc[:, "Precipitation"])
        st.plotly_chart(test.yay())

    # handler.show_df(uploaded_file)
    
    # st.sidebar.image('./resources/TAMUAgriLifeResearchLogo.png',width=200)
    # st.sidebar.image('./resources/blm-logo.png', width=200)
    # st.markdown(footer,unsafe_allow_html=True)

    # over_theme = {'txc_inactive': '#FFFFFF'}
'''

def main_alpha():
    uploaded_file = "D:\\Projects\\Watersheds\\Ghana\\Analysis\\botanga\prj01\\Scenarios\\Default\\TxtInOut_rice_f\\AF_468597.pcp"
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

    # return df
        



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


if __name__ == '__main__':
    # main()
    df = main_alpha()
    # df = df.loc[:, "Precipitation"].groupby(df.index.year)

    # print(df[2010])
    # print(df[2010])
