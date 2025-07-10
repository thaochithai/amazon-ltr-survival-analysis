# Amazon product ranking analysis

## Overview
Online marketplaces are essential platforms for businesses to sell products and for customers to find them quickly and efficiently. These platforms serve three primary stakeholders:
- **The e-commerce marketplace**
- **Sellers**
- **Customers**
Customers rely on these platforms to reduce search costs when looking for products. Meanwhile, marketplaces like Amazon continuously refine **ranking algorithms** to present the most relevant results. These rankings significantly impact purchase decisions and, in turn, platform revenue. Products that appear higher in search results enjoy increased visibility, click-through rates, and sales — making product ranking optimization critical for sellers and platforms alike.

Amazon is the most influential e-commerce marketplace:

- **300M+ monthly active users** (as of 2022)
- **56%** of online shoppers start their product search on Amazon

To help sellers boost visibility, Amazon offers:
- **Sponsored products** (paid search ads)
- **Search Engine Optimization (SEO)** tactics to improve organic rankings

However, the specifics of Amazon’s ranking algorithm are proprietary. Sellers are left to **infer ranking factors** based on experience and experimentation. Complicating things further, **rankings are dynamic**, evolving based on user behavior and competition. While getting to the top is challenging, **staying there is even harder**.

## Research Approach

This project analyzes the Amazon product ranking ecosystem using a dataset of over **28,000 product listings** scraped hourly from [Amazon.be](https://www.amazon.be). It applies two core methodologies:

1. **Learning-to-Rank (LTR)**  
   To approximate Amazon's ranking algorithm and evaluate feature importance

2. **Survival Analysis**  
   To assess the *temporal stability* of product rankings and determine which features help maintain high rank positions over time

## Key Contributions

- 🔍 **Empirical replication** of Amazon’s ranking logic using machine learning  
- 📊 **Feature importance analysis** to understand ranking drivers  
- ⏱️ **Novel use of survival analysis** to evaluate ranking persistence  
- ✅ **Actionable recommendations** for sellers on how to improve and sustain visibility

## Dataset
Using a dataset of 28,406 unique product listings scraped from Amazon.be between March 21 and 27, 2025 (total 1,524,775 rows), this research investigates the key factors influencing product ranking and the stability of that ranking over time. 

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
