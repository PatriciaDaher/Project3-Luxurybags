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
    # Get list of brands for the dropdown filter
    brands = query_db("SELECT DISTINCT Brand FROM ChristiesHK_Mar25 ORDER BY Brand")['Brand'].tolist()
    brands.insert(0, "All Brands")  # Add "All Brands" option
    
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
    color_chart = create_color_comparison()
    year_chart = create_year_trend()
    leather_chart = create_leather_comparison()
    
    # Render the template with initial data
    return render_template('/index.html', 
                          brands=brands,
                          brand_chart=brand_chart,
                          color_chart=color_chart,
                          year_chart=year_chart,
                          leather_chart=leather_chart,
                          stats=price_stats)

# API endpoint to filter data based on user selection
@app.route('/api/filter_data')
def filter_data():
    # Get filter parameters from the request
    brand = request.args.get('brand', 'All Brands')
    
    # Build the base query
    base_query = "SELECT * FROM ChristiesHK_Mar25"
    conditions = []
    params = []
    
    # Add filter conditions if selected
    if brand != "All Brands":
        conditions.append("Brand = ?")
        params.append(brand)
    
    # Combine conditions if any
    if conditions:
        base_query += " WHERE " + " AND ".join(conditions)
    
    # Execute the query
    filtered_df = query_db(base_query, params)
    
    # Generate new visualizations based on filtered data
    brand_chart = create_brand_comparison(filtered_df)
    color_chart = create_color_comparison(filtered_df)
    year_chart = create_year_trend(filtered_df)
    leather_chart = create_leather_comparison(filtered_df)
    
    # Get price stats for the filtered data
    if len(filtered_df) > 0:
        avg_price = filtered_df['[Price Realized (USD)]'].mean()
        max_price = filtered_df['[Price Realized (USD)]'].max()
        lower_estimate = filtered_df['[Lower Estimate (USD)'].max()
        higher_estimate = filtered_df['[Higher Estimate (USD)'].max()  # Using max() to get the highest estimate
    else:
        avg_price = 0
        max_price = 0
        lower_estimate = 0
        higher_estimate = 0

            
    
    # Return the JSON data with all charts
    return jsonify({
        'brand_chart': brand_chart,
        'color_chart': color_chart,
        'year_chart': year_chart,
        'leather_chart': leather_chart,
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
    
    # Create a bar chart using Altair (the non-standard library)
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

# Helper function to create color comparison visualization
def create_color_comparison(df=None):
    if df is None:
        # If no DataFrame provided, query the database
        df = query_db("""
            SELECT Color, AVG([Price Realized (USD)]) as Avg_Price
            FROM ChristiesHK_Mar25
            GROUP BY Color
            ORDER BY Avg_Price DESC
        """)
    else:
        # Otherwise use the provided DataFrame
        df = df.groupby('Color')['[Price Realized (USD)]'].mean().reset_index().rename(
            columns={'[Price Realized (USD)]': 'Avg_Price'}).sort_values('Avg_Price', ascending=False)
    
    # Create visualization with Plotly
    fig = px.bar(df, x='Color', y='Avg_Price', 
                title='Average Price by Color',
                labels={'Avg_Price': 'Average Price (USD)', 'Color': 'Color'},
                color='Color')
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

# Helper function to create year trend visualization
def create_year_trend(df=None):
    if df is None:
        # If no DataFrame provided, query the database
        df = query_db("""
            SELECT Year, AVG([Price Realized (USD)]) as Avg_Price
            FROM ChristiesHK_Mar25
            GROUP BY Year
            ORDER BY Year
        """)
    else:
        # Otherwise use the provided DataFrame
        if 'Year' in df.columns:
            df = df.groupby('Year')['[Price Realized (USD)]'].mean().reset_index().rename(
                columns={'[Price Realized (USD)]': 'Avg_Price'}).sort_values('Year')
        else:
            # If no Year column, use a dummy DataFrame
            df = pd.DataFrame({'Year': ['No Year Data'], 'Avg_Price': [0]})
    
    # Create visualization with Plotly
    fig = px.line(df, x='Year', y='Avg_Price', 
                 title='Price Trends Over Years',
                 labels={'Avg_Price': 'Average Price (USD)', 'Year': 'Year'},
                 markers=True)
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

# Helper function to create leather comparison visualization
def create_leather_comparison(df=None):
    if df is None:
        # If no DataFrame provided, query the database
        df = query_db("""
            SELECT Leather, AVG([Price Realized (USD)]) as Avg_Price
            FROM ChristiesHK_Mar25
            GROUP BY Leather
            ORDER BY Avg_Price DESC
            LIMIT 10
        """)
    else:
        # Otherwise use the provided DataFrame
        df = df.groupby('Leather')['[Price Realized (USD)]'].mean().reset_index().rename(
            columns={'[Price Realized (USD)]': 'Avg_Price'}).sort_values('Avg_Price', ascending=False).head(10)
    
    # Create visualization with Plotly
    fig = px.bar(df, x='Leather', y='Avg_Price', 
                title='Top 10 Leathers by Average Price',
                labels={'Avg_Price': 'Average Price (USD)', 'Leather': 'Leather Type'},
                color='Leather')
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

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
# Add this to your Flask app temporarily for debugging
@app.route('/debug')
def debug():
    df = query_db("SELECT * FROM ChristiesHK_Mar25 LIMIT 5")
    return jsonify({
        'column_types': {col: str(df[col].dtype) for col in df.columns},
        'estimate_sample': df['Estimate (USD)'].tolist()
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)