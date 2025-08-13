import http.server
import socketserver
import argparse
import urllib.request
from urllib.parse import urlparse
import sys

cache = {}

parser = argparse.ArgumentParser(description="Simple Caching Proxy Server")
parser.add_argument("--port", type=int, default=3000, help="Port to run the proxy server")
parser.add_argument("--origin", type=str, help="Origin server URL")
parser.add_argument("--clear-cache", action="store_true", help="Clear the cache and exit")
args = parser.parse_args()

if args.clear_cache:
    cache.clear()
    print("Cache cleared!")
    sys.exit(0)

if not args.origin:
    print("Error: --origin is required")
    sys.exit(1)

ORIGIN = args.origin.rstrip("/")



class CachingProxyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global cache
        # URL کامل سرور اصلی
        target_url = ORIGIN + self.path

        # بررسی کش
        if target_url in cache:
            data, headers = cache[target_url]
            self.send_response(200)
            for key, value in headers.items():
                self.send_header(key, value)
            self.send_header("X-Cache", "HIT")
            self.end_headers()
            self.wfile.write(data)
            return

        # اگر کش نیست، درخواست به سرور اصلی می‌فرستیم
        try:
            with urllib.request.urlopen(target_url) as response:
                data = response.read()
                headers = {k: v for k, v in response.getheaders()}
                cache[target_url] = (data, headers)

                self.send_response(200)
                for key, value in headers.items():
                    self.send_header(key, value)
                self.send_header("X-Cache", "MISS")
                self.end_headers()
                self.wfile.write(data)

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Error fetching {target_url}: {e}".encode("utf-8"))


if __name__ == "__main__":
    port = args.port
    with socketserver.TCPServer(("", port), CachingProxyHandler) as httpd:
        print(f"Caching Proxy running on port {port}, forwarding to {ORIGIN}")
        httpd.serve_forever()
