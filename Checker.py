#create by Kaiz 

import requests
import time
import sys
from datetime import datetime

# ================= CONFIG =================
TARGET_USERNAMES = ["fyl8", "hr3n"]
WEBHOOK_URL = "https://discord.com/api/webhooks/1389085100297293895/buLkSg9cI7fksPMQq2SZVCtrYHDd50RfzH0fOsMXqj1cGYXswcBPilN2PK_pbwB9NU-6"

CHECK_INTERVAL_SEC = 300  # 5 minutes

# ================= COLORS =================
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    END = '\033[0m'


# ================= WEBHOOK =================
def send_webhook(username):
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    payload = {
        "content": f"# 🚨 @everyone A LA DATE DU {now}, TON USERNAME **{username}** EST DISPONIBLE !"
    }

    try:
        requests.post(WEBHOOK_URL, json=payload, timeout=10)
    except Exception as e:
        print(f"{Colors.RED}[WEBHOOK ERROR] {e}{Colors.END}")


# ================= CHECK =================
def check_username(username):
    url = "https://discord.com/api/v9/unique-username/username-attempt-unauthed"

    payload = {"username": username}
    headers = {"Content-Type": "application/json"}

    try:
        r = requests.post(url, json=payload, headers=headers, timeout=10)

        # Affichage debug (important pour comprendre les résultats)
        print(f"{Colors.CYAN}[DEBUG] {username} -> {r.status_code} -> {r.text[:80]}{Colors.END}")

        if r.status_code == 200:
            data = r.json()

            if isinstance(data, dict) and "taken" in data:
                return not data["taken"]

            return None

        if r.status_code == 429:
            print(f"{Colors.YELLOW}[RATE LIMIT]{Colors.END}")
            time.sleep(2)
            return None

        return None

    except Exception as e:
        print(f"{Colors.RED}[ERROR] {e}{Colors.END}")
        return None


# ================= MAIN LOOP =================
def run():
    print(f"{Colors.CYAN}Starting Discord username checker...{Colors.END}")

    already_sent = set()

    while True:
        for username in TARGET_USERNAMES:

            available = check_username(username)
            now = datetime.now().strftime("%H:%M:%S")

            # AVAILABLE
            if available is True:
                print(f"{Colors.GREEN}[{now}] AVAILABLE → {username}{Colors.END}")

                if username not in already_sent:
                    send_webhook(username)
                    already_sent.add(username)

            # NOT AVAILABLE
            elif available is False:
                print(f"{Colors.RED}[{now}] NOT AVAILABLE → {username}{Colors.END}")

            # ERROR / UNKNOWN
            else:
                print(f"{Colors.YELLOW}[{now}] UNKNOWN / ERROR → {username}{Colors.END}")

        print(f"\n{Colors.CYAN}Waiting {CHECK_INTERVAL_SEC} seconds...\n{Colors.END}")
        time.sleep(CHECK_INTERVAL_SEC)


# ================= START =================
if __name__ == "__main__":
    if WEBHOOK_URL == "TON_WEBHOOK_ICI":
        print(f"{Colors.RED}ERROR: mets ton webhook URL{Colors.END}")
        sys.exit(1)

    run()
