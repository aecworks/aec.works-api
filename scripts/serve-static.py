#!/usr/bin/env python3

"""
Static File server to serve apidocs.data locally for development

Usage:
    ~/Desktop/apidocs_data/
    $ ./serve.py
"""
from http.server import HTTPServer, SimpleHTTPRequestHandler, test
import os


class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, HEAD, OPTIONS")
        self.send_header(
            "Access-Control-Allow-Headers",
            "Accept, Referer, Origin, Content-Type, X-Requested-With",
        )
        SimpleHTTPRequestHandler.end_headers(self)


if __name__ == "__main__":
    path = os.environ["STATIC_DIR"]
    os.chdir(path)
    test(CORSRequestHandler, HTTPServer, port=5000)
