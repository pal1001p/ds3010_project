# Connecticut Real Estate Sales Analysis & Price Prediction

## Overview
This project analyzes the **Connecticut Real Estate Sales Dataset (2001–2023)** from Connecticut Open Data to understand housing market trends and build predictive models for estimating property prices.

It combines **data cleaning, exploratory data analysis (EDA), visualization, and machine learning** to support a future web application where users can estimate home prices and evaluate neighborhood investment decisions.

---

## Dataset

We use the **Connecticut Real Estate Sales Dataset (2001–2023)**, which includes property sales information such as:

- List price  
- Sale price  
- Sales ratio (sale price / list price)  
- Property type  
- Town / location  
- Address and geospatial coordinates  
- Listing and recording dates  

### Dataset Summary
- Time range: 2001–2023  
- Price range: ~$700 to $160,000,000  
- Average sale price: ~$465,000  
- Includes residential, commercial, industrial, and vacant land properties  

---

## Data Cleaning Steps

To ensure data quality and reliability, the following preprocessing steps were applied:

- Removed rows with missing values in **Location** and **Address** (required for geospatial analysis and heat map construction)
- Removed rows with any value in **Non Use Code**
  - These indicate sales that are not reliable for property valuation  
  - Source: Connecticut Open Data documentation  
- Dropped irrelevant columns:
  - `OPM Remarks`
  - `Assessor Remarks`
- Reduced dataset size from **1,000,000+ records → ~200,000 usable records**

---

## Exploratory Data Analysis (EDA)

### Price Distribution
- Extremely wide range of property values
- Strong right-skew due to high-value commercial and land sales
- Majority of properties fall within typical residential price ranges

---

### Sales Ratio Analysis
- Sales ratio = (Sale Price / List Price)
- Distribution peaks around **~55%**
- Indicates most properties sell below listing price → **buyer’s market**
- Few extreme outliers above 175% and below 25%
- Overall distribution is right-skewed

---

### Geographic Trends
- Highest number of sales in:
  - Stamford  
  - Norwalk  
  - Bridgeport  
- Likely influenced by:
  - Proximity to New York City  
  - Highway access (I-95 corridor)  
- Suggests strong commuter-driven housing demand

---

### Property Type Distribution
- Majority of sales are **residential properties**
- Includes:
  - Single-family homes  
  - Condos  
  - Apartments  
- “Residential” category may be an umbrella label, potentially inflating counts due to missing specificity

---

### Average Sale Price by Property Type
- Commercial, industrial, and apartment properties have significantly higher average sale prices
- Likely reflects:
  - Bulk property transactions (e.g., entire buildings)
  - Not individual unit-level sales

---

### Time-Based Trends
- Clear dip around **2008 financial crisis**
- Another fluctuation period between **2015–2019**
- Strong upward trend in recent years, including post-COVID recovery
- Overall long-term growth despite economic downturns

---

## Machine Learning Model

A regression-based model was developed to estimate property prices using key features such as:

- Location  
- Property type  
- Listing price  
- Sales ratio  
- Historical trends  

---

# Final Project Application 

### Home Price Estimation
- Input desired home characteristics  
- Receive estimated price using trained model  

### Neighborhood Market Insights
- View average home prices by location  
- Analyze local pricing trends  

### Investment Decision Support
- Assess whether building or buying in a specific area is financially viable  

---

## Next Steps

- Implement logistic regression model in backend pipeline  
- Build API for real-time predictions  
- Integrate model into web application frontend  
- Improve feature engineering and geospatial analysis  
- Add interactive visualizations (heat maps, trend dashboards)  

---

## Key Insight

Despite short-term fluctuations (2008 crash, COVID-era shifts), Connecticut real estate shows a **long-term upward pricing trend**, with strong geographic clustering in commuter-accessible cities near New York.

---
