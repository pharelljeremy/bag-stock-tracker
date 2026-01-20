from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
from datetime import datetime
import sys
import re

URL = "https://bash.com/ff-mini-bucket-bag-sage-green-000003aclz9/p?skuId=2825852"

def norm(s: str) -> str:
    return re.sub(r'\s+', ' ', s or '').strip().lower()

print("="*50)
print("👜 STOCK CHECK")
print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print(URL)
print("="*50)

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800},
            java_script_enabled=True,
        )
        page = context.new_page()

        try:
            # give more time for heavy pages
            resp = page.goto(URL, timeout=30000, wait_until="domcontentloaded")
            status = resp.status if resp else "no-response"
            print(f"HTTP status: {status}")
        except PWTimeout as e:
            print("⚠️ page.goto timed out:", e)
            # still try to continue; maybe partial content loaded
        except Exception as e:
            print("⚠️ page.goto failed:", e)

        # Wait up to 20s for the button to be visible by several strategies
        btn = None
        selectors = [
            "#addToCartBtn",
            "button.product-form__cart-submit",
            "button[id^=addToCart]",
            "button:has-text(\"Add to cart\")",
            "button:has-text(\"ADD TO CART\")",
        ]
        for sel in selectors:
            try:
                # wait for visible element
                btn = page.wait_for_selector(sel, timeout=20000, state="visible")
                if btn:
                    print(f"Found button using selector: {sel}")
                    break
            except PWTimeout:
                # not found with this selector
                btn = None
            except Exception as e:
                print(f"Warning: selector {sel} raised {e}")
                btn = None

        if not btn:
            # Save a small snippet of the page for debugging
            snippet = page.content()[:2000]  # first 2k chars
            print("🚨 Add-to-cart button missing (or not visible). Page snippet:")
            print(snippet)
            context.close()
            browser.close()
            sys.exit(1)

        # Try to get visible text; normalize whitespace and case
        text = btn.inner_text().strip()
        norm_text = norm(text)
        print(f"🔍 Button text (raw): '{text}'")
        print(f"🔍 Button text (normalized): '{norm_text}'")

        # If button text is empty, try computed style or aria-label
        if not norm_text:
            aria = btn.get_attribute("aria-label") or ""
            alt_text = norm(aria)
            print(f"🔍 aria-label: '{aria}' -> normalized '{alt_text}'")
            if alt_text:
                norm_text = alt_text

        # Accept several variants
        expected_variants = {"add to cart", "add to bag", "addtocart", "add to basket"}
        if norm_text not in expected_variants:
            print("🚨🚨 STATUS CHANGED — POSSIBLE STOCK CHANGE OR LABEL DIFFERENCE 🚨🚨")
            context.close()
            browser.close()
            sys.exit(1)
        else:
            print("✅ Still normal (Add to cart)")
            context.close()
            browser.close()
            sys.exit(0)

except Exception as e:
    print("⚠️ Unexpected Error:", repr(e))
    sys.exit(0)

