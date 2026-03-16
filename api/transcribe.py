from http.server import BaseHTTPRequestHandler
import json


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        body = json.dumps({
            "error": "Transcription is not available on Vercel (Whisper is too large for serverless). Run the app locally with: python app.py — or deploy the Flask app to Render/Railway for full transcription."
        }).encode("utf-8")
        self.wfile.write(body)
        return
