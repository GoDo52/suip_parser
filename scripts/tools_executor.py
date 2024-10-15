import subprocess
import re

def execute_command(command):
    """
    Executes a shell command and returns the output as a list of strings (each line as an element).
    
    Args:
    command (str): The shell command to execute.
    
    Returns:
    list: List of output lines from the command.
    """
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout.splitlines()  # Split output into lines
        return output
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        return []

def filter_subdomains(subdomains_list):
    """
    Filters the subdomain list to only include valid subdomain names.
    
    Args:
    subdomains_list (list): A list of raw subdomain data.

    Returns:
    list: A filtered list of valid subdomains.
    """
    # Regular expression pattern to match valid subdomains
    subdomain_pattern = re.compile(r'^(?:[a-zA-Z0-9-_]+\.)+[a-zA-Z]{2,}$')

    # Filter the list to include only valid subdomains
    valid_subdomains = [sub for sub in subdomains_list if subdomain_pattern.match(sub)]

    return valid_subdomains

def get_subdomains(url: str):
    """
    Retrieves subdomains using amass, subfinder, and findomain by executing their respective commands.
    
    Args:
    url (str): The domain to fetch subdomains for.
    
    Returns:
    list: A combined set of unique and valid subdomains.
    """
    try:
        # Normalize the URL (remove 'http://', 'https://')
        normalized_url = url.removeprefix("http://").removeprefix("https://")

        # Define commands
        amass_command = f"amass enum -passive -d {normalized_url}"
        subfinder_command = f"subfinder -d {normalized_url}"
        findomain_command = f"findomain -t {normalized_url}"

        # Execute commands
        amass_output = execute_command(amass_command)
        subfinder_output = execute_command(subfinder_command)
        findomain_output = execute_command(findomain_command)

        # Combine and deduplicate the results
        raw_subdomains_list = set(amass_output + subfinder_output + findomain_output)

        # Filter the raw subdomains to include only valid subdomains
        valid_subdomains_list = filter_subdomains(raw_subdomains_list)

        return list(valid_subdomains_list)

    except Exception as e:
        print(f'An error occurred: {e}')
        return []


if __name__ == "__main__":
    get_subdomains("https://kali.org")