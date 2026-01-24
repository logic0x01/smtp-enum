#!/usr/bin/python3

import socket 
import optparse
import sys
from time import sleep
from banner import print_banner , G, Y, R, W, B , usage




parser = optparse.OptionParser(usage=usage)

# Targeting Options
group_target = optparse.OptionGroup(parser, "Targeting Options")
group_target.add_option('-t', '--target', dest='target', 
                  help='Single target IP address or hostname (e.g., 127.0.0.1)')
group_target.add_option('-T', '--targets', dest='targets', 
                  help='Path to a file containing a list of targets (one per line)')
parser.add_option_group(group_target)

# User Discovery Options
group_users = optparse.OptionGroup(parser, "User Discovery Options")
group_users.add_option('-w', '--wordlist', dest='wordlist', 
                  help='Path to the wordlist file for username enumeration')
group_users.add_option('-u', '--username', dest='username', 
                  help='Check a single username only (e.g., root)')
parser.add_option_group(group_users)

# Configuration Options
group_config = optparse.OptionGroup(parser, "Scanning Configuration")
group_config.add_option('-d', '--delay', dest='delay', type="float", default=0.0, 
                  help='Time to wait between requests in seconds (default: 0.0)')
group_config.add_option('-c', '--command', dest='command', default="VRFY", 
                  help='SMTP method to use: VRFY, EXPN, or RCPT TO (default: VRFY)')
parser.add_option_group(group_config)

# Output Options
group_output = optparse.OptionGroup(parser, "Output Options")

group_output.add_option('-o', '--output', dest='output', 
                  help='Path to save the results to a  txt file')
parser.add_option_group(group_output)


opts, args = parser.parse_args()


if not opts.target and not opts.targets:
    parser.print_help()
    sys.exit(1)

if opts.targets:
    try:
        with open(opts.targets , 'r') as file_target:
            targets = [ line.strip() for line in file_target.readlines() ]
    except FileNotFoundError:
        print(f"{R}[!] Error: Wordlist '{opts.wordlist}' not found.{W}")
        sys.exit(1)


Usermode = "Username" if opts.username and not opts.wordlist else "Wordlist"
Targetmode = " , ".join(targets) if opts.targets else opts.target


print_banner(Targetmode, Usermode, opts.delay, opts.command)

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



def save_output( file_path , usernames : list , target = "" ) -> str:
    with open(file_path  , 'w') as file :
        if target:
            file.write(f"Target: {target}\n\n")
        for username in usernames:
            file.write(f"{username}\n")
        
    
    print(f"{Y}[*] {G}Output {R}Saved {G}Done . ")
    



# Enumeration
def enum_single_target():
    try:
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.settimeout(10) 
        
        print(f"{B}[*]{W} Connecting to target...")
        
        soc.connect((opts.target, 25))
        banner_raw = soc.recv(1024)

        print(f"{B}[*]{W} Scanning {G}{len(usernames_to_check)}{W} entries...\n")

        VALID_Usernames = []

    
        for username in usernames_to_check:
            if opts.delay > 0:
                sleep(opts.delay)
            
            cmd_string = f"{opts.command} {username}\r\n"
            soc.send(cmd_string.encode())
            result = soc.recv(1024).decode(errors='ignore')
            
            if "250" in result or "252" in result:
                VALID_Usernames.append(username)
                print(f"{G}[+]{W} VALID: {Y}{username}{W}")
        
        if opts.output:
            save_output(opts.output, VALID_Usernames )        

    except Exception or KeyboardInterrupt as e:
        print(f"{R}[!] Connection error: {e}{W}")
    finally:
        soc.close()
        print(f"\n{B}[*]{W} Done.")


def enum_targets():
    for target in targets:
        try:
            soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            soc.settimeout(10) 
            
            print(f"{B}[*]{W} Target : {G}{target}")
            print(f"{B}[*]{W} Connecting to target...")
            
            soc.connect((target, 25))
            banner_raw = soc.recv(1024)

            print(f"{B}[*]{W} Scanning {G}{len(usernames_to_check)}{W} entries...\n")            
            
            
            VALID_Usernames = []
            for username in usernames_to_check:
                if opts.delay > 0:
                    sleep(opts.delay)
                
                cmd_string = f"{opts.command} {username}\r\n"
                soc.send(cmd_string.encode())
                result = soc.recv(1024).decode(errors='ignore')
                
                if "250" in result or "252" in result:
                    VALID_Usernames.append(username)
                    print(f"{G}[+]{W} VALID: {Y}{username}{W}")
                    
            if opts.output:
                save_output(opts.output, VALID_Usernames , target )
                
            

        except Exception or KeyboardInterrupt as e:
            print(f"{R}[!] Connection error: {e}{W}")
        finally:
            soc.close()
            print(f"\n{B}[*]{W} Done.\n")
            print(f"{Y}-"*20 )


if __name__ =="__main__":
    if opts.targets:
        enum_targets()   
    else:
        enum_single_target()
        
        