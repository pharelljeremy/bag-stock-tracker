import requests, sys
from bs4 import BeautifulSoup
from datetime import datetime

URL = "https://bash.com/ff-mini-bucket-bag-sage-green-000003aclz9/p?skuId=2825852"

print("="*50)
print("👜 STOCK CHECK")
print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print(URL)
print("="*50)

try:
    r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")
    btn = soup.find("button", id="addToCartBtn")

    if not btn:
        print("🚨 Add-to-cart button missing")
        sys.exit(1)

    text = btn.get_text(strip=True)
    print(f"🔍 Button text: '{text}'")

    if text.lower() != "add to cart":
        print("🚨🚨 STATUS CHANGED — POSSIBLE STOCK CHANGE 🚨🚨")
        sys.exit(1)   # FAIL → email
    else:
        print("✅ Still normal (Add to cart)")
        sys.exit(0)   # OK → no email

except Exception as e:
    print("⚠️ Error:", e)
    sys.exit(0)       # Don't spam on errors

