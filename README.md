# Project3-Luxurybags
# Luxury Handbag Market Analysis


## Project Overview
Christie’s Auction house, one of the two major international auction houses in the world, was established on December 5, 1766, by James Christie in London, England. Throughout the years this major auction house played a crucial role in facilitating the secondary market for high-end luxury sales. Handbag sales in particular, have been record-breaking, highlighting the desirability of rare and limited-edition pieces.
This project explores the factors influencing the value of luxury handbags. By analyzing Christie's Hong Kong March 2025 luxury handbag sale, we examine how attributes such as brand, color, leather type, and year of manufacture affect auction prices.
To visualize these relationships, we develop an interactive dashboard, providing insights into how rarity and other characteristics impact value.
Our analysis offers valuable insights for collectors, investors, and industry professionals, with a particular focus on handbags from Hermès, Louis Vuitton, and Chanel.


## Repository Contents
```
Luxury-handbag-visualization
|_ Index.html
|_ luxury_handbag_auctions.sqlite
|_ Christies Hong Kong March 2025 Cleaned .csv
|_ Cleaned_Enhanced_Luxury_Bag_Data.csv
|_ LuxuryBags.ipynb
Presentation projectf.DS_Store
README.md

```
## How to Use and Interact with the Project


### Setup and Installation
1- Clone the repository: https://github.com/sadebeckz/Project3-Luxurybags.git
Navigate to the project directory: cd project project name Project3-Luxurybags


2. Install the required packages:
   ```
   pip install python pandas matplotlib sqlite3 plotly altair
   ```
3. start the server by navigating to the directory, particularly the luxury-handbag-visualization folder, and in the folder, open using python's built-in server type the following:
   ```
   python3 -m http.server 8000
   ```
   (For Windows, if python3 doesn't work, try python or py instead.)

4. To `Access the server: Open your web browser and navigate 
Open a browser and go to any of these or the link provided:
http://localhost:8000 or http://127.0.0.1:8000

### Interactive Features
- **Visualize Data**: Use the dropdown menue to view Sales Analysis based on options such as Sale Results, Brand, Year, Color, and Leather type. 
- **Apply Filters**: Click the "Apply Filters" button to update all visualizations based on your selections.
- **Interactive Charts**: Hover over select chart elements to see detailed tooltips.


## Data Collection, Cleaning  and Transformation
1. **Data Sources**: Data Sources: Auction records were scraped from Christie's website, from their Hong Kong March 2025 sale titled “ Handbags Online: the Hong Kong Edit” into a csv.
2. **Data Cleaning and Transformation**: Used Word, Excel, Python and Pandas to create a clean csv:
   - Cleaned csv by removing irrelevant lots, converting currency from HKD to USD, and Splitting the Estimate column into Lower Estimate and Higher Estimate. ​
   - Created a price category classifying sales as passed, below, within, or above estimate
3. **Database Creation**: Stored the cleaned DataFrame in a SQLite database


## Database
The Sqlite database contains auction data with information about lots number, brand, type, color, leather, hardware, year manufactured, estimates, and realized prices.


## Visualizations & Interactions  (HTML Content)   

2- **Analysis Dropdown Menu displaying a total of 9 charts**
Visualizations 1: General Sale Performance
b- Bar Chart 1 Lot Sales Relative to Estimates
c- Bar Chart 2 Top 10 Most Expensive Handbags
Visualizations 2: General Sale Results by BRAND
	a- Bar Chart 1: Total Sales By Brand 
	b- Bar Chart 2: Average Sales by Brand
Visualizations 3: Average prices by Brand and Year
	a- Plot Chart 1: Average Price Results by Brand per Year Manufactured
Visualizations 4: Price results by COLOR
	a- Bar Chart 1: Average Auction Price by Color
	b- Plot Chart 2: Price Realized for Each Bag by Brand Based on Color
	b- Plot Chart 3: Average Price Realized by Brand Based on Color
Visualization 5: Leather
   a- Bar Chart 1: Average Price by Leather type


## Ethical Considerations


Our project raises several ethical considerations related to luxury goods and data usage:


1. **Environmental Impact**: Many of the highest-priced bags in our analysis use exotic leathers from alligators and crocodiles. While we present this data objectively, we acknowledge the environmental and animal welfare concerns associated with these materials. Sustainable alternatives are increasingly important in the luxury market.


2. **Data Privacy**: We have been careful to  use publicly available anonymized auction data that will not compromise bidder privacy, ensuring no sensitive user information was exposed.


3. **Wealth Inequality**: The luxury handbag market represents significant wealth concentration. Our analysis shows bags selling for up to $274,600—more than many people's annual incomes. We present this information for educational purposes while acknowledging the broader socioeconomic context.


4. **Cultural Considerations**: Luxury consumption varies across cultures, and our analysis of Hong Kong auction data may reflect regional preferences not representative of global trends. We've attempted to avoid cultural generalizations in our analysis.


We believe that transparent data analysis can help consumers and industry professionals make more informed decisions while being mindful of these ethical considerations.Bias Mitigation was addressed by critically evaluating data sources for fairness and transparency, and by cleaning the dataset in a considerate manner, minimizing skewed representations. Transparency was maintained by thoroughly documenting all processes, allowing for clear auditability and reproducibility.


## Key Insights
- Hermès bags consistently achieve the highest auction prices, especially limited edition and exotic leather designs
- Exotic leathers like alligator and crocodile command significantly higher prices compared to standard leather options
- White, multicolor, and turquoise bags achieve the highest average prices, while silver and yellow are the lowest-performing colors
- Recent years, especially 2021 and beyond, saw an increase in luxury handbag prices, reflecting strong demand
- Most bags sell within or above their estimated price range, showcasing a robust secondary market for luxury handbags


## Technologies Used
- **Database**: SQLite3
- **Backend**: Java Script, Python, Pandas
- **Visualization**: Matplotlib, Plotly, Altair (new library not covered in class)
- **Frontend**: HTML, CSS, Bootstrap


## Project Contributors
- Sade Beckles
- Patricia Daher
- Arisleyda Reyes


## Data Sources
Christie's Auction House website: 
Auction data specifically from Christie's Hong Kong March 2025 Handbags Online sale titled : Handbags Online: The Hong Kong Edit https://onlineonly.christies.com/s/handbags-online-hong-kong-edit/lots/3721)


## References for Data and Code
All data in the csv files and database has been extracted from Christie's auction results for Christie's Hong Kong March 2025 Online Handbags sale titled : Handbags Online: The Hong Kong Edit  https://www.christies.com/en/results
All code in app.py, index.html and LuxuryBags.jpynb has been extracted from ChatGbt and Deep Seek, tweeked by Deepseek, and adjusted by the project contributors.
Chat Gbt Website: https://chatgpt.com/
Deep Seek Website: https://chat.deepseek.com/sign_in








