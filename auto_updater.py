import os
import hmac
import hashlib
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer

SECRET_KEY = os.getenv("GITHUB_WEBHOOK_SECRET", "super_kiasu_secret").encode()
DEPLOY_CMD = "cd ~/berry-brain-bot && git pull && source .venv/bin/activate && pip install --upgrade -r requirements.txt && sudo systemctl restart berry-brain-bot"

class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        signature = self.headers.get('X-Hub-Signature-256')

        if not signature:
            self.send_response(400)
            self.end_headers()
            return

        # Verify HMAC Cryptographic Signature
        mac = hmac.new(SECRET_KEY, msg=post_data, digestmod=hashlib.sha256)
        expected_sig = "sha256=" + mac.hexdigest()

        if not hmac.compare_digest(expected_sig, signature):
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b"Signature mismatch. Rejected.")
            return

        # Execute Zero-Bandwidth Auto-Update Protocol
        try:
            print("[WEBHOOK] Valid GitHub Signature received. Triggering Auto-Updater...")
            subprocess.Popen(DEPLOY_CMD, shell=True, executable="/bin/bash")
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Kiasu Deployment triggered!")
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())

def run(server_class=HTTPServer, handler_class=WebhookHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting Kiasu Auto-Updater Webhook Listener on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
