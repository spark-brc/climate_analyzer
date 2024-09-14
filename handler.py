import pandas as pd
import streamlit as st
# read pcp file from SWAT formatß

def read_pcp():
    uploaded_file = st.sidebar.file_uploader("PCP file from SWAT")
    fordf = uploaded_file
    if uploaded_file:
        file_content = uploaded_file.readlines()[2].strip().split()


        st.write(file_content)
        print(fordf)
        # df = pd.read_csv(
        #             fordf,
        #             sep=r'\s+',
        #             skiprows=4,
        #             # header=0,
        #             )


        # tdf = st.expander('{} Dataframe for Simulated and Observed Stream Discharge'.format("PCP file from SWAT"))
        # tdf.dataframe(df)
        

        # with open(uploaded_file, 'r') as f:
        #     content = f.readlines()
        # doy = [int(i[:7]) for i in content[4:]]
        # date = pd.to_datetime(doy, format='%Y%j')
        # df = pd.DataFrame(index=date)
        # return df
