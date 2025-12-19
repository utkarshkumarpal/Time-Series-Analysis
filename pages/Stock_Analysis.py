import streamlit as st
import yfinance as yf
import datetime
import pandas as pd
from pages.utils.plotly_figure import plotly_table,candlestick,RSI,close_chart,MACD, Moving_average
 

st.set_page_config(
    page_title='Stock Analysis',
    page_icon='📃',
    layout='wide'
)

st.title("Stock Analysis")

col1, col2, col3 = st.columns(3)

today = datetime.date.today()

with col1:
    ticker = st.text_input('Stock Ticker', 'AMZN')
with col2:
    startdate = st.date_input("Choose Start Date",
                              datetime.date(today.year - 1, today.month, today.day))
with col3:
    enddate = st.date_input("Choose End date",
                            datetime.date(today.year, today.month, today.day))

st.subheader(ticker)

stock = yf.Ticker(ticker)

st.write('**ABOUT:**', stock.info.get('longBusinessSummary', 'N/A'))
st.write('**Industry Sector:**', stock.info.get('sector', 'N/A'))
st.write('**Total Employees:**', stock.info.get('fullTimeEmployees', 'N/A'))
st.write('**Website link:**', stock.info.get('website', 'N/A'))

col1, col2 = st.columns(2)

with col1:
    df = pd.DataFrame({
        'Metric': ['Market Cap', 'Beta', 'EPS', 'PE Ratio'],
        'Value': [
            stock.info.get('marketCap'),
            stock.info.get('beta'),
            stock.info.get('trailingEps'),
            stock.info.get('trailingPE')
        ]
    })
    st.plotly_chart(plotly_table(df), use_container_width=True)

with col2:
    df = pd.DataFrame({
        'Metric': ['Quick Ratio', 'Revenue per Share',
                   'Profit Margin', 'Debt to Equity', 'Return on Equity'],
        'Value': [
            stock.info.get('quickRatio'),
            stock.info.get('revenuePerShare'),
            stock.info.get('profitMargins'),
            stock.info.get('debtToEquity'),
            stock.info.get('returnOnEquity')
        ]
    })
    st.plotly_chart(plotly_table(df), use_container_width=True)

# st.write(stock.info.keys())   to check the yahoo sent the data or not
data=yf.download(ticker,start=startdate,end=enddate)
col1,col2,col3=st.columns([1,1,1]) 
# daily_change=data['Close'].iloc[-1]-data['Close'].iloc[-2]
latest_close = data['Close'].iloc[-1]
prev_close = data['Close'].iloc[-2]
daily_change = latest_close - prev_close
daily_pct_change = (daily_change / prev_close) * 100
col1.metric(
    "Daily Change",
    f"{data['Close'].iloc[-1].item():.2f}",
    f"{daily_change.item():.2f}"
)


last_10_df=data.tail(10).sort_index(ascending=False).round(3)
fig_df=plotly_table(last_10_df)

st.write('#### Last 10 days data')
st.plotly_chart(fig_df,use_container_width=True)


col1,col2,col3,col4,col5,col6,col7,col8,col9,col10,col11,col12=st.columns([1,1,1,1,1,1,1,1,1,1,1,1])


num_period=''

with col1:
    if st.button('5d'):
        num_period='5d'
with col2:
    if st.button('1M'):
        num_period='1mo'
with col3:
    if st.button('6M'):
        num_period='6mo'
with col4:
    if st.button('YTD'):
        num_period='ytd'
with col5:
    if st.button('1Y'):
        num_period='1y'
with col6:
    if st.button('5Y'):
        num_period='5y'
with col7:
    if st.button('MAX'):
        num_period='max'        


col1,col2,col3=st.columns([1,1,4])
with col1:
    chart_type=st.selectbox('',('Candle','Line'))
with col2:
    if chart_type=='Candle':
        indicators=st.selectbox('',('RSI','MACD'))
    else:
        indicators=st.selectbox('',('RSI','Moving Average','MACD'))


ticker_=yf.Ticker(ticker)
newdf=ticker_.history(period='max')
data1=ticker_.history(period='max')

if num_period=='':
    
    if chart_type=='Candle' and indicators=='RSI':
        st.plotly_chart(candlestick(data1,'1y'),use_container_width=True)
        st.plotly_chart(RSI(data1,'1y'),use_container_width=True)
    if chart_type=='Candle' and indicators=='MACD':
        st.plotly_chart(candlestick(data1,'1y'),use_container_width=True)
        st.plotly_chart(MACD(data1,'1y'),use_container_width=True)
    if chart_type=='Line' and indicators=='RSI':
        st.plotly_chart(close_chart(data1,'1y'),use_container_width=True)
        st.plotly_chart(RSI(data1,'1y'),use_container_width=True)
    if chart_type=='Line' and indicators=='MACD':
        st.plotly_chart(close_chart(data1,'1y'),use_container_width=True)
        st.plotly_chart(MACD(data1,'1y'),use_container_width=True)
    if chart_type=='Line' and indicators=='Moving Average':
        st.plotly_chart(Moving_average(data1,'1y'),use_container_width=True)

else:
    if chart_type=='Candle' and indicators=='RSI':
        st.plotly_chart(candlestick(newdf,num_period),use_container_width=True)
        st.plotly_chart(RSI(newdf,num_period),use_container_width=True)
    if chart_type=='Candle' and indicators=='MACD':
        st.plotly_chart(candlestick(newdf,num_period),use_container_width=True)
        st.plotly_chart(MACD(newdf,num_period),use_container_width=True)
    if chart_type=='Line' and indicators=='RSI':
        st.plotly_chart(close_chart(newdf,num_period),use_container_width=True)
        st.plotly_chart(RSI(newdf,num_period),use_container_width=True)
    if chart_type=='Line' and indicators=='MACD':
        st.plotly_chart(close_chart(newdf,num_period),use_container_width=True)
        st.plotly_chart(MACD(newdf,num_period),use_container_width=True)
    if chart_type=='Line' and indicators=='Moving Average':
        st.plotly_chart(Moving_average(newdf,num_period),use_container_width=True)


