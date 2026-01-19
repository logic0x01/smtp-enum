#!/usr/bin/python3

import socket 
import optparse
import sys
from time import sleep


# Colors
G, Y, R, W, B = '\033[92m', '\033[93m', '\033[91m', '\033[0m', '\033[94m'

def print_banner(target, mode, delay, command):
    banner = f"""
{B}  _______________________________________________________________
{B} /                                                               \\
{B} |   {Y}███████╗███╗   ███╗████████╗██████╗     ███████╗███╗   ██╗██╗   ██╗{B} |
{B} |   {Y}██╔════╝████╗ ████║╚══██╔══╝██╔══██╗    ██╔════╝████╗  ██║██║   ██║{B} |
{B} |   {Y}███████╗██╔████╔██║   ██║   ██████╔╝    █████╗  ██╔██╗ ██║██║   ██║{B} |
{B} |   {Y}╚════██║██║╚██╔╝██║   ██║   ██╔═══╝     ██╔══╝  ██║╚██╗██║██║   ██║{B} |
{B} |   {Y}███████║██║ ╚═╝ ██║   ██║   ██║         ███████╗██║ ╚████║╚██████╔╝{B} |
{B} |   {Y}╚══════╝╚═╝     ╚═╝   ╚═╝   ╚═╝         ╚══════╝╚═╝  ╚═══╝ ╚═════╝ {B} |
{B} \\_______________________________________________________________/
                                              {W}By: {Y}@logic0x01{W}
    
    {B}[*]{W} Target : {G}{target}{W}
    {B}[*]{W} Mode   : {G}{mode}{W}
    {B}[*]{W} Delay  : {G}{delay}s{W}
    {B}[*]{W} Command  : {G}{command}
    """
    print(banner)

# Parser Setup
usage = f"\n  {sys.argv[0]} -t <target> [-w <file> | -u <user>] [options]"



parser = optparse.OptionParser(usage=usage)

parser.add_option('-t', '--target', dest='target', help='Target IP or Hostname')
parser.add_option('-w', '--wordlist', dest='wordlist', help='Path to usernames  wordlist')
parser.add_option('-u', '--username', dest='username', help='Single username to check')
parser.add_option('-d', '--delay', dest='delay', type="float", default=0.0, help='Delay between requests')
parser.add_option('-c', '--command', dest='command', default="VRFY", help='SMTP command (default: VRFY)')

opts, args = parser.parse_args()

if not opts.target or (not opts.wordlist and not opts.username):
    parser.print_help()
    sys.exit(1)


mode = "Single User" if opts.username and not opts.wordlist else "Wordlist"
print_banner(opts.target, mode, opts.delay, opts.command)

# Load usernames
usernames_to_check = []
if opts.username: usernames_to_check.append(opts.username)
if opts.wordlist:
    try:
        with open(opts.wordlist, 'r') as file:
            usernames_to_check.extend([u.strip() for u in file.readlines()])
    except FileNotFoundError:
        print(f"{R}[!] Error: Wordlist '{opts.wordlist}' not found.{W}")
        sys.exit(1)

# Enumeration
try:
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.settimeout(10) 
    
    print(f"{B}[*]{W} Connecting to target...")
    soc.connect((opts.target, 25))
    banner_raw = soc.recv(1024)

    print(f"{B}[*]{W} Scanning {G}{len(usernames_to_check)}{W} entries...\n")

    for username in usernames_to_check:
        if opts.delay > 0:
            sleep(opts.delay)
        
        cmd_string = f"{opts.command} {username}\r\n"
        soc.send(cmd_string.encode())
        result = soc.recv(1024).decode(errors='ignore')
        
        if "250" in result or "252" in result:
            print(f"{G}[+]{W} VALID: {Y}{username}{W}")

except Exception as e:
    print(f"{R}[!] Connection error: {e}{W}")
finally:
    soc.close()
    print(f"\n{B}[*]{W} Done.")
