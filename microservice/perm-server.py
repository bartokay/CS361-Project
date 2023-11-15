# citation: https://docs.python.org/3/library/http.server.html#http.server.SimpleHTTPRequestHandler

import http.server
import socketserver
import json
import random
from urllib.parse import urlparse, parse_qs

class MyServer(http.server.BaseHTTPRequestHandler):
    def permutations(self, min, max):
        nums = list(range(min, max + 1))
        random.shuffle(nums)
        return nums

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        min_max = parse_qs(urlparse(self.path).query)
        min = int(min_max["min"][0])
        max = int(min_max["max"][0])
        perm = self.permutations(min, max)

        self.wfile.write(bytes(json.dumps({'perm': perm}), 'utf-8'))


PORT = 8000

with socketserver.TCPServer(("", PORT), MyServer) as httpd:
    print("serving at port ", PORT)
    httpd.serve_forever()
    


