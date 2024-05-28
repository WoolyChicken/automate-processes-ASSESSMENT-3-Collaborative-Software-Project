import configparser
import os
import urllib.error
import urllib.request
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def read_config(config_file):
    # Read URLs from the configuration file
    config = configparser.ConfigParser()
    try:
        config.read(config_file)
        return config['DEFAULT']
    except Exception as e:
        logger.error(f"Error reading configuration file: {e}")
        raise

def download_block_lists(urls):
    # Download domain block lists from URLs
    lists = []
    for url in urls:
        if not url:
            logger.warning("Empty URL found, skipping.")
            continue
        try:
            with urllib.request.urlopen(url) as response:
                if response.getcode() == 200:
                    lists.append(response.read().decode().splitlines())
                else:
                    logger.error(f"Failed to download block list from {url}: HTTP {response.getcode()}")
        except urllib.error.URLError as e:
            logger.error(f"Failed to download block list from {url}: {e}")
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
    try:
        if os.path.exists(hosts_path) and not os.path.exists(backup_path):
            os.system(f"cp {hosts_path} {backup_path}")
    except Exception as e:
        logger.error(f"Error backing up hosts file: {e}")
        raise

def append_to_hosts_file(domains):
    # Append blocked domains to the hosts file
    hosts_path = 'C:\\Windows\\System32\\drivers\\etc\\hosts'  # Adjust path based on your OS
    try:
        with open(hosts_path, 'a') as hosts_file:
            for domain in domains:
                hosts_file.write(f"127.0.0.1 {domain}\n")
    except Exception as e:
        logger.error(f"Error appending to hosts file: {e}")
        raise

def main():
    try:
        config = read_config("config.ini")
        urls = config.get("urls", "").split(",")
        lists = download_block_lists(urls)
        domains = parse_block_lists(lists)
        backup_hosts_file()
        append_to_hosts_file(domains)
        logger.info("Blocking domains added to hosts file successfully.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
