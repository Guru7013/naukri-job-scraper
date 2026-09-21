from http.server import BaseHTTPRequestHandler
import json
import pandas as pd
import os


class handler(BaseHTTPRequestHandler):

    def do_GET(self):

        excel_file = "naukri_jobs.xlsx"

        jobs = []

        try:
            if os.path.exists(excel_file):
                df = pd.read_excel(excel_file)

                df = df.fillna("")

                jobs = df.to_dict(orient="records")

        except Exception as e:
            print("Error reading Excel:", e)

        data = {
            "project": "Naukri Job Scraper",
            "status": "Deployed successfully",
            "technology": "Python + Playwright",
            "total_jobs": len(jobs),
            "jobs": jobs
        }

        body = json.dumps(data).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        self.wfile.write(body)