# Amazon product ranking analysis

## Overview
Online marketplaces are essential platforms for businesses to sell products and for customers to find them quickly and efficiently. These platforms serve three primary stakeholders:
- **Marketplace**
- **Sellers**
- **Customers**

Customers rely on these platforms to reduce search costs when looking for products. Meanwhile, marketplaces like Amazon continuously refine **ranking algorithms** to present the most relevant results. These rankings significantly impact purchase decisions and, in turn, platform revenue. Products that appear higher in search results enjoy increased visibility, click-through rates, and sales, making product ranking optimization critical for sellers and platforms alike.

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

- **Empirical replication** of Amazon’s ranking logic using machine learning  
- **Feature importance analysis** to understand ranking drivers  
- **Novel use of survival analysis** to evaluate ranking persistence  
- **Actionable recommendations** for sellers on how to improve and sustain visibility

## 
## Ranking Model and Survival Analysis: Key Findings

This study identifies key product features affecting Amazon rankings and ranking stability, offering actionable insights for sellers aiming to enhance visibility and performance on the platform.

---

### Ranking Model Results

We evaluate the model's performance and feature importance using XGBoost and SHAP.

#### Model Performance
- **nDCG**: 0.859  
- **Precision**: 0.441  
- These results demonstrate strong predictive ability using publicly scraped data and outperform several comparable studies.
- Performance varies across queries, which aligns with prior research observations.

#### Feature Importance (via SHAP)

- **Sales Performance**  
  - Sales rank is the most predictive feature.
  - Sales badges (e.g., "200+ sold") are important but secondary.
  - 👉 _Sellers should aim to improve sales rank through volume-driving tactics._

- **Sentiment Features**  
  - Review count and product ratings increase relevance.
  - Popularity (derived from reviews, ratings, badges) has minimal extra value.
  - 👉 _Use tools like [Amazon Vine](https://sell.amazon.com/tools/vine) or the "Request a Review" button to build review volume._

- **Pricing**  
  - Price competitiveness matters more than absolute price.
  - Competitive pricing boosts rankings, while discounts show limited effect.
  - 👉 _Leverage dynamic pricing and tools for competitive pricing within search queries._

- **Query-Product Semantic Similarity**  
  - Semantic title match is significantly more important than keyword stuffing.
  - Lexical similarity has negligible impact.
  - 👉 _Use semantically rich language aligned with customer intent. Use tools like [Search Query Performance](https://sellercentral.amazon.com/help/hub/reference/external/G8J4CB5ZBF3NX7TP) to guide content updates._


### Survival Analysis Results

We analyze how listings maintain visibility over time (i.e., "ranking survival").

#### Survival Probabilities

- **Organic Listings**  
  - Sharp early drop, especially within first 15–30 hours.
  - Stabilize after surviving initial competition.
  
- **Sponsored Listings**  
  - High initial survival due to ad placement.
  - Decline over time due to ad pacing or budget constraints.
  
- Both listing types converge to ~75% daily survival probability after Day 2.

#### Feature Effects on Survival Time

- **Organic Hourly Survival**  
  - Improved by: sales badge, review volume, rating.
  - Not significantly affected by price competitiveness.

- **Sponsored Hourly Survival**  
  - Improved by: competitive pricing.
  - Limited influence from reviews or ratings (due to paid placement dynamics).

- **Daily Survival (Both Types)**  
  - Strongly predicted by initial rank and category sales rank.
  - Subcategory rank has inverse relationship (possibly due to lower competition).
  
👉 _Sellers should prioritize feature optimization during high-risk periods: early hours and Days 2–3._

### Strategic Implications

Tailor product listing strategies by feature importance and desired timeframe:

| Feature                    | Rank Impact | Hourly Survival (Organic) | Hourly Survival (Sponsored) | Daily Survival (Organic) | Daily Survival (Sponsored) |
|----------------------------|-------------|----------------------------|------------------------------|---------------------------|-----------------------------|
| Sub-category sales rank    | +++         | ↑                          | ↑                            | ○                         | ↑                           |
| Main category sales rank   | +++         | ↓                          | ○                            | ○                         | ↓                           |
| Sales badge                | ++          | ↑                          | ○                            | ↑                         | ○                           |
| Price competitiveness      | +++         | ○                          | ↑                            | ○                         | ○                           |
| Semantic title             | +++         |                            |                              |                           |                             |
| Review count               | ++          | ↑                          | ○                            | ○                         | ○                           |
| Rating                     | ++          | ↓                          | ○                            | ○                         | ○                           |
| Semantic bullet points     | ++          |                            |                              |                           |                             |
| Price                     | ++          | ↑                          | ○                            | ↑                         | ↑                           |
| Discount                   | ++          | ↑                          | ○                            | ○                         | ○                           |
| Semantic description       | ++          |                            |                              |                           |                             |
| Prime badge                | +           | ↑                          | ○                            | ↑                         | ↑                           |
| Popularity                 | +           | ↑                          | ○                            | ○                         | ○                           |
| Initial rank               | -           | ↓                          | ↓                            | ↓                         | ↓                           |

> 🔹 `+++` = High importance, `++` = Medium, `+` = Low  
> 🔹 `↑` = Improves survival, `↓` = Reduces survival, `○` = Not significant

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
