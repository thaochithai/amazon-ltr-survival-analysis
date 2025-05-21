import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import random
import logging
import re
import os
import schedule
from datetime import datetime
import argparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('amazon_html_scraper_1.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class AmazonHTMLScraper:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.setup_driver()
        # Create base directory for HTML files
        self.base_dir = "amazon_html_data_1"
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
        base_delay=random.uniform(min_seconds, max_seconds)
        extra_delay=random.uniform(0,2) if random.random()< 0.1 else 0  # 10% chance of extra delay
        time.sleep(base_delay + extra_delay)

    def get_search_page_html(self, search_term, page_number=1):
        """
        Get the full HTML of a search results page
        
        Args:
            search_term (str): The search term
            page_number (int): The page number to retrieve (default: 1)
            
        Returns:
            str: The HTML content of the page
        """
        try:
            url = f"https://www.amazon.com.be/s?k={search_term.replace(' ', '+')}&page={page_number}&language=en_GB"
            logger.info(f"Retrieving URL: {url}")
            
            self.driver.get(url)
            self._random_delay()
            
            # Wait for search results to load
            try:
                results_selector = "div[data-component-type='s-search-result']"
                self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, results_selector)))
            except TimeoutException:
                logger.warning(f"Timeout waiting for search results on page {page_number} for term '{search_term}'")
            
            # Return the full HTML
            return self.driver.page_source
            
        except Exception as e:
            logger.error(f"Error getting HTML for search term '{search_term}' page {page_number}: {str(e)}")
            return ""

    def save_html_to_file(self, html_content, search_term, page_number, timestamp):
        """
        Save HTML content to a file with organized directory structure
        
        Args:
            html_content (str): The HTML content to save
            search_term (str): The search term
            page_number (int): The page number
            timestamp (datetime): The timestamp when the data was collected
        """
        if not html_content:
            logger.warning(f"No HTML content to save for term '{search_term}' page {page_number}")
            return
            
        # Create directory structure: base_dir/search_term/date/hour_minute/
        safe_term = re.sub(r'[^a-zA-Z0-9]', '_', search_term)
        date_str = timestamp.strftime("%Y-%m-%d")
        time_str = timestamp.strftime("%H-%M-%S")
        hour_minute_str = timestamp.strftime("%H-%M")
        
        term_dir = os.path.join(self.base_dir, safe_term)
        date_dir = os.path.join(term_dir, date_str)
        time_dir = os.path.join(date_dir, hour_minute_str)
        
        os.makedirs(time_dir, exist_ok=True)
        
        # Create filename with search term, page number, and timestamp with seconds
        filename = f"{safe_term}_page{page_number}_{time_str}.html"
        filepath = os.path.join(time_dir, filename)
        
        # Save the HTML content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        logger.info(f"Saved HTML for '{search_term}' page {page_number} to {filepath}")

    def close(self):
        """Clean up resources"""
        if self.driver:
            self.driver.quit()


def scrape_search_pages(input_csv):
    """
    Scrape search pages for all terms in the input CSV
    
    Args:
        input_csv (str): Path to the input CSV file containing search terms
    """
    try:
        # Read search terms from CSV
        df = pd.read_csv(input_csv)
        if 'Keyword' not in df.columns:
            logger.error("CSV file does not have a 'Keyword' column")
            return
            
        search_terms = df['Keyword'].dropna().tolist()
        if not search_terms:
            logger.error("No valid search terms found in input CSV")
            return
            
        logger.info(f"Starting HTML scraping for {len(search_terms)} search terms")
        
        scraper = AmazonHTMLScraper()
        timestamp = datetime.now()
        
        try:
            for i, search_term in enumerate(search_terms):
                logger.info(f"Processing search term {i + 1}/{len(search_terms)}: {search_term}")
                
                # Get 3 pages for each search term
                for page in range(1, 4):
                    html_content = scraper.get_search_page_html(search_term, page)
                    scraper.save_html_to_file(html_content, search_term, page, timestamp)
                    
                    # Add delay between pages
                    if page < 3:
                        time.sleep(random.uniform(1, 3))
                
                # Add longer pause between search terms
                if i < len(search_terms) - 1:
                    time.sleep(random.uniform(3, 7))
                    
        finally:
            scraper.close()
            
        logger.info("HTML scraping completed successfully")
        
    except Exception as e:
        logger.error(f"Error in scrape_search_pages: {str(e)}")


def run_scheduled_job(input_csv):
    """Run the scraping job and log the execution time"""
    start_time = datetime.now()
    logger.info(f"Starting scheduled scraping job at {start_time}")
    
    try:
        scrape_search_pages(input_csv)
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds() / 60
        logger.info(f"Completed scheduled job in {duration:.2f} minutes")
    except Exception as e:
        logger.error(f"Error in scheduled job: {str(e)}")


def schedule_jobs(input_csv):
    """
    Schedule the scraping job to run at specific even hours: 0,2,4,6,8,10,12,14,16,18,20,22
    
    Args:
        input_csv (str): Path to the input CSV file
    """
    logger.info("Setting up schedule to run at even hours (0,2,4,6,8,10,12,14,16,18,20,22)")
    
    # Schedule for every even hour
    for hour in [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22]:
        schedule.every().day.at(f"{hour:02d}:00").do(run_scheduled_job, input_csv)
        logger.info(f"Scheduled job for {hour:02d}:00")
    
    # Determine if we should run immediately
    current_hour = datetime.now().hour
    current_minute = datetime.now().minute
    
    if current_hour % 2 == 0:
        # We're at an even hour, check if we've just missed the scheduled time
        if current_minute > 5:  # If more than 5 minutes past the hour, run now
            logger.info(f"Current time is {current_hour}:{current_minute}, running job immediately")
            run_scheduled_job(input_csv)
    else:
        # Current hour is odd, run immediately
        logger.info(f"Current hour ({current_hour}) is not in schedule. Running job immediately.")
        run_scheduled_job(input_csv)
    
    # Keep the script running to execute scheduled jobs
    logger.info("Entering schedule loop. Press Ctrl+C to exit.")
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check for pending jobs every minute
    except KeyboardInterrupt:
        logger.info("Schedule interrupted by user")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Collect Amazon search results HTML for tracking')
    parser.add_argument('input_csv', help='Path to input CSV file containing search terms')
    parser.add_argument('--run-once', action='store_true', help='Run once without scheduling')
    
    args = parser.parse_args()
    
    try:
        logger.info(f"Starting with input file: {args.input_csv}")
        
        if args.run_once:
            logger.info("Running once without scheduling")
            scrape_search_pages(args.input_csv)
        else:
            logger.info("Setting up schedule to run at even hours (0,2,4,...,22)")
            schedule_jobs(args.input_csv)
            
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        raise