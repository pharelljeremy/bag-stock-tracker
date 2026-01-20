from playwright.sync_api import sync_playwright
from datetime import datetime
import sys

URL = "https://bash.com/ff-mini-bucket-bag-sage-green-000003aclz9/p?skuId=2825852"

print("="*50)
print("👜 STOCK CHECK")
print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print(URL)
print("="*50)

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(URL, timeout=15000)
        
        # Wait up to 10s for the button to appear
        try:
            btn = page.wait_for_selector("#addToCartBtn", timeout=10000)
        except:
            btn = None

        if not btn:
            print("🚨 Add-to-cart button missing (or not loaded yet)")
            sys.exit(1)

        text = btn.inner_text().strip()
        print(f"🔍 Button text: '{text}'")

        if text.lower() != "add to cart":
            print("🚨🚨 STATUS CHANGED — POSSIBLE STOCK CHANGE 🚨🚨")
            sys.exit(1)
        else:
            print("✅ Still normal (Add to cart)")
            sys.exit(0)

except Exception as e:
    print("⚠️ Error:", e)
    sys.exit(0)

