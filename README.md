# Amazon product ranking analysis

## Overview
This project investigates the key factors influencing product ranking on Amazon.be and examines the stability of that ranking over time to provide actionable insights for sellers to optimize their product visibility in Amazon's competitive marketplace.

## Project highlights
- Analyze **28,406 unique product listings** from Amazon.be
- Data collected between **March 21-27, 2025**
- Employe **Gradient Boosted Tree Learning-to-Rank model (LambdaMART)**
- Applie **survival analysis** to understand ranking stability over time

## Repository structure

### ltr-gbt-lambdamart-model/
- `ltr-gbt-lambdamart.ipynb`: Main Learning-to-Rank model notebook

### scraping/
- `html_retrieve_pp.py`: Retrieve HTML of product pages from ASIN
- `html-retrieve-serp.py`: Retrieve HTML of SERP from search queries
- `initial_cleaning_data.ipynb`: Initial data preprocessing
- `product_parser.py`: Parse HTML files into structured product information

### survival-analysis/
- `main/`: Main implementation directory
- `surviva_analysis.ipynb`: Survival analysis notebook

### tabular-data/
- `data/`: Organized dataset directory
  - `data_2025-03-21.zip` to `data_2025-03-27.zip`: Product page data (March 21–27)
  - `keywords.csv`: List of keywords used
  - `semantic.csv`: Semantic similarity scores using Hugging Face model
  - `product_page.zip`: Unique product data

### Root files
- `README.md`: Project documentation
