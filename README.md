# SMTP-Enum

![SMTP Enum Demo](screenshot.png)

> **Username Enumeration Tool For OSCP Prep** > *Created by: [@logic0x01](https://github.com/logic0x01)*

**SMTP-Enum** is a lightweight, high-speed Python 3 tool designed for security researchers and penetration testers to identify valid users on a target mail server. It leverages the SMTP `VRFY` command to query the server and determine if a specific username exists.

---

## 🚀 Features

* **Dual-Mode Enumeration:** Supports both single-username checks (`-u`) and massive wordlist attacks (`-w`).
* **Intelligent Response Handling:** Automatically identifies SMTP success codes (`250` and `252`).
* **Creative UI:** Features a stylized ASCII banner and color-coded terminal output for better readability.
* **Error Resilient:** Includes socket timeouts and exception handling to prevent hanging during scans.

---

## 🛠️ Installation

Ensure you have **Python 3.x** installed on your system.

1. **Clone the repository:**

    git clone [https://github.com/logic0x01/smtp-enum](https://github.com/logic0x01/smtp-enum)
    cd SMTP-Enum

2. **Set permissions:**

    chmod +x smtp_user_enum.py

---

## 🧪 Development & Local Testing (New!)

To test this tool safely without scanning public servers (which may be illegal or blocked), we have included a **Mock SMTP Server**. This script creates a fake mail server on your local machine that responds to queries.

### 1. Start the Mock Server
The server runs on the standard SMTP **Port 25**, so it requires root privileges. Open a terminal and run:

    sudo python3 mock_smtp_server.py

> *You should see: `[+] Mock SMTP Server running on 127.0.0.1:25`*

### 2. Run the Tool
Open a **new terminal window**. You can now run `smtp-enum` against your local machine.

**Check a single user:**

    python3 smtp_user_enum.py -t 127.0.0.1 -u admin

**Check a list of users:**
We have included a sample `usernames.txt` for testing.

    python3 smtp_user_enum.py -t 127.0.0.1 -w usernames.txt

---

## 📖 Usage

The tool uses `optparse` for a clean command-line experience.

**View Help Menu:**

    python3 smtp_user_enum.py -h

**Enumerate using a Wordlist:**

    python3 smtp_user_enum.py -t <TARGET_IP> -w usernames.txt

**Check a Single Username:**

    python3 smtp_user_enum.py -t <TARGET_IP> -u admin

---

## ⚙️ Technical Details
The tool works by establishing a TCP connection to **Port 25** and interacting with the SMTP protocol:

1.  **Connection:** Opens a socket connection to the target.
2.  **Handshake:** Receives the server banner.
3.  **Validation:** Sends the `VRFY` command followed by the username.
4.  **Logic:**
    * **250:** Requested mail action okay, completed. (Valid User)
    * **252:** Cannot VRFY user, but will accept message. (Likely Valid User)
    
---

### ⚠️ Disclaimer
*This tool is for educational purposes and authorized security testing only. Do not use this tool against servers you do not own or have explicit permission to test.*
