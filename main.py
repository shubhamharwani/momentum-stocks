import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
import streamlit as st
import requests
import random

st.set_page_config(page_title='Momentum Rank Screener',layout='centered',page_icon=':zap:')

NIFTY_50 = r'https://archives.nseindia.com/content/indices/ind_nifty50list.csv'
NIFTY_NEXT_50 = r'https://archives.nseindia.com/content/indices/ind_niftynext50list.csv'

NIFTY_100 = r'https://archives.nseindia.com/content/indices/ind_nifty100list.csv'
NIFTY_200 = r'https://archives.nseindia.com/content/indices/ind_nifty200list.csv'

NIFTY_MIDCAP_50 = r'https://archives.nseindia.com/content/indices/ind_niftymidcap50list.csv'
NIFTY_MIDCAP_100 = r'https://archives.nseindia.com/content/indices/ind_niftymidcap100list.csv'
NIFTY_MIDCAP_150 = r'https://archives.nseindia.com/content/indices/ind_niftymidcap150list.csv'

NIFTY_SMALLCAP_50 = r'https://archives.nseindia.com/content/indices/ind_niftysmallcap50list.csv'
NIFTY_SMALLCAP_100 = r'https://archives.nseindia.com/content/indices/ind_niftysmallcap100list.csv'
NIFTY_SMALLCAP_250 = r'https://archives.nseindia.com/content/indices/ind_niftysmallcap250list.csv'

NIFTY_LARGEMIDCAP_250 = r'https://archives.nseindia.com/content/indices/ind_niftylargemidcap250list.csv'
NIFTY_MIDSMALLCAP_400 = r'https://archives.nseindia.com/content/indices/ind_niftymidsmallcap400list.csv'

NIFTY_500 = r'https://archives.nseindia.com/content/indices/ind_nifty500list.csv'
NIFTY_MICROCAP_250 = r'https://archives.nseindia.com/content/indices/ind_niftymicrocap250_list.csv'

# definition to download the stock universe list
def universe(link):
    # new changes
    user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'
    ]
    
    headers = {'User-Agent': random.choice(user_agents)}
    response = requests.get(link, headers=headers)

    if response.status_code == 200:
        data = response.content.decode('utf-8')
    else:
        st.write('Failed to load CSV')
        st.stop()

    # old data
    universe = pd.read_csv(data)
    universe = universe['Symbol'] + '.NS'
    universe = universe.to_list()
    return universe

# radio button to select universe
universe_button = st.radio('Select Universe',('Nifty 50','Nifty Next 50','Nifty 100','Nifty 200',
                                              'Nifty Midcap 50','Nifty Midcap 100','Nifty Midcap 150',
                                              'Nifty Small Cap 50','Nifty Small Cap 100','Nifty Small Cap 250',
                                              'Nifty Large Mid Cap 250','Nifty Mid Small Cap 400',
                                              'Nifty 500','Nifty Micro Cap 250'))
st.write('Please have patience as downloading and calculating the data takes time.')

stocks = st.number_input('Number Of Stocks',1,1000,20)
allocation = st.number_input('Allocation In Each Stock (in ₹)',1,1000000,5000)

if universe_button == 'Nifty 50':
    tickers_list = universe(NIFTY_50)

if universe_button == 'Nifty Next 50':
    tickers_list = universe(NIFTY_NEXT_50)

if universe_button == 'Nifty 100':
    tickers_list = universe(NIFTY_100)

if universe_button == 'Nifty 200':
    tickers_list = universe(NIFTY_200)

if universe_button == 'Nifty Midcap 50':
    tickers_list = universe(NIFTY_MIDCAP_50)

if universe_button == 'Nifty Midcap 100':
    tickers_list = universe(NIFTY_MIDCAP_100)

if universe_button == 'Nifty Midcap 150':
    tickers_list = universe(NIFTY_MIDCAP_150)

if universe_button == 'Nifty Small Cap 50':
    tickers_list = universe(NIFTY_SMALLCAP_50)

if universe_button == 'Nifty Small Cap 100':
    tickers_list = universe(NIFTY_SMALLCAP_100)

if universe_button == 'Nifty Small Cap 250':
    tickers_list = universe(NIFTY_SMALLCAP_250)

if universe_button == 'Nifty Large Mid Cap 250':
    tickers_list = universe(NIFTY_LARGEMIDCAP_250)

if universe_button == 'Nifty Mid Small Cap 400':
    tickers_list = universe(NIFTY_MIDSMALLCAP_400)

if universe_button == 'Nifty 500':
    tickers_list = universe(NIFTY_500)

if universe_button == 'Nifty Micro Cap 250':
    tickers_list = universe(NIFTY_MICROCAP_250)


with st.spinner('Please wait.'):
    df = yf.download(tickers = tickers_list, period = "1y", interval = "1d")

# fetch prices & set date to datetime format
prices = df['Close']
prices.index = pd.to_datetime(prices.index)

# calculate yearly returns
start_value = prices.iloc[0]
end_value = prices.iloc[-1]

pct_change = (end_value - start_value) / start_value * 100
pct_change = round(pct_change,2)
pct_change = pct_change.sort_values(ascending=False)

# create blank dataframe and insert yearly returns with LTP in it
df2 = pd.DataFrame()
df2['% / Rank'] = pct_change
df2['LTP'] = round(end_value,2)
df2['Qty'] = round(allocation/df2['LTP'])
df2 = df2.head(stocks)

# plot
st.subheader(f'List of Top {stocks} Stocks in Momentum Over Last 1 Year')
st.dataframe(df2,width=500,height=950)


# function to convert and download the uploaded data as a csv file
def convert_df(df):
    return df.to_csv().encode('utf-8')
    

file = convert_df(df2)
st.download_button('Download List in CSV',file,'data.csv')

# extra information
st.write('You can read about the stock universe at [NSE](https://www.nseindia.com/products-services/indices-broad-market)')

exp = {'Nifty 50':'1 - 50','Nifty Next 50':'51 - 100','Nifty 100':'1-100','Nifty 200':'1-200',
       'Nifty Midcap 50':'101 - 150','Nifty Midcap 100':'101 - 200','Nifty Midcap 150':'101 - 250',
       'Nifty Small Cap 50':'251 - 300','Nifty Small Cap 100':'251 - 350','Nifty Small Cap 250':'251 - 500',
       'Nifty Large Mid Cap 250':'1 - 250 (Nifty50 + Nifty Next 50 + Nifty Midcap 150)','Nifty Mid Small Cap 400':'101 - 500 (Nifty Midcap 150 + Nifty Small Cap 250)',
       'Nifty 500': '1 - 500','Nifty Microcap 250':'501 - 750'}

exp_df = pd.DataFrame(exp.items(),columns=['Index','Positioning'])
st.table(exp_df)

# contact me button

import streamlit.components.v1 as components

tw1, tw2 = st.columns(2)
with tw1:
    st.subheader('Follow me on Twitter')
    components.html('<a href="https://twitter.com/oyesindhi_?ref_src=twsrc%5Etfw" class="twitter-follow-button" data-size="large" data-show-count="false">Follow @oyesindhi_</a><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>')
with tw2:
    st.subheader('Share on Twitter')
    components.html('<a href="https://twitter.com/share?ref_src=twsrc%5Etfw" class="twitter-share-button" data-size="large" data-text="Checkout this Backtesting Analyzer by @oyesindhi_" data-url="https://momentum-screener.streamlit.app/"data-show-count="false">"Share on Twitter</a><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>')

#this is the css code to hide main menu button, stream logo at the bottom, top header colored ribbon
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
