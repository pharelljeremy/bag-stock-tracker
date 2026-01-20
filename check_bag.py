from playwright.sync_api import sync_playwright
from datetime import datetime
import sys

URL = "https://bash.com/ff-mini-bucket-bag-sage-green-000003aclz9/p?skuId=2825852"

print("=" * 50)
print("👜 STOCK CHECK")
print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print(URL)
print("=" * 50)

selectors = [
    "#addToCartBtn",
    "button#addToCartBtn",
    "button.product-form__cart-submit",
    "button:has-text('Add to cart')",
    "button:has-text('ADD TO CART')",
]

def find_button(page):
    # check main page
    for sel in selectors:
        try:
            btn = page.wait_for_selector(sel, timeout=5000, state="visible")
            if btn:
                print("Found on main page:", sel)
                return btn
        except:
            pass

    # check iframes
    for frame in page.frames:
        for sel in selectors:
            try:
                btn = frame.wait_for_selector(sel, timeout=5000, state="visible")
                if btn:
                    print("Found in iframe:", sel)
                    return btn
            except:
                pass

    return None

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox"]
        )
        page = browser.new_page()
        page.goto(URL, timeout=45000, wait_until="networkidle")

        btn = find_button(page)

        if not btn:
            with open("snapshot.html", "w", encoding="utf-8") as f:
                f.write(page.content())
            print("🚨 Add-to-cart button not found (even in iframes)")
            sys.exit(1)

        text = btn.inner_text().strip()
        print(f"🔍 Button text: '{text}'")

        if text.lower() != "add to cart":
            print("🚨🚨 STATUS CHANGED — POSSIBLE STOCK CHANGE 🚨🚨")
            sys.exit(1)

        print("✅ Still normal (Add to cart)")
        sys.exit(0)

except Exception as e:
    print("⚠️ Error:", e)
    sys.exit(0)

