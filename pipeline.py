"""
Lab 2 — Data Pipeline: Retail Sales Analysis
Module 2 — Programming for AI & Data Science

Complete each function below. Remove the TODO: comments and pass statements
as you implement each function. Do not change the function signatures.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ─── Configuration ────────────────────────────────────────────────────────────

DATA_PATH = 'data/sales_records.csv'
OUTPUT_DIR = 'output'


# ─── Pipeline Functions ───────────────────────────────────────────────────────

def load_data(filepath):
    """Load sales records from a CSV file.

    Args:
        filepath (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Raw sales records DataFrame.
    """
    df = pd.read_csv(filepath)
    print(f"Loaded: {len(df)} records from {filepath}")
    return df
    pass


def clean_data(df):
    """Handle missing values and fix data types.

    - Fill missing 'quantity' values with the column median.
    - Fill missing 'unit_price' values with the column median.
    - Parse the 'date' column to datetime (use errors='coerce' to handle malformatted dates).
    - Print a progress message showing the record count after cleaning.

    Args:
        df (pd.DataFrame): Raw DataFrame from load_data().

    Returns:
        pd.DataFrame: Cleaned DataFrame (do not modify the input in place).
    """    
    df = df.copy()

    df['quantity']   = df['quantity'].fillna(df['quantity'].median())
    df['unit_price'] = df['unit_price'].fillna(df['unit_price'].median())

    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # Drop rows where BOTH quantity AND unit_price are still missing after fill
    df = df.dropna(subset=['quantity','unit_price'],how='all')       
    # Removal — use cautiously; drops data
    df = df.dropna(subset=['date'])
    print(f"cleaned Data: {len(df)} records")
    return df
    pass


def add_features(df):
    """Compute derived columns.

    - Add 'revenue' column: quantity * unit_price.
    - Add 'day_of_week' column: day name from the date column.

    Args:
        df (pd.DataFrame): Cleaned DataFrame from clean_data().

    Returns:
        pd.DataFrame: DataFrame with new columns added.
    """
    df = df.copy()
    df['revenue'] = df['quantity'] * df['unit_price']
    df['day_of_week'] = df['date'].dt.day_name()
    return df
    pass


def generate_summary(df):
    """Compute summary statistics.

    Args:
        df (pd.DataFrame): Enriched DataFrame from add_features().

    Returns:
        dict: Summary with keys:
            - 'total_revenue': total revenue (sum)
            - 'avg_order_value': average order value (mean)
            - 'top_category': product category with highest total revenue
            - 'record_count': number of records in df
    """
    total_revenue = round(df['revenue'].sum(),2)
    avg_order_value = round(df['revenue'].mean(),2)
    top_category = df.groupby('product_category')['revenue'].sum().idxmax()
    record_count = len(df)
    summary = {
        'total_revenue' : total_revenue,
        'avg_order_value': avg_order_value,
        'top_category': top_category,
        'record_count': record_count
    } 
    return summary
    pass


def create_visualizations(df, output_dir=OUTPUT_DIR):
    """Create and save 3 charts as PNG files.

    Charts to create:
    1. Bar chart: total revenue by product category
    2. Line chart: daily revenue trend (aggregate revenue by date)
    3. Horizontal bar chart: average order value by payment method

    Save each chart as a PNG using fig.savefig().
    Do NOT use plt.show() — it blocks execution in pipeline scripts.
    Close each figure with plt.close(fig) after saving.

    Args:
        df (pd.DataFrame): Enriched DataFrame from add_features().
        output_dir (str): Directory to save PNG files (create if needed).
    """
    os.makedirs(output_dir, exist_ok=True)

    #  Chart 1
    #   - Group by 'product_category', sum 'revenue'
    ctg_revenue = df.groupby('product_category')['revenue'].sum()
    categories = ctg_revenue.index
    values     = ctg_revenue.values
    #   - fig, ax = plt.subplots(figsize=(10, 6))
    fig, ax = plt.subplots(figsize=(10, 6))
    
    #   - ax.bar(categories, values) or use ax.barh() for horizontal
    ax.bar(categories, values, color='red', edgecolor='white')

    #   - Set title, labels
    ax.set_title('Total Revenue For category')
    ax.set_xlabel('Product Category')
    ax.set_ylabel('Total Revenue')

    ax.tick_params(axis='x', rotation=45) 
    ax.grid(True, axis='y', alpha=0.3)
    #   - fig.savefig(f'{output_dir}/revenue_by_category.png', dpi=150, bbox_inches='tight')
    fig.savefig(f'{output_dir}/revenue_by_category.png', dpi=150, bbox_inches='tight')

    #   - plt.close(fig)
    plt.close(fig)
   
    #  Chart 2
    #   - Group by 'date', sum 'revenue' — sort by date
    date_revenue = df.groupby('date')['revenue'].sum()
    dates = date_revenue.index
    revenues = date_revenue.values
    #   - ax.plot(dates, revenues)
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(dates , revenues, color='green')
    ax.set_title("Daily Revenue")
    ax.set_xlabel("Date")
    ax.set_ylabel("Revenue")
    ax.tick_params(axis='x', rotation=45) 
    ax.grid(True, axis='y', alpha=0.3)
    #   - fig.savefig(f'{output_dir}/daily_revenue_trend.png', dpi=150, bbox_inches='tight')
    fig.savefig(f'{output_dir}/daily_revenue_trend.png', dpi=150, bbox_inches='tight')
    #   - plt.close(fig)
    plt.close(fig)

    #  Chart 3 
    #   - Group by 'payment_method', mean 'revenue'
    avg_order = df.groupby('payment_method')['revenue'].mean()
    methods = avg_order.index
    avg_values = avg_order.values
    #   - ax.barh(methods, avg_values)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(methods, avg_values, color='blue')
    ax.set_title("Average Order Value by Payment Method")
    ax.set_xlabel("Average Revenue")
    ax.set_ylabel("Payment Method")
    ax.tick_params(axis='x', rotation=45) 
    ax.grid(True, axis='x', alpha=0.3)
    #   - fig.savefig(f'{output_dir}/avg_order_by_payment.png', ...)
    fig.savefig(f'{output_dir}/avg_order_by_payment.png', dpi=150, bbox_inches='tight')
    #   - plt.close(fig)
    plt.close(fig)

    pass



# Build Guard Function
def main():
    """Run the full data pipeline end-to-end."""
    # TODO: Call load_data(DATA_PATH)
    df = load_data(DATA_PATH)
    # TODO: Call clean_data(df)
    df = clean_data(df)
    # TODO: Call add_features(df)
    df = add_features(df)
    # TODO: Call generate_summary(df) and print the results
    summary = generate_summary(df)
    print("=== Summary ===")
    print(f"Total Revenue: {summary['total_revenue']}")
    print(f"Average Order Value: {summary['avg_order_value']}")
    print(f"Top Category: {summary['top_category']}")
    print(f"Record Count: {summary['record_count']}")
    # TODO: Call create_visualizations(df)
    create_visualizations(df)
    # TODO: Print "Pipeline complete."
    print("Pipeline complete.")
    pass


if __name__ == "__main__":
    main()
