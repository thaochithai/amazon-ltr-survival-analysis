# Amazon product ranking analysis

## Overview
Product ranking is critical to user engagement and sales performance on e-commerce marketplaces. Despite its significance, limited research focused on analyzing the features and temporal dynamics that influence product ranking from the seller's perspective. Using a dataset of 28,406 unique product listings scraped from Amazon.be between March 21 and 27, 2025, this study investigates the key factors influencing product ranking and the stability of that ranking over time. Employing a Gradient Boosted Tree Learning-to-Rank model (LambdaMART), the analysis reveals that sales rank is the most influential factor in determining product position, followed by price competitiveness and semantic similarity between title and search query. Additionally, survival analysis highlights that while sponsored products tend to exhibit greater short-term ranking stability, they are significantly more likely to drop to a lower rank over time compared to organic listings. These findings suggest that ad placements should be viewed as tactical tools for short-term visibility, whereas sustained success on Amazon requires strong organic performance, driven by factors such as competitive pricing, high-quality content, and reviews. As a result, this research provides actionable insights for sellers to strategically apply paid and organic approaches to optimize and maintain product visibility in Amazon’s competitive marketplace.

## Project highlights
- Analyze **28,406 unique product listings** from Amazon.be
- Data collected between **March 21-27, 2025**
- Employ **Gradient Boosted Tree Learning-to-Rank model (LambdaMART)**
- Apply **survival analysis** to understand ranking stability over time

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
