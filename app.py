import streamlit as st
import yfinance as yf
from app_functions import program_action, validate_ticker

def app():
    st.title("Financial Statement Analysis")

    # Sidebar input for stock ticker
    st.sidebar.header("Input Options")
    ticker = st.sidebar.text_input("Enter the company's stock ticker:", "").upper()

    if ticker:
        stock = yf.Ticker(ticker)
        valid_ticker, company_name = validate_ticker(stock)

        if valid_ticker:
            st.write(f'Company: {company_name}')
            program_action(stock)
