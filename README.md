# DDNS UFW Updater

A Python script to dynamically update UFW firewall rules based on DDNS (Dynamic DNS) IP changes, designed to run as a cron job. The script queries DNS records, stores them in a JSON file (`ips.json`), and updates UFW rules when IP changes are detected. It supports optional DNS server specification and adds comments to UFW rules for easy identification.

## Features
- **Dynamic DNS Resolution**: Retrieves IP addresses for specified DDNS domains.
- **Persistent Storage**: Stores resolved IPs in `ips.json` for tracking changes.
- **UFW Integration**: Automatically updates UFW firewall rules by removing old IPs and adding new ones with DDNS-specific comments.
- **Cron-Friendly**: Designed to be executed via cron, running in a Python virtual environment.
- **Custom DNS Support**: Optionally specify a DNS server for queries (e.g., Google DNS, Cloudflare).
- **Idempotent Operation**: Safely handles cases where IPs haven't changed, avoiding redundant UFW updates.

## Prerequisites
- **Python 3.6+**: Ensure Python is installed.
- **UFW**: Installed and configured on your system (Ubuntu or compatible).
- **Python Libraries**:
  - `dnspython` for DNS resolution
  - `json` for handling the IP storage file
  - `subprocess` for UFW system calls
- **Cron**: For scheduling automated runs.
- **Virtual Environment** (recommended): To isolate dependencies.

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/py-ddns-ufw.git
   cd py-ddns-ufw
   ```

2. Set up a Python virtual environment:
    ```
    python3 -m venv venv
   source venv/bin/activate
    ```

3. Install required Python packages:
    ```
    pip install -r requirements.txt
    ```

4. Ensure UFW is enabled and configured:
    ```
    sudo ufw status
    ```

## Usage
Run the script manually to test:
```
python main.py <domain> [dns_server]
```
- `<domain>`: The DDNS domain to resolve (e.g., `myhost.dyndns.org`).
- `[dns_server]` (optional): The DNS server to query (e.g., `8.8.8.8` for Google DNS). Defaults to system DNS if not provided.

Example:
```
python main.py myhost.dyndns.org 1.1.1.1
```

### Setting Up Cron
To automate updates, add a cron job to run the script periodically. Edit the crontab:
```
crontab -e
```

Add a line like this to run every 5 minutes:
```
*/5 * * * * /path/to/venv/bin/python /path/to/main.py myhost.dyndns.org 8.8.8.8
```

Ensure the script has executable permission
```
chmod +x main.py
```

## How It Works
1. **DNS Query**: Resolves the provided DDNS domain to an IP address using `dnspython`.
2. **IP Storage**: Checks `ips.json` in the working directory for the last known IP of the domain.
3. **IP Comparison**: Compares the resolved IP with the stored IP.
4. **UFW Update** (if changed):
   - Deletes the old UFW rule (if it exists) using the stored IP.
   - Adds a new UFW rule with the updated IP and a comment (e.g., `allow from <IP> to any # myhost.dyndns.org`).
5. **JSON Update**: Updates `ips.json` with the new IP.
6. **Idempotency**: Skips UFW updates if the IP hasn't changed.

### File Structure
- `ddns_ufw_updater.py`: The main Python script.
- `ips.json`: Stores the last resolved IPs (created automatically if it doesn't exist).
- `requirements.txt`: Lists Python dependencies.
- `README.md`: This file.

## Example `ips.json`
```
{
  "myhost.dyndns.org": "192.168.1.100",
  "anotherhost.ddns.net": "203.0.113.50"
}
```


## Security Notes
- **Sudo Privileges**: The script requires `sudo` to modify UFW rules. Ensure the cron job or user has appropriate permissions.
- **Firewall Safety**: The script only modifies rules for specific IPs and includes comments for traceability.
- **DNS Security**: Use trusted DNS servers to avoid DNS poisoning risks.

## Troubleshooting
- **UFW Errors**: Ensure UFW is installed and enabled (`sudo ufw enable`).
- **Permission Denied**: Verify the script has permissions to read/write `ips.json` and execute UFW commands.
- **DNS Resolution Fails**: Check the DNS server or try a public one like `8.8.8.8` or `1.1.1.1`.
- **Cron Issues**: Test the command manually to ensure the virtual environment and paths are correct.

## Contributing
Contributions are welcome! Please:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/my-feature`).
3. Commit changes (`git commit -m 'Add my feature'`).
4. Push to the branch (`git push origin feature/my-feature`).
5. Open a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Built with [dnspython](https://github.com/rthalley/dnspython) for DNS resolution.
- Designed for Ubuntu systems with UFW.
- Inspired by the need for simple, automated DDNS firewall management.

---

Happy firewalling! 🚀