import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

# Load .env
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(env_path)

TOKEN = os.getenv("BROWSERLESS_TOKEN")

if not TOKEN:
    raise RuntimeError("BROWSERLESS_TOKEN not found in .env")

# Browserless native Playwright endpoint
WS_ENDPOINT = (
    f"wss://production-sfo.browserless.io/"
    f"chromium/playwright?token={TOKEN}&proxy=residential&proxyCountry=in"
)

with sync_playwright() as p:

    print("Connecting to Browserless...")

    browser = p.chromium.connect(WS_ENDPOINT)

    print("Connected to Browserless successfully.")

    page = browser.new_page()

    print("Opening Naukri...")

    page.goto(
        "https://www.naukri.com/",
        wait_until="domcontentloaded",
        timeout=60000
    )

    print("Naukri opened successfully.")
    print("Page title:", page.title())
    print("Current URL:", page.url)

    input("Press ENTER to close...")

    browser.close()

    print("Browserless connection closed.")