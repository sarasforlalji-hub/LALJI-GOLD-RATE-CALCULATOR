from playwright.sync_api import sync_playwright
import json, datetime

URL = "https://emeraldbullion.com/"
SELECTOR = "#goldRate"   # replace this with the actual ID/class

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(URL)

    # wait until the gold price appears (not just "...")
    page.wait_for_function("""() => {
        const el = document.querySelector('#goldRate');
        return el && el.innerText.trim() !== '...';
    }""")

    gold_price = page.inner_text(SELECTOR)

    data = {
        "gold_price": gold_price,
        "fetched_at": datetime.datetime.utcnow().isoformat()
    }

    with open("gold.json", "w") as f:
        json.dump(data, f, indent=2)

    browser.close()
