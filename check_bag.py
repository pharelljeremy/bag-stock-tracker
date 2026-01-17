import requests
import sys
from bs4 import BeautifulSoup
from datetime import datetime

# Configuration
URL = "https://bash.com/ff-mini-bucket-bag-sage-green-000003aclz9/p?skuId=2825852"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

def check_bash_stock():
    print(f"[{datetime.now()}] Checking: {URL}")
    
    try:
        # Fetch the webpage
        headers = {'User-Agent': USER_AGENT}
        response = requests.get(URL, headers=headers, timeout=10)
        response.raise_for_status()  # Check for HTTP errors
        
        # Check if we got a valid response
        if response.status_code != 200:
            print(f"❌ Bad response: {response.status_code}")
            return "ERROR"
        
        print(f"✅ Page loaded successfully")
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Method 1: Look for button with "Unavailable" text
        unavailable_buttons = soup.find_all('button', string=lambda text: text and 'unavailable' in text.lower())
        
        # Method 2: Look for span with class containing "buttonText"
        button_spans = soup.find_all('span', class_=lambda c: c and 'buttonText' in c)
        
        # Method 3: Search all text on page
        all_text = soup.get_text().lower()
        
        print(f"Found {len(unavailable_buttons)} buttons with 'unavailable'")
        print(f"Found {len(button_spans)} button text spans")
        
        # Check all methods
        is_unavailable = False
        
        if unavailable_buttons:
            print("✅ Found 'unavailable' in button text directly")
            is_unavailable = True
        elif button_spans:
            for span in button_spans:
                if 'unavailable' in span.get_text().lower():
                    print("✅ Found 'unavailable' in button span")
                    is_unavailable = True
                    break
        elif 'unavailable' in all_text:
            print("✅ Found 'unavailable' in page text")
            is_unavailable = True
        else:
            print("⚠️  'unavailable' not found in any location")
        
        if is_unavailable:
            print("❌ Bag is still unavailable")
            return "OUT_OF_STOCK"
        else:
            print("🎉🎉🎉 BAG MIGHT BE AVAILABLE! CHECK NOW!")
            print("Link: https://bash.com/ff-mini-bucket-bag-sage-green-000003aclz9/p?skuId=2825852")
            return "IN_STOCK"
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching page: {e}")
        return "ERROR"
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return "ERROR"

def main():
    print("=" * 60)
    print("BASH BAG STOCK CHECKER")
    print("=" * 60)
    
    status = check_bash_stock()
    
    print("\n" + "=" * 60)
    print(f"Final result: {status}")
    print("=" * 60)
    
    # GitHub Actions will show the output in logs
    if status == "IN_STOCK":
        # Make this fail intentionally to get a notification
        # GitHub sends emails for failed workflows by default
        print("\n⚠️  Forcing failure to trigger email notification")
        print("(This is intentional - GitHub emails on workflow failure)")
        sys.exit(1)  # Fail on IN_STOCK to get email
    else:
        sys.exit(0)  # Success exit for out of stock or errors

if __name__ == "__main__":
    main()
