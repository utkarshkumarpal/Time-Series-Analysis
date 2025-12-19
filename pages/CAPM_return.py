# importing libraries

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import datetime
import pandas as pd
import yfinance as yf
import pandas_datareader.data as web
import pages.CAPM_functions as CAPM_functions


st.set_page_config(
    page_title="CAPM",
    page_icon="chart_with_pwards_trend",
    layout='wide'
)

st.title("Capital Asset Pricing Model")

#getting input from user

col1,col2=st.columns([1,1])

with col1:
    stocks_list=st.multiselect("Choose any 4 stocks",('AMZN','GOOGL','MSFT','NFLX','NVDA','TSLA','APPL'),['AMZN','GOOGL','MSFT','NVDA'])

with col2:
    year=st.number_input("Number of years",1,15)

#downaloding data for sp500
try:
    end=datetime.date.today()
    start=datetime.date(datetime.date.today().year-year,datetime.date.today().month,datetime.date.today().day)
    SP500=web.DataReader(['sp500'],'fred',start,end)
    # print(SP500.head())


    stock_df=pd.DataFrame()


    for stock in stocks_list:
        data=yf.download(stock,period=f'{year}y')
        stock_df[f'{stock}']=data['Close']

    # print(stock_df.head())

    stock_df.reset_index(inplace=True)
    SP500.reset_index(inplace=True)
    # print(stock_df.dtypes)
    # print(SP500.dtypes)


    SP500=SP500.rename(columns={'DATE':'Date'})
    stock_df= pd.merge(stock_df,SP500,on='Date',how='inner')
    # print(stock_df)

    col1,col2=st.columns([1,1])
    with col1:
        st.markdown('### Dataframe Head')
        st.dataframe(stock_df.head(),use_container_width=True)
    with col2:
        st.markdown('### Dataframe Tail')
        st.dataframe(stock_df.tail(),use_container_width=True)


    col1,col2=st.columns([1,1])
    with col1:
        st.markdown('### Price of all the stocks')
        st.plotly_chart(CAPM_functions.interactive_plot(stock_df))

    with col2:
        # print(CAPM_functions.normalise(stock_df)) 
        st.markdown('### Price of all the stocks (After Normalising)')
        st.plotly_chart(CAPM_functions.interactive_plot((CAPM_functions.normalise(stock_df))))



    stock_return_daily=CAPM_functions.daily_return(stock_df)
    print(stock_return_daily.head())


    # beta and alpha
    beta={}
    alpha={}
    for i in stock_return_daily.columns:
        if i!='Date' and i !='sp500':
            b,a=CAPM_functions.calclulate_beta(stock_return_daily,i)
            beta[i]=b
            alpha[i]=a
    # print(beta,alpha)

    beta_df=pd.DataFrame(columns=['Stock','Beta_Value'])
    beta_df['Stock']=beta.keys()
    beta_df['Beta Value']=[str(round(i,2)) for i in beta.values()]

    with col1:
        st.markdown('### Calculated Beta Values')
        st.dataframe(beta_df,use_container_width=True)

    rf=0
    rm= stock_return_daily['sp500'].mean()*252

    return_df=pd.DataFrame()
    return_value=[]

    for stock,value in beta.items():
        return_value.append(str(round(rf+(value*(rm-rf)),2)))

    return_df['Stock']=stocks_list
    return_df['Return Value']=return_value

    with col2:
        st.markdown('### Calculated Return using CAPM')
        st.dataframe(return_df,use_container_width=True)

except:
    print.write("Please select valid Input")