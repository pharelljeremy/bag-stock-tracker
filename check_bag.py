from playwright.sync_api import sync_playwright
from datetime import datetime
import sys

URL = "https://bash.com/ff-mini-bucket-bag-sage-green-000003aclz9/p?skuId=2825852"

selectors = [
    "#addToCartBtn",
    "button:has-text('Add to cart')",
    "button:has-text('ADD TO CART')",
]

print("="*50)
print("👜 STOCK CHECK")
print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print(URL)
print("="*50)

def find_button(page):
    for sel in selectors:
        try:
            return page.wait_for_selector(sel, timeout=8000)
        except:
            pass
    for f in page.frames:
        for sel in selectors:
            try:
                return f.wait_for_selector(sel, timeout=8000)
            except:
                pass
    return None

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    page = browser.new_page()
    page.goto(URL, timeout=45000, wait_until="domcontentloaded")

    btn = find_button(page)

    if not btn:
        print("⚠️ Button not found (slow load / bot protection)")
        sys.exit(0)  # inconclusive → no alert

    text = btn.inner_text().strip().lower()
    print(f"🔍 Button text: '{text}'")

    if text != "add to cart":
        print("🚨🚨 STATUS CHANGED — POSSIBLE STOCK CHANGE 🚨🚨")
        sys.exit(1)

    print("✅ Still normal (Add to cart)")

