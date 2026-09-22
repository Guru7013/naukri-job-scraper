from http.server import BaseHTTPRequestHandler
import json
import pandas as pd
import os


class handler(BaseHTTPRequestHandler):

    def do_GET(self):

        try:
            file_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "naukri_jobs.xlsx"
            )

            df = pd.read_excel(file_path)

            df = df.fillna("")

            jobs = df.to_dict(orient="records")

            data = {
                "total_jobs": len(jobs),
                "jobs": jobs
            }

            body = json.dumps(data, default=str).encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            self.wfile.write(body)

        except Exception as e:

            body = json.dumps({
                "error": str(e),
                "total_jobs": 0,
                "jobs": []
            }).encode("utf-8")

            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(body)