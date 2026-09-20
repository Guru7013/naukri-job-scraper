from flask import Flask, render_template_string
from playwright.sync_api import sync_playwright
import threading
import time
import os

app = Flask(__name__)

PROFILE_DIR = "naukri_profile"

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Naukri Job Scraper</title>

    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            margin-top: 100px;
            background: #f5f5f5;
        }

        .box {
            background: white;
            width: 500px;
            margin: auto;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.15);
        }

        h1 {
            color: #333;
        }

        p {
            color: #555;
        }

        button {
            background: #0073e6;
            color: white;
            border: none;
            padding: 15px 30px;
            font-size: 18px;
            border-radius: 8px;
            cursor: pointer;
        }

        button:hover {
            background: #005bb5;
        }

        .status {
            margin-top: 25px;
            font-size: 18px;
            color: #333;
        }
    </style>
</head>

<body>

<div class="box">

    <h1>Naukri Job Scraper</h1>

    <p>Click the button to open Naukri using your saved login.</p>

    <form action="/login" method="post">
        <button type="submit">Login to Naukri</button>
    </form>

    <div class="status">
        {{ message }}
    </div>

</div>

</body>
</html>
"""


def open_naukri():

    try:

        if not os.path.exists(PROFILE_DIR):
            print("ERROR: Naukri profile not found.")
            print("Please run save_session.py first.")
            return

        playwright = sync_playwright().start()

        context = playwright.chromium.launch_persistent_context(
            PROFILE_DIR,
            headless=False
        )

        page = context.pages[0] if context.pages else context.new_page()

        page.goto(
            "https://www.naukri.com/",
            wait_until="domcontentloaded",
            timeout=60000
        )

        page.wait_for_timeout(5000)

        print("Naukri opened using saved browser profile.")
        print("Your saved login session is being used.")

        # Keep browser open
        while True:
            time.sleep(5)

    except Exception as e:

        print("Error:", e)


@app.route("/")
def home():

    return render_template_string(
        HTML,
        message="Ready. Click the button to open Naukri."
    )


@app.route("/login", methods=["POST"])
def login():

    thread = threading.Thread(
        target=open_naukri,
        daemon=True
    )

    thread.start()

    return render_template_string(
        HTML,
        message="Naukri opened using your saved login session."
    )


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )