from http.server import BaseHTTPRequestHandler
import json


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        data = {
            "project": "Naukri Job Scraper",
            "status": "Deployed successfully",
            "technology": "Python + Playwright",
            "message": "Naukri job scraping project is running."
        }

        body = json.dumps(data).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)
