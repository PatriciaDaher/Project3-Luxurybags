# Project3-Luxurybags
# Luxury Handbag Market Analysis

## Project Overview
This project analyzes auction data from Christie's Hong Kong March 2025 luxury handbag sale to identify factors influencing handbag values in the secondary market. We examine how brand, color, leather type, and rarity impact auction prices, creating an interactive dashboard that allows users to explore these relationships.

The analysis reveals key insights for collectors, investors, and industry professionals about what drives value in the luxury handbag market, with a particular focus on Hermès, Louis Vuitton, and Chanel bags.

## How to Use and Interact with the Project

### Setup and Installation
1. Clone this repository to your local machine
2. Install the required packages:
   ```
   pip install flask pandas sqlite3 plotly altair
   ```
3. Run the Flask application:
   ```
   python app.py
   ```
4. Open your web browser and navigate to `http://127.0.0.1:5001`

### Interactive Features
- **Filter Data**: Use the dropdown menus at the top of the dashboard to filter by brand and/or color
- **Apply Filters**: Click the "Apply Filters" button to update all visualizations based on your selections
- **Interactive Charts**: Hover over chart elements to see detailed tooltips with exact values
- **Responsive Design**: The dashboard adapts to different screen sizes for optimal viewing

## Database
We've used SQLite for this project for several reasons:
- **Lightweight**: SQLite requires minimal setup and runs without a separate server process
- **Portability**: The entire database is stored in a single file, making it easy to share and back up
- **Simplicity**: For our dataset size (247 records), SQLite provides excellent performance without unnecessary complexity

The database contains auction data with information about lot number, brand, type, color, leather, hardware, year manufactured, estimates, and realized prices.

## Data Collection and Transformation
1. **Data Sources**: Auction records were scraped from Christie's website for their Hong Kong March 2025 sale
2. **Key Metrics**: 247 unique records listing Hermès, Louis Vuitton, and Chanel bags
3. **Data Cleaning**: Used Python and Pandas to:
   - Convert currencies to USD
   - Split price estimate ranges into lower and higher bounds
   - Create a price category classifying sales as below, within, or above estimate
4. **Database Creation**: Stored the cleaned DataFrame in a SQLite database

## Ethical Considerations
Our project raises several ethical considerations related to luxury goods and data usage:

1. **Environmental Impact**: Many of the highest-priced bags in our analysis use exotic leathers from alligators and crocodiles. While we present this data objectively, we acknowledge the environmental and animal welfare concerns associated with these materials. Sustainable alternatives are increasingly important in the luxury market.

2. **Data Privacy**: Although we used publicly available auction data, we've been careful to present aggregate statistics rather than individual transaction details that might compromise bidder privacy.

3. **Wealth Inequality**: The luxury handbag market represents significant wealth concentration. Our analysis shows bags selling for up to $274,600—more than many people's annual incomes. We present this information for educational purposes while acknowledging the broader socioeconomic context.

4. **Cultural Considerations**: Luxury consumption varies across cultures, and our analysis of Hong Kong auction data may reflect regional preferences not representative of global trends. We've attempted to avoid cultural generalizations in our analysis.

We believe that transparent data analysis can help consumers and industry professionals make more informed decisions while being mindful of these ethical considerations.

## Key Insights
- Hermès bags consistently achieve the highest auction prices, especially limited edition and exotic leather designs
- Exotic leathers like alligator and crocodile command significantly higher prices compared to standard leather options
- White, multicolor, and turquoise bags achieve the highest average prices, while silver and yellow are the lowest-performing colors
- Recent years, especially 2021 and beyond, saw an increase in luxury handbag prices, reflecting strong demand
- Most bags sell within or above their estimated price range, showcasing a robust secondary market for luxury handbags

## Technologies Used
- **Database**: SQLite
- **Backend**: Flask, Python, Pandas
- **Visualization**: Plotly, Altair (new library not covered in class)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap

## Data Sources
- Christie's Auction House: [Christie's Website](https://www.christies.com/en/results)
- Auction data specifically from Christie's Hong Kong March 2025 Handbags Online sale

## Project Contributors
- Sade Beckles
- Patricia Daher
- Arisleyda Reyes

## References
- Christie's auction results: https://www.christies.com/en/results
- Sotheby's luxury handbag data (for comparison): https://www.sothebys.com/en/search?locale=en&query=hermès&tab=objects&sortBy=bsp_dotcom_prod_en
- Christie's Hong Kong press releases: https://press.christies.com/christies-hong-kong-presents