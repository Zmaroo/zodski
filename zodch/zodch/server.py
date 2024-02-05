import http.server
import socketserver

PORT = 8000  # Choose an available port

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/quit-signal':
            # Handle the quit signal here (e.g., set a global variable to True)
            global quit_requested
            quit_requested = True
            self.send_response(200)
            self.end_headers()
        else:
            super().do_GET()

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Serving at http://localhost:{PORT}")
    httpd.serve_forever()
