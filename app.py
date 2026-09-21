from flask import Flask, send_file, jsonify, request
from playwright.sync_api import sync_playwright
import pandas as pd
import threading
import os
import time

app = Flask(__name__)

PROFILE_DIR = "naukri_profile"
EXCEL_FILE = "naukri_jobs.xlsx"


# -----------------------------------
# Read jobs from Excel
# -----------------------------------

def get_jobs():

    if not os.path.exists(EXCEL_FILE):
        return []

    try:
        df = pd.read_excel(EXCEL_FILE)
        df = df.fillna("")

        return df.to_dict(orient="records")

    except Exception as e:

        print("Excel Error:", e)

        return []


# -----------------------------------
# Open Naukri using saved profile
# -----------------------------------

def open_naukri():

    try:

        if not os.path.exists(PROFILE_DIR):

            print("Naukri profile not found.")
            print("Please run save_session.py first.")

            return

        playwright = sync_playwright().start()

        context = playwright.chromium.launch_persistent_context(
            PROFILE_DIR,
            headless=False
        )

        page = (
            context.pages[0]
            if context.pages
            else context.new_page()
        )

        page.goto(
            "https://www.naukri.com/",
            wait_until="domcontentloaded",
            timeout=60000
        )

        page.wait_for_timeout(5000)

        print("Naukri opened successfully.")
        print("Saved login profile is being used.")

        while True:

            time.sleep(5)

    except Exception as e:

        print("Naukri Error:", e)


# -----------------------------------
# Home page
# -----------------------------------

@app.route("/")
def home():

    return send_file("index.html")


# -----------------------------------
# Jobs API
# -----------------------------------

@app.route("/api")
def api_jobs():

    jobs = get_jobs()

    keyword = request.args.get(
        "keyword",
        ""
    ).strip().lower()

    location = request.args.get(
        "location",
        ""
    ).strip().lower()

    filtered_jobs = []

    for job in jobs:

        title = str(
            job.get("Title", "")
        ).lower()

        company = str(
            job.get("Company", "")
        ).lower()

        job_location = str(
            job.get("Location", "")
        ).lower()

        skills = str(
            job.get("Skills", "")
        ).lower()

        keyword_match = True

        location_match = True

        if keyword:

            keyword_match = (
                keyword in title
                or keyword in company
                or keyword in skills
            )

        if location:

            location_match = (
                location in job_location
            )

        if keyword_match and location_match:

            filtered_jobs.append(job)

    return jsonify({

        "total_jobs": len(filtered_jobs),

        "jobs": filtered_jobs

    })


# -----------------------------------
# Login / Open Naukri
# -----------------------------------

@app.route("/login", methods=["POST"])
def login():

    thread = threading.Thread(
        target=open_naukri,
        daemon=True
    )

    thread.start()

    return jsonify({

        "message":
        "Naukri opened using saved login session."

    })


# -----------------------------------
# Start Flask server
# -----------------------------------

if __name__ == "__main__":

    print()

    print("=" * 60)
    print("             NAUKRI JOB SCRAPER")
    print("=" * 60)

    print(
        "Excel File:",
        EXCEL_FILE
    )

    print(
        "Profile:",
        PROFILE_DIR
    )

    print(
        "Website:",
        "http://127.0.0.1:5000"
    )

    print("=" * 60)

    print()

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=False

    )