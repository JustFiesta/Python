#!/usr/bin/env python

import argparse

# create parser and get value for each argument
def create_parser():
    parser = argparse.ArgumentParser(description="""Count user agents in given access.log file""")
    parser.add_argument("file",
                        help="Provide a name to acces.log file",
                        nargs=None,
                        metavar='file')
    
    return parser


def count_user_agents(filename):
    unique_ips = set() 

    with open(filename, "r") as file:
            for line in file:
                ip = line.split()[0] # ip addresses are usually first in acces.log
                unique_ips.add(ip) # sets store unique values - no duplicates allowed

    return len(unique_ips)


def main():
    args = create_parser().parse_args()

    filename = args.file

    # check for correct filetype
    if "access" not in filename.split(".") and "log" not in filename.split("."):
        raise NameError("Wrong filename. Expected: *access.log*")
    else:
        print("Number of user agents: " + str(count_user_agents(filename)))

# check python variable for this module - if correct run main 
if __name__ == "__main__":
    main()