# Imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load dataset
df = pd.read_csv(r"Imports_Exports_Dataset (1).csv")

# Sample the dataset
df_sample = df.sample(n=3001, random_state=55006)

# Sidebar for filters
st.sidebar.title("Filters")

# Filter by Import or Export
import_export_filter = st.sidebar.selectbox("Select Transaction Type", options=["All", "Import", "Export"])
if import_export_filter != "All":
    df_sample = df_sample[df_sample['Import_Export'] == import_export_filter]

# Filter by Shipping Method
shipping_method_filter = st.sidebar.selectbox("Select Shipping Method", options=["All"] + df_sample['Shipping_Method'].unique().tolist())
if shipping_method_filter != "All":
    df_sample = df_sample[df_sample['Shipping_Method'] == shipping_method_filter]

# Title for the dashboard
st.title('Dashboard for Imports and Exports')

# First row: Pie chart and Line chart side by side
st.subheader('Overview of Imports and Exports')

col1, col2 = st.columns(2)

# Pie Chart for Import/Export Distribution
with col1:
    st.subheader('Distribution of Import vs Export')
    import_export_count = df_sample['Import_Export'].value_counts()
    fig1, ax1 = plt.subplots(figsize=(7, 7))
    import_export_count.plot(kind='pie', autopct='%1.1f%%', startangle=90, ax=ax1)
    ax1.set_ylabel('')  # Removes the default y-label
    st.pyplot(fig1)

# Line Chart for Average Value of Transactions by Month
with col2:
    st.subheader('Average Value of Transactions by Month')
    df_sample['Date'] = pd.to_datetime(df_sample['Date'], format='%d-%m-%Y')
    df_sample['Month'] = df_sample['Date'].dt.month
    monthly_avg_value = df_sample.groupby(['Month', 'Import_Export'])['Value'].mean().unstack()
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    for column in monthly_avg_value.columns:
        ax2.plot(monthly_avg_value.index, monthly_avg_value[column], marker='o', label=column)
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Average Transaction Value')
    ax2.grid(True)
    ax2.legend(title='Transaction Type')
    st.pyplot(fig2)

# Second row: Box plot spanning the entire width
st.subheader('Detailed Distribution')

# Box Plot for Transaction Value by Category
st.subheader('Distribution of Transaction Value by Category')
fig3, ax3 = plt.subplots(figsize=(10, 6))
sns.boxplot(x='Category', y='Value', data=df_sample, ax=ax3, palette="Set3")  # Changed color palette
ax3.set_xticklabels(ax3.get_xticklabels(), rotation=45)
st.pyplot(fig3)

# Third row: Bar Plot for Shipping Method and Correlation Heatmap
col3, col4 = st.columns(2)

with col3:
    st.subheader('Quantity of Products by Shipping Method')
    shipping_quantity = df_sample.groupby("Shipping_Method")["Quantity"].sum()
    fig4, ax4 = plt.subplots(figsize=(10, 6))
    colors = sns.color_palette("hsv", len(shipping_quantity))  # Add different colors for each bar
    ax4.bar(x=shipping_quantity.index, height=shipping_quantity.values, color=colors)
    ax4.set_xlabel('Shipping Method')
    ax4.set_ylabel('Quantity')
    ax4.set_xticklabels(shipping_quantity.index, rotation=45)
    st.pyplot(fig4)

with col4:
    st.subheader('Correlation Between Quantity, Value, and Weight')
    corr = df_sample[['Quantity', 'Value', 'Weight']].corr()
    fig5, ax5 = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax5)
    st.pyplot(fig5)
