from dns import resolver
from dns.resolver import NXDOMAIN, NoAnswer
import textwrap
import subprocess
from typing import Dict, Union
import sys
import logging
import json

IP_FILE = "ips.json"


def get_json(file: str = IP_FILE) -> Dict:
    try:
        with open(file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File {file} not found")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {file}")
        return {}


def update_json_value(new_data: Dict, file: str = IP_FILE):
    try:
        try:
            with open(file, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in {file}")
            return False

        data.update(new_data)

        with open(file, "w") as f:
            # f.write(json.dumps(data))
            json.dump(data, f, indent=4)
        return True

    except Exception as e:
        print(f"Error writing to {file}: {str(e)}")
        return False



def dns_query(data: Dict, record_type: str = "A") -> Union[str, None]:
    domain = data.get("domain")
    ns = data.get("ns", "8.8.8.8")
    try:
        r = resolver.Resolver()
        r.nameservers = [ns]
        answers = r.resolve(domain, record_type)
        if answers:
            return str(answers[0])
        else:
            return None
    except NXDOMAIN:
        logging.error(f"Domain '{domain}' does not exist at {ns}.")
        return None
    except NoAnswer:
        logging.error(f"No {record_type} record found for '{domain}' at {ns}.")
        return None
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None


def ufw_delete(ip: str, comment: str) -> None:
    try:
        subprocess.run(
            ["sudo", "ufw", "delete", "allow", "from", ip, "to", "any", "comment", comment],
            check=True,
        )
    except (subprocess.CalledProcessError, IndexError):
        logging.error(f"Unable to delete {ip} ({comment}) from UFW!")


def ufw_add(ip: str, comment: str) -> None:
    try:
        subprocess.run(
            ["sudo", "ufw", "allow", "from", ip, "to", "any", "comment", comment], check=True
        )
    except (subprocess.CalledProcessError, IndexError):
        logging.error(f"Unable to add {ip} ({comment}) to UFW!")


def help() -> None:
    text = textwrap.dedent(f"""
        DNS - UFW Updater
        To use, pass the DNS entry as a command-line argument to this script to update UFW rules
        Example:  {sys.argv[0]} my.ddns.com
        You can optionally pass a DNS server to use:  {sys.argv[0]} my.ddns.com 8.8.8.8""")
    print(text)


def process_arguments() -> Dict:
    args = {}
    if len(sys.argv) < 2:
        help()
        sys.exit(1)
    args["domain"] = sys.argv[1]
    if len(sys.argv) > 2:
        args["ns"] = sys.argv[2]
    return args


def main():
    args = process_arguments()
    json_data = get_json()
    current_ip = json_data.get(args.get("domain"), None)
    new_ip = dns_query(args)

    if not new_ip:
        logging.error(f"Cannot retrieve IP for {args.get('domain')}")
        exit()

    if new_ip != current_ip:
        # ufw_delete(new_ip, ddns)
        update_json_value(new_data={args.get('domain'): new_ip})
        # ufw_add(new_ip, ddns)
        logging.info(f"New IP {new_ip} written to file")


if __name__ == "__main__":
    main()
