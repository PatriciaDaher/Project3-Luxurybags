from flask import Flask, jsonify, render_template, request
# Uploading Libraries
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import altair as alt
import sqlite3

app = Flask(__name__)

# Database connection function
def connect_db():
    conn = sqlite3.connect('Luxury_handbag_auctions.sqlite')
    conn.row_factory = sqlite3.Row
    return conn

# Helper function to create a DataFrame from SQL query
def query_db(query, params=()):
    conn = connect_db()
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

# Home route that renders our main HTML template
@app.route('/')
def home():
    # Create filter options for the dropdown menu
    filter_options = [
        "General Stats",
        "Year",  # Fixed from "VYear"
        "Brand",
        "Color",
        "Leather Type"
    ]
    
    # Get price stats for the dashboard header
    price_stats = query_db("""
        SELECT 
            COUNT(*) as total_items,
            AVG([Price Realized (USD)]) as avg_price, 
            MAX([Price Realized (USD)]) as max_price,
            MAX([Lower Estimate (USD)]) as lower_estimate,
            MAX([Higher Estimate (USD)]) as higher_estimate
        FROM ChristiesHK_Mar25
    """).iloc[0].to_dict()  # Convert to dictionary
    
    # Create default visualizations (when no filters are applied)
    brand_chart = create_brand_comparison()
    
    # Render the template with initial data
    return render_template('index.html', 
                        filter_options=filter_options,
                        brand_chart=brand_chart,
                        stats=price_stats)

# API endpoint to filter data based on user selection
@app.route('/api/filter_data')
def filter_data():
    # Get filter parameters from the request
    filter_type = request.args.get('filter_type', 'General Stats')
    
    # Build the base query based on filter type
    if filter_type == "General Stats":
        filtered_df = query_db("SELECT * FROM ChristiesHK_Mar25")
    elif filter_type == "Brand":
        filtered_df = query_db("SELECT * FROM ChristiesHK_Mar25 ORDER BY Brand")
    elif filter_type == "Color":
        filtered_df = query_db("SELECT * FROM ChristiesHK_Mar25 ORDER BY Color")
    elif filter_type == "Leather Type":
        filtered_df = query_db("SELECT * FROM ChristiesHK_Mar25 ORDER BY Leather")
    elif filter_type == "Year":
        filtered_df = query_db("SELECT * FROM ChristiesHK_Mar25 ORDER BY Year")
    else:
        filtered_df = query_db("SELECT * FROM ChristiesHK_Mar25")
    
    # Generate new visualizations based on filtered data
    brand_chart = create_brand_comparison(filtered_df)
    
    # Calculate statistics
    stats = {
        'total_items': len(filtered_df),
        'avg_price': 0,
        'max_price': 0,
        'lower_estimate': 0,
        'higher_estimate': 0
    }
    
    if len(filtered_df) > 0:
        try:
            stats['avg_price'] = float(filtered_df['[Price Realized (USD)]'].mean())
            stats['max_price'] = float(filtered_df['[Price Realized (USD)]'].max())
            stats['lower_estimate'] = float(filtered_df['[Lower Estimate (USD)]'].max())
            stats['higher_estimate'] = float(filtered_df['[Higher Estimate (USD)]'].max())
        except KeyError as e:
            app.logger.error(f"Missing column in data: {e}")
    
    return jsonify({
        'brand_chart': brand_chart,
        'stats': stats
    })

# Helper function to create brand comparison visualization
def create_brand_comparison(df=None):
    if df is None:
        # Query the database if no DataFrame provided
        df = query_db("""
            SELECT Brand, AVG([Price Realized (USD)]) as Avg_Price
            FROM ChristiesHK_Mar25
            GROUP BY Brand
            ORDER BY Avg_Price DESC
        """)
    else:
        # Process the provided DataFrame
        df = df.groupby('Brand')['[Price Realized (USD)]'].mean().reset_index().rename(
            columns={'[Price Realized (USD)]': 'Avg_Price'}).sort_values('Avg_Price', ascending=False)
    
    # Create interactive bar chart using Altair
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('Brand:N', sort='-y', title='Brand'),
        y=alt.Y('Avg_Price:Q', title='Average Price (USD)'),
        color=alt.Color('Brand:N', legend=None),
        tooltip=['Brand', alt.Tooltip('Avg_Price:Q', format='$,.2f')]
    ).properties(
        title='Average Price by Brand',
        width='container',
        height=400
    ).interactive()
    
    return chart.to_json()

if __name__ == '__main__':
    app.run(debug=True, port=5001)