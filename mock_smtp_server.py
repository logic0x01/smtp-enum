#!/usr/bin/python3

import socket
import sys
import os

# A simple Mock SMTP server that runs on the standard Port 25.
# REQUIRES SUDO/ROOT privileges.
def start_server(host='127.0.0.1', port=25):
    # Check if running as root
    if os.geteuid() != 0:
        print(f"[-] Error: Binding to port {port} requires root privileges.")
        print(f"    Please run: sudo python3 {sys.argv[0]}")
        sys.exit(1)

    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Allow reusing the address to avoid "Address already in use" errors
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen(1)
        
        print(f"\n[+] Mock SMTP Server running on {host}:{port} (Privileged)")
        print("[+] Any VRFY command will return 'User Found'")
        print("[!] Press Ctrl+C to stop...\n")

        while True:
            try:
                client, addr = server.accept()
                print(f"[>] Connection received from {addr[0]}")

                client.send(b"220 MockSMTP Server Ready\r\n")

                while True:
                    data = client.recv(1024)
                    if not data: break
                    
                    decoded = data.decode('utf-8', errors='ignore').strip()
                    if not decoded: continue

                    print(f"    [Received]: {decoded}")

                    if decoded.upper().startswith("HELO") or decoded.upper().startswith("EHLO"):
                        client.send(b"250 Hello\r\n")
                    
                    elif decoded.upper().startswith("VRFY"):
                        # Extract the username requested
                        parts = decoded.split(" ")
                        user = parts[-1] if len(parts) > 1 else "Unknown"
                        
                        # Respond with Success (250)
                        client.send(f"250 2.0.0 {user} User found\r\n".encode())
                        print(f"    [Action]: Confirmed user '{user}'")
                        
                    elif decoded.upper().startswith("QUIT"):
                        client.send(b"221 Bye\r\n")
                        break
                    else:
                        client.send(b"250 OK\r\n")
                        
                client.close()
                print("[<] Connection closed\n")

            except Exception as e:
                print(f"[-] Client Error: {e}")

    except KeyboardInterrupt:
        print("\n[!] Stopping server...")
        server.close()
        sys.exit()
    except Exception as e:
        print(f"\n[-] Fatal Error: {e}")

if __name__ == "__main__":
    start_server()