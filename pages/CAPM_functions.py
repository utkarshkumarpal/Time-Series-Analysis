import plotly.express as px
import numpy as np

#function to plot intercative plotly chart
def  interactive_plot(df):
    fig=px.line()
    for i in df.columns[1:]:
        fig.add_scatter(x=df['Date'],y=df[i],name=i)
    fig.update_layout(width=500,margin=dict(l=20,r=20,t=50,b=20),legend=dict(orientation='h',yanchor='bottom',y=1.02,xanchor='right',x=1))
    return fig

# function to normalize the prices
def normalise(df):
    df_copy=df.copy()
    for i in df_copy.columns[1:]:
        df_copy[i]=df_copy[i]/df_copy[i][0]
    return df_copy


# function to get the daily returns
def daily_return(df):
    df_return=df.copy()
    for i in df_return.columns[1:]:
        for j in range(1,len(df_return)):
            df_return[i][j]=((df[i][j]-df[i][j-1])/df[i][j-1])*100
        df_return[i][0]=0
    return df_return


#function to calculate beta
def calclulate_beta(stock_return_daily,stock):
    rm=stock_return_daily['sp500'].mean()*252
    b,a = np.polyfit(stock_return_daily['sp500'],stock_return_daily[stock],1)
    return b,a