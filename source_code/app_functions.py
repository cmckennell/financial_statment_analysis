import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Function to validate the stock ticker
def validate_ticker(stock):
    try:
        company_name = stock.info["shortName"]
        return True, company_name
    except KeyError:
        st.write("Invalid Stock Ticker. No company found.")
        return False, None

# Placeholder to clear main display when switching between actions
def program_action(stock):
    # Create a placeholder that will be cleared and updated
    placeholder = st.empty()
    
    actions = {'Analyze Performance': analyze_performance, 'View Financial Statements': view_financial_statements}
    action = st.sidebar.selectbox('What would you like to do?:', actions.keys())
    
    if action:
        # Clear the placeholder content first
        placeholder.empty()
        
        # Execute the selected action within the placeholder
        with placeholder:
            actions[action](stock)

def analyze_performance(stock):
    st.write("Analyzing key financial performance ratios...")

    # Fetch the financial data and reset index to access data easily
    income_statement = stock.financials.reset_index()  # Reset the index to make the financial metrics regular columns
    balance_sheet = stock.balance_sheet.reset_index()
    cash_flow = stock.cashflow.reset_index()

    # Find the most recent column dynamically (it should always be the second column)
    most_recent_column = income_statement.columns[1]  # This gets the name of the second column (most recent data)

    # Access values from the financial statements
    revenue = income_statement.loc[income_statement['index'] == 'Total Revenue', most_recent_column].values[0]
    gross_profit = income_statement.loc[income_statement['index'] == 'Gross Profit', most_recent_column].values[0]
    net_income = income_statement.loc[income_statement['index'] == 'Net Income', most_recent_column].values[0]
    total_assets = balance_sheet.loc[balance_sheet['index'] == 'Total Assets', most_recent_column].values[0]
    total_equity = balance_sheet.loc[balance_sheet['index'] == 'Stockholders Equity', most_recent_column].values[0]
    total_liabilities = balance_sheet.loc[balance_sheet['index'] == 'Total Liabilities Net Minority Interest', most_recent_column].values[0]
    current_assets = balance_sheet.loc[balance_sheet['index'] == 'Current Assets', most_recent_column].values[0]
    current_liabilities = balance_sheet.loc[balance_sheet['index'] == 'Current Liabilities', most_recent_column].values[0]
    cash_flow_operations = cash_flow.loc[cash_flow['index'] == 'Operating Cash Flow', most_recent_column].values[0]
    interest_expense = income_statement.loc[income_statement['index'] == 'Interest Expense', most_recent_column].values[0]

    # Calculate financial ratios
    gross_profit_margin = (gross_profit / revenue) * 100
    net_profit_margin = (net_income / revenue) * 100
    return_on_assets = (net_income / total_assets) * 100
    return_on_equity = (net_income / total_equity) * 100
    current_ratio = current_assets / current_liabilities
    debt_to_equity_ratio = total_liabilities / total_equity
    interest_coverage_ratio = net_income / interest_expense

    # Create a DataFrame to display these ratios
    ratios = pd.DataFrame({
        "Metric": ["Gross Profit Margin (%)", "Net Profit Margin (%)", "Return on Assets (%)", 
                   "Return on Equity (%)", "Current Ratio", "Debt to Equity Ratio", "Interest Coverage Ratio"],
        "Value": [gross_profit_margin, net_profit_margin, return_on_assets, return_on_equity, 
                  current_ratio, debt_to_equity_ratio, interest_coverage_ratio]
    })

    # Display the ratios
    st.write("### Key Financial Ratios")
    st.dataframe(ratios)

    # Plot charts for some of the key ratios
    st.write("### Ratio Charts")

    # Plot the ratios in a bar chart
    fig, ax = plt.subplots()
    ax.bar(ratios["Metric"], ratios["Value"])
    plt.xticks(rotation=45, ha='right')
    plt.title('Key Financial Ratios')
    plt.tight_layout()

    # Display the chart in Streamlit
    st.pyplot(fig)

# Function to view financial statements
def view_financial_statements(stock):
    financials = {
        "Balance Sheet": stock.balance_sheet,
        "Income Statement": stock.financials,
        "Cash Flow Statement": stock.cashflow,
    }

    # Dropdown to select the financial statement document
    doc_type = st.sidebar.selectbox("Select a financial document to analyze:", financials.keys())
    
    if doc_type:
        st.write(f"Displaying {doc_type}")
        st.dataframe(financials[doc_type], width=2000, height=600)
