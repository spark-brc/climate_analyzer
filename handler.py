import pandas as pd
import streamlit as st
from io import StringIO

# read pcp file from SWAT formatß

@st.cache_data
def read_pcp(uploaded_file):
    if uploaded_file:
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
        return df
    

def show_df(uploaded_file):
    df = read_pcp(uploaded_file)



        

        # with open(uploaded_file, 'r') as f:
        #     content = f.readlines()
        # doy = [int(i[:7]) for i in content[4:]]
        # date = pd.to_datetime(doy, format='%Y%j')
        # df = pd.DataFrame(index=date)
        # return df
