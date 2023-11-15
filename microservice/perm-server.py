# citations: https://docs.python.org/3/library/http.server.html#http.server.SimpleHTTPRequestHandler
#            https://itecnote.com/tecnote/python-parse-http-get-and-post-parameters-from-basehttphandler/

import http.server
import socketserver
import json
import random
from urllib.parse import urlparse, parse_qs
import re

class MyServer(http.server.BaseHTTPRequestHandler):
    def _permutations(self, min, max):
        """
        returns a random permutation of the numbers between min and max
        """
        nums = list(range(min, max + 1))
        random.shuffle(nums)
        return nums

    def _send_response(self, code, json_obj):
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(bytes(json_obj, 'utf-8'))

    def _validate_min_max(self, min, max):
        if min > max:
            raise Exception("min less than max")
        if min < 0 or max > 1000:
            raise Exception("min max range: 0-1000")
        
    def do_GET(self):
        
        # validate path: /perm/?min=1&max=4
        if re.search(r"/perm/\?min=[0-9]+&max=[0-9]+", self.path):

            try:
                min_max = parse_qs(urlparse(self.path).query)
                min, max = int(min_max["min"][0]), int(min_max["max"][0])
                self._validate_min_max(min, max)

                # get permutation
                perm = self._permutations(min, max)

                # send response with permutation
                self._send_response(200, json.dumps({'perm': perm}))
                
            except Exception as err:    
                self._send_response(400, json.dumps({'error_message': str(err)}))
        else:
            self._send_response(404, json.dumps({'error_message': 'URL Not Found'}))

PORT = 8000

with socketserver.TCPServer(("", PORT), MyServer) as httpd:
    print("serving at port ", PORT)
    httpd.serve_forever()
    


