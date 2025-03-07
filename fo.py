import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("Sample - Superstore.csv", encoding='latin1')
    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("Filters")
categories = st.sidebar.multiselect("Select Category", df['Category'].unique(), default=df['Category'].unique())
regions = st.sidebar.multiselect("Select Region", df['Region'].unique(), default=df['Region'].unique())

df_filtered = df[(df['Category'].isin(categories)) & (df['Region'].isin(regions))]

# Dashboard Title
st.title("Sales and Profit Dashboard")

# KPI Metrics
total_sales = df_filtered['Sales'].sum()
total_profit = df_filtered['Profit'].sum()
col1, col2 = st.columns(2)
col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}")

# Sales by Category
fig_category = px.bar(df_filtered, x='Category', y='Sales', title='Sales by Category', color='Category')
st.plotly_chart(fig_category)

# Profit by Region
fig_region = px.bar(df_filtered, x='Region', y='Profit', title='Profit by Region', color='Region')
st.plotly_chart(fig_region)

# Sales vs. Profit Scatter Plot
fig_scatter = px.scatter(df_filtered, x='Sales', y='Profit', color='Category', title='Sales vs Profit')
st.plotly_chart(fig_scatter)

# Show Data
st.subheader("Filtered Data")
st.dataframe(df_filtered)
