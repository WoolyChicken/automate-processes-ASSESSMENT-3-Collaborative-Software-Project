import configparser
import os
import requests

def read_config(config_file):
    # Read URLs from the configuration file
    config = configparser.ConfigParser()
    config.read(config_file)
    return config['DEFAULT']

def download_block_lists(urls):
    # Download domain block lists from URLs
    lists = []
    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            lists.append(response.text.splitlines())
        else:
            print(f"Failed to download block list from {url}")
    return lists

def parse_block_lists(lists):
    # Parse and merge lists into unique domains
    domains = set()
    for block_list in lists:
        for domain in block_list:
            domains.add(domain.strip())
    return domains

def backup_hosts_file():
    # Backup the original hosts file
    hosts_path = '/etc/hosts'  # Adjust path based on your OS
    backup_path = '/etc/hosts.backup'  # Adjust path based on your preference
    if os.path.exists(hosts_path) and not os.path.exists(backup_path):
        os.system(f"cp {hosts_path} {backup_path}")

def append_to_hosts_file(domains):
    # Append blocked domains to the hosts file
    hosts_path = '/etc/hosts'  # Adjust path based on your OS
    with open(hosts_path, 'a') as hosts_file:
        for domain in domains:
            hosts_file.write(f"127.0.0.1 {domain}\n")

def main():
    config = read_config("config.ini")
    urls = config.get("urls", "").split(",")
    lists = download_block_lists(urls)
    domains = parse_block_lists(lists)
    backup_hosts_file()
    append_to_hosts_file(domains)

if __name__ == "__main__":
    main()
