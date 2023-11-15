# citations: https://docs.python.org/3/library/http.server.html#http.server.SimpleHTTPRequestHandler
#            https://itecnote.com/tecnote/python-parse-http-get-and-post-parameters-from-basehttphandler/

import http.server
import socketserver
import json
import random
from urllib.parse import urlparse, parse_qs
import re

class MyServer(http.server.BaseHTTPRequestHandler):
    def permutations(self, min, max):
        nums = list(range(min, max + 1))
        random.shuffle(nums)
        return nums

    def do_GET(self):
        
        if re.search(r"/perm/\?min=[0-9]+&max=[0-9]+", self.path):
            try:
                min_max = parse_qs(urlparse(self.path).query)
                min = int(min_max["min"][0])
                max = int(min_max["max"][0])
                if min > max:
                    error = "min less than max"
                    raise Exception
                if min < 0 or max > 1000:
                    error = "min max range: 0-1000"
                    raise Exception
                perm = self.permutations(min, max)

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(bytes(json.dumps({'perm': perm}), 'utf-8'))
            except:    
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(bytes(json.dumps({'error_message': error}), 'utf-8'))
        else:
            self.send_response(404)
            self.wfile.write(bytes(json.dumps({'URL': 'Not Found'}), 'utf-8'))

PORT = 8000

with socketserver.TCPServer(("", PORT), MyServer) as httpd:
    print("serving at port ", PORT)
    httpd.serve_forever()
    


