import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="E-commerce Sales Dashboard", layout="wide")
st.title("E-commerce Sales Dashboard")

df = pd.read_csv("Amazon Sale Report.csv")
df['Date'] = pd.to_datetime(df['Date'])
df['Month'] = df['Date'].dt.to_period('M').astype(str)

# Sidebar filters
st.sidebar.header("Filters")
categories = st.sidebar.multiselect("Category", sorted(df['Category'].dropna().unique()), default=sorted(df['Category'].dropna().unique()))
fulfilment = st.sidebar.multiselect("Fulfilment", sorted(df['Fulfilment'].dropna().unique()), default=sorted(df['Fulfilment'].dropna().unique()))
df = df[df['Category'].isin(categories) & df['Fulfilment'].isin(fulfilment)]

# KPI cards
total_sales = df['Amount'].sum()
total_orders = df['Order ID'].nunique()
total_qty = df['Qty'].sum()
aov = total_sales / total_orders if total_orders else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Sales", f"{total_sales:,.0f}")
c2.metric("Total Orders", f"{total_orders:,}")
c3.metric("Total Qty", f"{total_qty:,}")
c4.metric("Avg Order Value", f"{aov:,.0f}")

# Row 1
col1, col2 = st.columns(2)
monthly = df.groupby('Month')['Amount'].sum().reset_index()
col1.plotly_chart(px.line(monthly, x='Month', y='Amount', markers=True, title='Monthly Sales Trend'), use_container_width=True)

cat = df.groupby('Category')['Amount'].sum().reset_index().sort_values('Amount', ascending=False)
col2.plotly_chart(px.bar(cat, x='Category', y='Amount', title='Sales by Category'), use_container_width=True)

# Row 2
col3, col4 = st.columns(2)
states = df.groupby('ship-state')['Amount'].sum().nlargest(10).reset_index()
col3.plotly_chart(px.bar(states, x='Amount', y='ship-state', orientation='h', title='Top 10 States by Sales'), use_container_width=True)

prods = df.groupby('SKU')['Amount'].sum().nlargest(10).reset_index()
col4.plotly_chart(px.bar(prods, x='Amount', y='SKU', orientation='h', title='Top 10 Products by Sales'), use_container_width=True)

# Row 3
col5, col6 = st.columns(2)
ful = df.groupby('Fulfilment')['Amount'].sum().reset_index()
col5.plotly_chart(px.pie(ful, names='Fulfilment', values='Amount', title='Sales by Fulfilment'), use_container_width=True)

status = df['Status'].value_counts().reset_index()
status.columns = ['Status', 'Count']
col6.plotly_chart(px.bar(status, x='Status', y='Count', title='Order Status'), use_container_width=True)