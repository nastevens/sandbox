import sys
from xml.etree import ElementTree
import httplib2

def print_my_recent_bookmarks(username, password):
    client = httplib2.Http(".cache")
    client.add_credentials(username, password)

    # Make the HTTP request, and fetch the response and body
    response, xml = client.request('https://api.del.icio.us/v1/posts/recent')

    # Turn the XML entity-body into a data structure
    doc = ElementTree.fromstring(xml)

    # Print information about every bookmark
    for post in doc.findall('post'):
        print('{description}: {href}'.format_map(post.attrib))

# Main program
if len(sys.argv) != 3:
    print("Usage: {} [username] [password]" % sys.argv[0])
    sys.exit()

username, password = sys.argv[1:]
print_my_recent_bookmarks(username, password)
