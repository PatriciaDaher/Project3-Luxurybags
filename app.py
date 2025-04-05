from flask import Flask, jsonify, render_template, request
import sqlite3
import pandas as pd
import json
import plotly
import plotly.express as px
import altair as alt

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
        "Year",
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
    """).iloc[0]
    
    # Create default visualizations (when no filters are applied)
    brand_chart = create_brand_comparison()
    
    # Render the template with initial data
    return render_template('/index.html', 
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
        # Show all data for general stats
        filtered_df = query_db("SELECT * FROM ChristiesHK_Mar25")
    elif filter_type == "Brand":
        # Get all brands data
        filtered_df = query_db("SELECT * FROM ChristiesHK_Mar25 ORDER BY Brand")
    elif filter_type == "Color":
        # Get all colors data
        filtered_df = query_db("SELECT * FROM ChristiesHK_Mar25 ORDER BY Color")
    elif filter_type == "Leather Type":
        # Get all leather types data
        filtered_df = query_db("SELECT * FROM ChristiesHK_Mar25 ORDER BY Leather")
    elif filter_type == "Year":
        # Get all years data
        filtered_df = query_db("SELECT * FROM ChristiesHK_Mar25 ORDER BY Year")
    else:
        # Default to general stats
        filtered_df = query_db("SELECT * FROM ChristiesHK_Mar25")
    
    # Generate new visualizations based on filtered data
    brand_chart = create_brand_comparison(filtered_df)
    
    # Get price stats for the filtered data
    if len(filtered_df) > 0:
        avg_price = filtered_df['[Price Realized (USD)]'].mean()
        max_price = filtered_df['[Price Realized (USD)]'].max()
        lower_estimate = filtered_df['[Lower Estimate (USD)'].max()
        higher_estimate = filtered_df['[Higher Estimate (USD)'].max()
    else:
        avg_price = 0
        max_price = 0
        lower_estimate = 0
        higher_estimate = 0
            
    # Return the JSON data with all charts
    return jsonify({
        'brand_chart': brand_chart,
        'stats': {
            'total_items': len(filtered_df),
            'avg_price': float(avg_price),
            'max_price': float(max_price),
            'lower_estimate': float(lower_estimate),
            'higher_estimate': float(higher_estimate)
        }
    })

# Helper function to create brand comparison visualization
def create_brand_comparison(df=None):
    if df is None:
        # If no DataFrame provided, query the database
        df = query_db("""
            SELECT Brand, AVG([Price Realized (USD)]) as Avg_Price
            FROM ChristiesHK_Mar25
            GROUP BY Brand
            ORDER BY Avg_Price DESC
        """)
    else:
        # Otherwise use the provided DataFrame
        df = df.groupby('Brand')['[Price Realized (USD)]'].mean().reset_index().rename(
            columns={'[Price Realized (USD)]': 'Avg_Price'}).sort_values('Avg_Price', ascending=False)
    
    # Create a bar chart using Altair
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('Brand:N', sort='-y'),
        y=alt.Y('Avg_Price:Q', title='Average Price (USD)'),
        color=alt.Color('Brand:N', legend=None),
        tooltip=['Brand', alt.Tooltip('Avg_Price:Q', format='$,.2f')]
    ).properties(
        title='Average Price by Brand',
        width='container',
        height=300
    ).interactive()
    
    return chart.to_json()

# API endpoint to get top performing bags
@app.route('/api/top_bags')
def get_top_bags():
    df = query_db("""
        SELECT Brand, Description, Leather, Color, [Price Realized (USD)] 
        FROM ChristiesHK_Mar25
        ORDER BY [Price Realized (USD)] DESC
        LIMIT 10
    """)
    
    return jsonify(df.to_dict(orient='records'))

# API endpoint to get database statistics
@app.route('/api/stats')
def get_stats():
    try:
        stats_df = query_db("""
            SELECT 
                COUNT(*) as total_items,
                COUNT(DISTINCT Brand) as brand_count,
                COUNT(DISTINCT Color) as color_count,
                COUNT(DISTINCT Leather) as leather_count,
                AVG([Price Realized (USD)]) as avg_price,
                MAX([Price Realized (USD)]) as max_price,
                MIN([Price Realized (USD)]) as min_price
            FROM ChristiesHK_Mar25
        """)
        
        if stats_df is not None and not stats_df.empty:
            stats = stats_df.iloc[0].to_dict()
            return jsonify(stats)
        else:
            return jsonify({"error": "No data found"}), 404
                
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)