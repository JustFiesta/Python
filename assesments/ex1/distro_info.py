#!/usr/bin/env python

import argparse
import subprocess
import sys

"""
Create argument parser for CLI interface
"""
def create_parser():
    parser = argparse.ArgumentParser(description="""Get system information""")
    parser.add_argument('-d',
                        help="Distribution information",
                        action='store_true')
    parser.add_argument('-m',
                        help="Memory information",
                        action='store_true')
    parser.add_argument('-c',
                        help="CPU information",
                        action='store_true')
    parser.add_argument('-u',
                        help="Current user information",
                        action='store_true')
    parser.add_argument('-l',
                        help="Average load",
                        action='store_true')
    parser.add_argument('-i',
                        help="IP addresses",
                        action='store_true')
    
    return parser

# API to execute any command using subprocess.run
def execute_command(command):
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if result.returncode == 0:
        return result.stdout.decode('utf-8').strip()
    else:
        print("Error:", result.stderr.decode('utf-8').strip())  # Wyświetl błąd na stderr
        raise NameError(result.stderr.decode('utf-8').strip())


"""
Show distro information from /etc/os-release
"""
def distro_info():
    try:
        return execute_command('cat /etc/os-release')
    except NameError as e:
        print("Error retriving distribution information")


"""
Show memory information using 'free' command
"""
def memory_info():
    try:
        return execute_command('free -m')
    except NameError as e:
        print("Error retriving memory information")


"""
Show CPU information from /proc/cpuinfo
"""
def cpu_info():
    try:
        lsproc_command = 'ls /proc/cpuinfo | grep -E "[Mm]odel name|[Cc]ore(s)|CPU MHz"'
        
        return execute_command(lsproc_command)
    except NameError as e:
        print("Error retriving CPU information")


"""
Show current user using whoami
"""
def user_info():
    try:
        return execute_command('whoami')
    except NameError as e:
        print("Error retriving user name")


"""
Show avg load using 'uptime'
"""
def load_average():
    avg_load_command = 'uptime | grep load*'

    try:
        return execute_command(avg_load_command)
    except NameError as e:
        print("Error retriving avg load")


"""
Show IP address of all IPv4 interfaces
"""
def ip_addresses():
    ip_command = 'ip address  | grep -E "inet\s"'

    try:
        return execute_command(ip_command)
    except NameError as e:
        print("Error retriving IPv4 information")
    

def main():
    parser = create_parser()
    args = parser.parse_args()

    try:
        # check if any arguments were passed - if not display help
        if all(value is None for value in vars(args).values()):
            parser.print_help()
            sys.exit(0)
        else:
            if args.d:
                print("Distro information:\n" + distro_info())
            if args.m:
                print("Memory information:\n" + memory_info())
            if args.c:
                print("CPU information:\n" + cpu_info())
            if args.u:
                print("User information:\n" + user_info())
            if args.l:
                print("Average load:\n" + load_average())
            if args.i:
                print("IP addresess:\n" + ip_addresses())

        sys.exit(0)

    except subprocess.CalledProcessError as e:
        print("Error executing command:", e)
        sys.exit(1)

    except FileNotFoundError as e:
        print("File not found:", e)
        sys.exit(1)

    except Exception as e:
        print("An unexpected error occurred:", e)
        sys.exit(1)
        
    except NameError as e:
        print("An unexpected error occurred:", e)
        sys.exit(1)


if __name__ == "__main__":
    main()