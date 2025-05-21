# Amazon product ranking analysis

## Overview
This project investigates the key factors influencing product ranking on Amazon.be and examines the stability of that ranking over time to provide actionable insights for sellers to optimize their product visibility in Amazon's competitive marketplace.

## Project highlights
- Analyzed **28,406 unique product listings** from Amazon.be
- Data collected between **March 21-27, 2025**
- Employed **Gradient Boosted Tree Learning-to-Rank model (LambdaMART)**
- Applied **survival analysis** to understand ranking stability over time

## Repository structure
├── ltr-gbt-lambdamart-model/       # Learning-to-Rank model implementation
│   ├── ltr-gbt-lambdamart.ipynb    # Main model notebook
├── scraping/                       # Data collection utilities
│   ├── html_retrieve_pp.py         # Retrieve HTML of product pages from ASIN
│   ├── html-retrieve-serp.py       # Retrieve HTML of SERP from search queries
│   ├── initial_cleaning_data.ipynb # Initial data preprocessing
│   ├── product_parser.py           # Parse HMTL file retrieved to structured product information
├── survival-analysis/              # Ranking stability analysis
│   ├── main                        # Main implementation
│   └── surviva_analysis.ipynb      # Survival analysis notebook
├── tabular-data/                   # Dataset after parsing and convert into tabular format with asin as identifier
│   ├── data/                       # Organized data directory
│   │   ├── data_2025-03-21.zip     #  (March 21)
│   │   ├── data_2025-03-22.zip     # Product page data (March 22)
│   │   ├── data_2025-03-23.zip     # Product page data (March 23)
│   │   ├── data_2025-03-24.zip     # Product page data (March 24)
│   │   ├── data_2025-03-25.zip     # Product page data (March 25)
│   │   ├── data_2025-03-26.zip     # Product page data (March 26)
│   │   ├── data_2025-03-27.zip     # Product page data (March 27)
│   │   ├── keywords.csv            # List of keywords used
│   │   ├── semantic.csv            # Semantic simiarity score using model from Hugging Face 
│   │   └── product_page.zip        # Unique product data
└── README.md                       # Project documentation

## Key findings

### Ranking features (by importance)
1. **Sales rank** is the most influential factor
2. **Price competitiveness** is more important than heavy discount and setting low price
3. **Semantic similarity** between product title and search query

### Difference between survival probabilities between sponsored vs. organic Listings
- **Sponsored products**: Greater short-term ranking stability but more likely to drop in position over time
- **Organic listings**: More sustainable long-term ranking performance

## Practical implications
- Ad placements should be viewed as **tactical tools for short-term visibility**
- Sustained success requires strong **organic performance**
- Focus on **competitive pricing, high-quality content, and reviews** for long-term visibility

## Dataset
The dataset consists of 28,406 unique product listings scraped from Amazon.be between March 21 and 27, 2025. Data includes product attributes, ranking positions, pricing information, and review metrics.

## Methodology
1. **Data collection**: scraping product listings information from Amazon.be using 106 popular search queries 
2. **Ranking model**: using GBT LambdaMART algorithm to identify influential features
4. **Survival analysis**: Kaplan Meier curves, Weibull PHM

