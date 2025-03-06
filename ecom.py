import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go  # ✅ Import for Bar Charts

from plotly.colors import qualitative  # ✅ Import color palette

# Set Streamlit page configuration
st.set_page_config(page_title="E-commerce")
st.header("E-Commerce Dashboard")

# Load dataframe
csv_file = r'Sample - Superstore.csv'
df = pd.read_csv(csv_file, encoding='latin1')

# Convert 'Order Date' column to datetime
df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')

# Extract date-related information
df['Order Month'] = df['Order Date'].dt.month
df['Order Year'] = df['Order Date'].dt.year
df['Order Day of Week'] = df['Order Date'].dt.dayofweek

# Display dataframe in Streamlit
st.dataframe(df)

## **1. Monthly Sales Analysis**
sales_by_month = df.groupby('Order Month')['Sales'].sum().reset_index()

fig = px.line(
    sales_by_month,
    x='Order Month',
    y='Sales',
    title='Monthly Sales Analysis'
)

st.plotly_chart(fig)

## **2. Sales by Category (Pie Chart)**
sales_by_category = df.groupby('Category')['Sales'].sum().reset_index()
st.dataframe(sales_by_category)

fig = px.pie(
    sales_by_category,
    values='Sales',
    names='Category',
    hole=0.5,
    color_discrete_sequence=px.colors.qualitative.Pastel
)
fig.update_traces(textposition='inside', textinfo='percent+label')
fig.update_layout(title_text='Sales Analysis by Category', title_font=dict(size=24))

st.plotly_chart(fig)

## **3. Sales by Sub-Category (Bar Chart)**
sales_by_subcategory = df.groupby('Sub-Category')['Sales'].sum().reset_index()
st.dataframe(sales_by_subcategory)

fig = px.bar(
    sales_by_subcategory,
    x='Sub-Category',
    y='Sales',
    title='Sales by Sub-Category',
    color_discrete_sequence=px.colors.qualitative.Pastel
)

st.plotly_chart(fig)

## **4. Sales & Profit by Segment (Bar Chart)**
sales_profit_by_segment = df.groupby('Segment').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
st.dataframe(sales_profit_by_segment)

color_palette = qualitative.Pastel  # ✅ Corrected color palette import

fig = go.Figure()
fig.add_trace(go.Bar(
    x=sales_profit_by_segment['Segment'],
    y=sales_profit_by_segment['Sales'],
    name='Sales',
    marker_color=color_palette[0]
))
fig.add_trace(go.Bar(
    x=sales_profit_by_segment['Segment'],
    y=sales_profit_by_segment['Profit'],
    name='Profit',
    marker_color=color_palette[1]
))

fig.update_layout(
    title="Sales and Profit Analysis by Customer Segment",
    xaxis_title="Customer Segment",
    yaxis_title="Amount",
    barmode='group'
)

st.plotly_chart(fig)

sales_profit_by_segment = df.groupby('Segment').agg({'Sales':'sum','Profit':'sum'}).reset_index()
sales_profit_by_segment['Sales_to_profit_Ratio']=sales_profit_by_segment['Sales']/sales_profit_by_segment['Profit']
st.dataframe((sales_profit_by_segment[['Segment','Sales_to_profit_Ratio']]))