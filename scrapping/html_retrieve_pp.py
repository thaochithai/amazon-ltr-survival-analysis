import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import random
import logging
import re
import os
from datetime import datetime
import argparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('amazon_product_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class AmazonProductHTMLScraper:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.setup_driver()
        
        # Create base directory for HTML files
        self.base_dir = "amazon_product_html_data"
        os.makedirs(self.base_dir, exist_ok=True)

    def setup_driver(self):
        """Initialize Chrome driver with optimal settings for data collection"""
        chrome_options = Options()
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        # Add randomized user agent
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
        ]
        chrome_options.add_argument(f'user-agent={random.choice(user_agents)}')

        # Add preferences to appear more like a regular user
        chrome_options.add_experimental_option("prefs", {
            "profile.default_content_settings.popups": 0,
            "profile.password_manager_enabled": False,
            "credentials_enable_service": False,
            "profile.default_content_setting_values.notifications": 2
        })

        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 5)

        # Execute CDP commands to make detection harder
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": random.choice(user_agents)
        })

        # Add additional JavaScript to mask automation
        self.driver.execute_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)

    def _random_delay(self, min_seconds=3, max_seconds=7):
        """Implements humanized delay between actions"""
        base_delay = random.uniform(min_seconds, max_seconds)
        extra_delay = random.uniform(0, 2) if random.random() < 0.1 else 0  # 10% chance of extra delay
        time.sleep(base_delay + extra_delay)

    def get_product_page_html(self, asin):
        """
        Get the full HTML of a product page
        
        Args:
            asin (str): The Amazon Standard Identification Number
            
        Returns:
            str: The HTML content of the page
        """
        try:
            url = f"https://www.amazon.com.be/dp/{asin}?language=en_GB"
            logger.info(f"Retrieving URL: {url}")
            
            self.driver.get(url)
            self._random_delay()
            
            # Just wait for page load - no specific element needed as we're just capturing HTML
            time.sleep(2)  # Give the page a moment to fully load
            
            # Return the full HTML
            return self.driver.page_source
            
        except Exception as e:
            logger.error(f"Error getting HTML for product ASIN '{asin}': {str(e)}")
            return ""

    def save_html_to_file(self, html_content, asin, search_term):
        """
        Save HTML content to a file organized by search term
        
        Args:
            html_content (str): The HTML content to save
            asin (str): The product ASIN
            search_term (str): The search term associated with this product
        """
        if not html_content:
            logger.warning(f"No HTML content to save for ASIN '{asin}'")
            return
            
        # Create directory structure: base_dir/search_term/
        # Create safe directory name from search term
        safe_term = re.sub(r'[^a-zA-Z0-9]', '_', search_term)
        
        # Create timestamp for the filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create search term directory
        term_dir = os.path.join(self.base_dir, safe_term)
        os.makedirs(term_dir, exist_ok=True)
        
        # Create filename with ASIN and timestamp
        filename = f"{asin}_{timestamp}.html"
        filepath = os.path.join(term_dir, filename)
        
        # Save the HTML content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        logger.info(f"Saved HTML for ASIN '{asin}' (search term: '{search_term}') to {filepath}")

    def close(self):
        """Clean up resources"""
        if self.driver:
            self.driver.quit()


def scrape_product_pages(input_csv):
    """
    Scrape product pages for all ASINs in the input CSV, organizing by search term
    
    Args:
        input_csv (str): Path to the input CSV file containing ASINs and search terms
    """
    try:
        # Read from CSV
        df = pd.read_csv(input_csv)
        
        # Use fixed column names
        asin_column = 'asin'
        search_term_column = 'search_term'
        
        # Check if the required columns exist
        if asin_column not in df.columns:
            logger.error(f"CSV file does not have the required 'asin' column. Available columns: {', '.join(df.columns)}")
            return
            
        if search_term_column not in df.columns:
            logger.error(f"CSV file does not have the required 'search_term' column. Available columns: {', '.join(df.columns)}")
            return
            
        # Create a clean dataset with both ASIN and search term
        df = df[[asin_column, search_term_column]].dropna()
        
        if df.empty:
            logger.error("No valid ASIN and search term pairs found in input CSV")
            return
            
        # Convert to string to ensure proper handling
        df[asin_column] = df[asin_column].astype(str)
        df[search_term_column] = df[search_term_column].astype(str)
            
        logger.info(f"Starting HTML scraping for {len(df)} products")
        
        scraper = AmazonProductHTMLScraper()
        
        try:
            for i, row in df.iterrows():
                asin = row[asin_column]
                search_term = row[search_term_column]
                
                logger.info(f"Processing product {i + 1}/{len(df)}: ASIN {asin} (search term: {search_term})")
                
                html_content = scraper.get_product_page_html(asin)
                scraper.save_html_to_file(html_content, asin, search_term)
                
                # Add delay between product pages to avoid being blocked
                if i < len(df) - 1:
                    time.sleep(random.uniform(2, 5))
                    
        finally:
            scraper.close()
            
        logger.info("Product HTML scraping completed successfully")
        
    except Exception as e:
        logger.error(f"Error in scrape_product_pages: {str(e)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Collect Amazon product page HTML organized by search term')
    parser.add_argument('input_csv', help='Path to input CSV file containing product ASINs and search terms')
    parser.add_argument('--batch-size', type=int, default=100, 
                        help='Number of products to process before taking a longer break (default: 100)')
    parser.add_argument('--batch-delay', type=int, default=60,
                        help='Delay in seconds between batches (default: 60)')
    
    args = parser.parse_args()
    
    try:
        logger.info(f"Starting with input file: {args.input_csv}")
        
        # If there are many ASINs, process them in batches
        df = pd.read_csv(args.input_csv)
        
        # Use fixed column names
        asin_column = 'asin'
        search_term_column = 'search_term'
        
        # Check if the required columns exist
        if asin_column not in df.columns or search_term_column not in df.columns:
            logger.error(f"CSV file must have both 'asin' and 'search_term' columns. Available columns: {', '.join(df.columns)}")
            exit(1)
            
        # Create a clean dataset
        df = df[[asin_column, search_term_column]].dropna()
        total_products = len(df)
        
        if total_products <= args.batch_size:
            # Process all at once if the number is small
            scrape_product_pages(args.input_csv)
        else:
            # Process in batches
            logger.info(f"Processing {total_products} products in batches of {args.batch_size}")
            
            for i in range(0, total_products, args.batch_size):
                batch_end = min(i + args.batch_size, total_products)
                logger.info(f"Processing batch {i//args.batch_size + 1}: Products {i+1} to {batch_end}")
                
                # Create temporary CSV for this batch
                batch_df = df.iloc[i:batch_end].copy()
                batch_csv = f"temp_batch_{i}.csv"
                batch_df.to_csv(batch_csv, index=False)
                
                # Process the batch
                scrape_product_pages(batch_csv)
                
                # Remove temporary file
                os.remove(batch_csv)
                
                # Take a break between batches
                if batch_end < total_products:
                    logger.info(f"Taking a {args.batch_delay} second break before the next batch")
                    time.sleep(args.batch_delay)
            
            logger.info("All batches processed successfully")
            
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        raise