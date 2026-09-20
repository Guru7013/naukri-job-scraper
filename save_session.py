from playwright.sync_api import sync_playwright
import os

PROFILE_DIR = "naukri_profile"

with sync_playwright() as p:

    context = p.chromium.launch_persistent_context(
        PROFILE_DIR,
        headless=False
    )

    page = context.pages[0] if context.pages else context.new_page()

    page.goto(
        "https://www.naukri.com/",
        wait_until="domcontentloaded",
        timeout=60000
    )

    print("Naukri opened.")
    print("Please click Login and login normally.")
    print("After you are fully logged in, come back to this terminal.")

    input("Press ENTER only after you are successfully logged in...")

    print("Browser profile saved.")
    print("You can close the browser now.")

    input("Press ENTER to close...")

    context.close()