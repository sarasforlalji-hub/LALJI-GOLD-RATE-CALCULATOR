from playwright.sync_api import sync_playwright
import json, datetime

URL = "https://emeraldbullion.com/"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(URL)

    # Wait until GOLD row is populated
    page.wait_for_function("""() => {
        const el = document.querySelector('#DivSpotRate');
        return el && el.innerText.includes('GOLD');
    }""")

    # Select the GOLD row specifically
    gold_row = page.locator("#DivSpotRate .mht").nth(0)  # GOLD is first row
    row_text = gold_row.inner_text()

    # Split values: [GOLD, BID, ASK, HIGH, LOW]
    parts = row_text.split()
    gold_ask = parts[2]   # second value after 'GOLD'

    data = {
        "gold_ask": gold_ask,
        "fetched_at": datetime.datetime.utcnow().isoformat()
    }

    with open("gold.json", "w") as f:
        json.dump(data, f, indent=2)

    browser.close()
