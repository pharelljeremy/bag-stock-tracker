from playwright.sync_api import sync_playwright, TimeoutError as PWTimeoutError
from datetime import datetime
import os, sys

URL = "https://stevemadden.co.za/products/bevelyn-mm-cream"
DIR = os.getenv("GITHUB_WORKSPACE", ".")

def snapshot(page, name):
    try:
        with open(os.path.join(DIR, name), "w", encoding="utf-8") as f:
            f.write(page.content())
        print(f"📸 Snapshot saved: {name}")
    except Exception as e:
        print("⚠️ Snapshot failed:", e)

print("="*50)
print("👜 STOCK CHECK")
print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print(URL)
print("="*50)

selectors = [
    "#addToCartBtn",
    "button.product-form__cart-submit",
    "button:has-text('Add to cart')",
    "button:has-text('ADD TO CART')",
    "button[type=submit]:visible"
]

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = browser.new_page(viewport={"width":1280,"height":800})
        page.goto(URL, timeout=45000, wait_until="networkidle")

        btn = None
        for s in selectors:
            try:
                btn = page.wait_for_selector(s, timeout=12000, state="visible")
                print(f"🔎 Found button: {s}")
                break
            except PWTimeoutError:
                print(f"❌ Not found: {s}")

        if not btn:
            print("🚨 Add-to-cart missing")
            snapshot(page, "missing_add_to_cart.html")
            sys.exit(1)

        text = btn.inner_text().strip().lower()
        print(f"🔍 Button text: '{text}'")

        if "add to cart" not in text:
            print("🚨🚨 STATUS CHANGED 🚨🚨")
            snapshot(page, "status_changed.html")
            sys.exit(1)

        print("✅ Still in stock")
        sys.exit(0)

except Exception as e:
    print("💥 Script error:", e)
    sys.exit(1)

