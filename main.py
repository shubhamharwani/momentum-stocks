import pandas as pd
import numpy as np
import yfinance as yf
import time
import datetime as dt
import streamlit as st

st.set_page_config(page_title='Momentum Rank Screener',layout='centered',page_icon=':bar_chart:')

# NIFTY 50 STOCKS
nifty_50 = pd.read_csv(r'https://archives.nseindia.com/content/indices/ind_nifty50list.csv')
nifty_50 = nifty_50['Symbol'] + '.NS'
nifty_50_list = nifty_50.to_list()

# NIFTY SMALL CAP 250 STOCKS
nifty_250_sc = pd.read_csv(r'https://archives.nseindia.com/content/indices/ind_niftysmallcap250list.csv')
nifty_250_sc = nifty_250_sc['Symbol'] + '.NS'
nifty_250_sc_list = nifty_250_sc.to_list()

# NIFTY SMALL + MID CAP STOCKS (MID 150 + SMALL 250)
nifty_sml_400 = pd.read_csv(r'https://archives.nseindia.com/content/indices/ind_niftymidsmallcap400list.csv')
nifty_sml_400 = nifty_sml_400['Symbol'] + '.NS'
nifty_sml_400_list = nifty_sml_400.to_list()

# NIFTY TOP 500 STOCKS (NIFTY 50 + NIFTY NEXT 50 + NIFTY MID CAP 150 + NIFTY SMALL CAP 250)
nifty_500 = pd.read_csv(r'https://archives.nseindia.com/content/indices/ind_nifty500list.csv')
nifty_500 = nifty_500['Symbol'] + '.NS'
nifty_500_list = nifty_500.to_list()

universe_button = st.radio('Select Universe',('Nifty 50','Nifty Small Cap 250','Nifty Mid+Small 400','Nifty 500'))
st.write('Please have patience as downloading and calculating the data takes time.')

if universe_button == 'Nifty 50':
    tickers_list = nifty_50_list

if universe_button == 'Nifty Small Cap 250':
    tickers_list = nifty_250_sc_list

if universe_button == 'Nifty Mid+Small 400':
    tickers_list = nifty_sml_400_list

if universe_button == 'Nifty 500':
    tickers_list = nifty_500_list

with st.spinner('Please wait.'):
    df = yf.download(tickers = tickers_list, period = "1y", interval = "1d")

# fetch prices & set date to datetime format
prices = df['Adj Close']
prices.index = pd.to_datetime(prices.index)

# calculate monthly returns
yearly_ret = prices.pct_change().resample('Y').agg(lambda x: (x+1).prod() - 1)
yearly_ret = yearly_ret.T

frame2 = yearly_ret['2023-12-31']
frame2 = frame2.sort_values(ascending=False)

st.subheader('List of Top 20 Stocks in Momentum Over Last 1 Year')
st.write('Left Column: Stock Name, Right Column : Rank in % Returns')
st.dataframe(frame2.head(20),width=500,height=750)

#this is the css code to hide main menu button, stream logo at the bottom, top header colored ribbon
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
