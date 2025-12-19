import streamlit as st

st.set_page_config(
    page_title="Trading App",
    page_icon="📈",
    layout="wide"
)


st.title('Top Stocks Analysis :bar_chart:')

st.header("All the prior information regarding the stocks at one place.")

st.image("img3.jpg")

st.markdown("### Following are the features available on this web app:")

st.markdown("#### 1. Stock Information")
st.write("This page basically contains all the essential information regarding the stock.")

st.markdown("#### 2.Stock  Prediction")
st.write("This page will absically predict the stock prices for the next 30 days.")

st.markdown("#### 3.CAPM Return")
st.write("This page gives the information regarding the preiviously returns from those stocks.")

st.markdown("#### 4.CAPM Beta")
st.write("This page will let you know the alpha and beta value of the stock, giving the idea about the market.")