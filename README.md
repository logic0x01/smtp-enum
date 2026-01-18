SMTP-Enum: Username Enumeration Tool For OSCP Prep

Created by: @logic0x01

SMTP-Enum is a lightweight, high-speed Python 3 tool designed for security researchers and penetration testers to identify valid users on a target mail server. It leverages the SMTP VRFY command to query the server and determine if a specific username exists.

🚀 Features

    Dual-Mode Enumeration: Supports both single-username checks (-u) and massive wordlist attacks (-w).

    Intelligent Response Handling: Automatically identifies SMTP success codes (250 and 252).

    Creative UI: Features a stylized ASCII banner and color-coded terminal output for better readability.

    Error Resilient: Includes socket timeouts and exception handling to prevent hanging during scans.

🛠️ Installation

Ensure you have Python 3.x installed on your system.

    Clone the repository:
    

    git clone https://github.com/yourusername/SMTP-Enum.git
    cd SMTP-Enum

    Set permissions (Linux/macOS):
    

    chmod +x smtp_enum.py

📖 Usage

The tool uses optparse for a clean command-line experience.
Basic Help
Bash

```
python3 smtp_enum.py --help
```

Enumerate using a Wordlist


```
python3 smtp_enum.py -t <TARGET_IP> -w usernames.txt
```

Check a Single Username

```
python3 smtp_enum.py -t <TARGET_IP> -u admin
```

 Technical Details

The tool works by establishing a TCP connection to Port 25 and interacting with the SMTP protocol:

    Connection: Opens a socket connection to the target.

    Handshake: Receives the server banner.

    Validation: Sends the VRFY command followed by the username.

    Logic:

        250: Requested mail action okay, completed.

        252: Cannot VRFY user, but will accept message and attempt delivery (Commonly used by servers to indicate a valid user without confirming it explicitly).
