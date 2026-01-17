import requests
import os
import sys
from bs4 import BeautifulSoup
from datetime import datetime

# Configuration
URL = "https://bash.com/ff-mini-bucket-bag-sage-green-000003aclz9/p?skuId=2825852"
OUT_OF_STOCK_TEXT = "unavailable"  # The text we're looking for
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

def check_bash_stock():
    print(f"[{datetime.now()}] Checking: {URL}")
    
    try:
        # Fetch the webpage
        headers = {'User-Agent': USER_AGENT}
        response = requests.get(URL, headers=headers, timeout=10)
        response.raise_for_status()  # Check for HTTP errors
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Get all text on page (lowercase for comparison)
        page_text = soup.get_text().lower()
        
        # Check if "unavailable" is on the page
        if OUT_OF_STOCK_TEXT.lower() in page_text:
            print("❌ Bag is still unavailable")
            return "OUT_OF_STOCK"
        else:
            print("🎉 BAG IS AVAILABLE! Pink bag might be in stock!")
            return "IN_STOCK"
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching page: {e}")
        return "ERROR"
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return "ERROR"

def main():
    status = check_bash_stock()
    
    # Exit with code 0 for success, 1 for error (helps with notifications)
    if status == "IN_STOCK":
        print("SUCCESS: Item might be available!")
        sys.exit(0)  # Success exit code
    elif status == "OUT_OF_STOCK":
        print("Item still unavailable")
        sys.exit(0)  # Success but not in stock
    else:
        sys.exit(1)  # Error exit code

if __name__ == "__main__":
    main()
