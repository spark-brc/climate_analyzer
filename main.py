import pandas as pd
import base64
# import utils
# from hydralit import HydraApp
# import apps
import streamlit as st


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

    df_pcp = handler.read_pcp(pcp_file)
    tdf = st.expander('{} Dataframe for Simulated and Observed Stream Discharge'.format("PCP"))
    tdf.dataframe(df_pcp.loc[:, "Precipitation"], height=500)
    # st.dataframe(df.loc[:, "Precipitation"])
    st.plotly_chart(test.yay())

    # handler.show_df(uploaded_file)
    
    # st.sidebar.image('./resources/TAMUAgriLifeResearchLogo.png',width=200)
    # st.sidebar.image('./resources/blm-logo.png', width=200)
    # st.markdown(footer,unsafe_allow_html=True)

    # over_theme = {'txc_inactive': '#FFFFFF'}
    




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
    main()


