#!/usr/bin/env python3
import subprocess
import json
import requests
from email.mime.text import MIMEText

# === CONFIG ===
CONFIG_FILE = "coins.json"
EMAIL_FROM = "mike@nyxium.live"
EMAIL_TO = "mike@nyxium.live"
SMTP_SERVER = "localhost"
SMTP_PORT = 587

def get_local_version(command):
    try:
        output = subprocess.check_output(command.split(), stderr=subprocess.STDOUT).decode()
        # Extract first version-like string found
        for part in output.split():
            if any(char.isdigit() for char in part):
                return part.strip("v")  # remove 'v' if present
    except Exception as e:
        return f"Error: {e}"

def get_latest_github_release(repo):
    url = f"https://api.github.com/repos/{repo}/releases/latest"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get("tag_name", "").strip("v")
        return "Error fetching release"
    except Exception as e:
        return f"Error: {e}"

def send_email(subject, message):
    msg = f"To: {EMAIL_TO}\nFrom: {EMAIL_FROM}\nSubject: {subject}\n\n{message}"
    process = subprocess.Popen(["msmtp", "-a", "default", EMAIL_TO], stdin=subprocess.PIPE)
    process.communicate(msg.encode())

def main():
    with open(CONFIG_FILE, "r") as f:
        coins = json.load(f)

    coin_info = []  # This will store all version info

    # Iterate through all coins
    for coin in coins:
        name = coin["name"]
        repo = coin["repo"]
        cmd = coin["local_version_cmd"]

        local_ver = get_local_version(cmd)
        latest_ver = get_latest_github_release(repo)

        # Append the version info for each coin
        coin_info.append(f"{name}:\n  Local:  {local_ver}\n  Latest: {latest_ver}")

    # Combine all coin info into the body
    body = "\n\n".join(coin_info)

    # Send the email with all version info
    send_email("🔍 Coin Version Check Completed", body)

if __name__ == "__main__":
    main()
