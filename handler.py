import pandas as pd
import streamlit as st
from io import StringIO
from plotly.colors import n_colors

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
    

@st.cache_data
def read_tmp(df, var):
    years = df.index.year.unique()
    dff = pd.DataFrame()
    meanvals = []
    for y in years:
        dfj = df.loc[df.index.year == y, var]
        meanvals.append(dfj.mean())

        dfj.index = dfj.index.dayofyear
        dff = pd.concat([dff, dfj], axis=1, ignore_index=True)
    dff.columns = years
    data = dff.dropna().to_numpy()
    # data = dff.fillna(0).to_numpy()
    colors = n_colors('rgb(5, 200, 200)', 'rgb(200, 10, 10)', len(meanvals), colortype='rgb')
    return data, colors, years
    
@st.cache_data
def get_db(pcp_file, fdpcp_file):
    if pcp_file and fdpcp_file:
        dfp = pd.read_csv(
                    pcp_file,
                    sep=r'\s+',
                    skiprows=3,
                    # header=0,
                    names=["Year", "j", "pcp", "lat", "lon"],
                    na_values=-999
                    )
        year = dfp.iloc[0, 0]
        # st.write(info)
        dfp.index = pd.date_range(f'1/1/{year}', periods=len(dfp))
        dfp = dfp.loc[:, 'pcp']
        dfp = dfp.astype({"pcp": float})
    # if fdpcp_file:
        dffd = pd.read_excel(fdpcp_file, index_col=0, parse_dates=True)
        dffd.index = dffd.index.normalize()
        # dffd.index.name = "Date"
        dfp = pd.concat([dfp, dffd], axis=1)
        dfp.dropna(axis=0, inplace=True)
        dfp.index.name = "Time"
    return dfp

def table_(pcp_file, fdpcp_file):
    dfp = get_db(pcp_file, fdpcp_file)
    
    return dfp


@st.cache_data
def get_db02(tmp_file, pcp_file):
    if tmp_file:
        dft = pd.read_csv(
                    tmp_file,
                    sep=r'\s+',
                    skiprows=3,
                    # header=0,
                    names=["Year", "j", "tmax", "tmin"],
                    na_values=-999
                    )
        year = dft.iloc[0, 0]
        dft = dft.loc[:, ["Year", "tmax", "tmin"]]
        # st.write(info)
        dft.index = pd.date_range(f'1/1/{year}', periods=len(dft))
        dft.index.name = "Date"
        dft["tmean"] = (dft["tmax"] + dft["tmin"])/2
    if pcp_file:
        dfp = pd.read_csv(
                    pcp_file,
                    sep=r'\s+',
                    skiprows=3,
                    # header=0,
                    names=["Year", "j", "pcp", "lat", "lon"],
                    na_values=-999
                    )
        year = dfp.iloc[0, 0]
        # st.write(info)
        dfp.index = pd.date_range(f'1/1/{year}', periods=len(dfp))
        dft["pcp"] = dfp.loc[:, "pcp"]
    return dft





def read_adj_his():
    df = pd.read_excel("./data/adjusted-historical.xlsx", index_col=0, parse_dates=True)
    df.index = df.index.normalize()
    return df







def show_df(uploaded_file):
    df = read_pcp(uploaded_file)



        

        # with open(uploaded_file, 'r') as f:
        #     content = f.readlines()
        # doy = [int(i[:7]) for i in content[4:]]
        # date = pd.to_datetime(doy, format='%Y%j')
        # df = pd.DataFrame(index=date)
        # return df


if __name__ == '__main__':
    # main()
    # df = main_alpha()
    # df = df.loc[:, "Precipitation"].groupby(df.index.year)

    # print(df[2010])
    # print(df[2010])
    # main_tmp()
    # plotviolin()
    # st.plotly_chart(plotviolin(), use_container_width=True)
    read_adj_his()