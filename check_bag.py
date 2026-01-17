import requests
from bs4 import BeautifulSoup
from datetime import datetime
import sys

URL = "https://bash.com/ff-mini-bucket-bag-sage-green-000003aclz9/p?skuId=2825852"

print("=" * 60)
print("👜 BASH BAG STOCK CHECKER - ALERT SYSTEM")
print("=" * 60)
print(f"⏰ Check time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"🔗 URL: {URL}")
print("-" * 60)

try:
    # Fetch page
    response = requests.get(
        URL, 
        headers={'User-Agent': 'Mozilla/5.0'},
        timeout=10
    )
    response.raise_for_status()
    
    # Parse HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Look for "Unavailable" in button text
    buttons = soup.find_all('span', class_=lambda c: c and 'buttonText' in c)
    
    is_available = True  # Assume available until proven otherwise
    
# Around line 32-35, CHANGE THIS:
    if 'unavailable' in button_text:
        is_available = False
        print("✅ Confirmed: 'unavailable' found in button")
        break

    # TO THIS (for testing):
    if False:  # if 'unavailable' in button_text:
        is_available = False
        print("✅ Confirmed: 'unavailable' found in button")
        break    
        print("-" * 60)
    
    if is_available:
        print("🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉")
        print("🚨🚨🚨 BAG MIGHT BE AVAILABLE! 🚨🚨🚨")
        print("🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉")
        print("")
        print("📍 CHECK IMMEDIATELY:")
        print(f"🔗 {URL}")
        print("")
        print("⏰ Time is critical - bags sell out fast!")
        print("=" * 60)
        sys.exit(1)  # ⭐ FAIL - triggers "FAILED" email alert
    else:
        print("❌ STATUS: Still unavailable")
        print("✅ System working - no alert needed")
        print("⏰ Next automatic check: Tomorrow")
        print("=" * 60)
        sys.exit(0)  # ⭐ SUCCEED - no email
        
except Exception as e:
    print(f"⚠️ ERROR: {e}")
    print("System will try again tomorrow")
    print("=" * 60)
    sys.exit(0)  # Succeed on error (no alert email)
