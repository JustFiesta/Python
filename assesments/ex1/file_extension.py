#!/usr/bin/env python

def get_file_extention(filename):

    extension = filename.split(".")

    if len(extension) < 2:
        raise NameError("Filename does not contain extension")
    else:
        return extension[-1]
    

usr_input = input("Please provide filename: ")
extension = get_file_extention(usr_input)

print(f"Extension is: {extension}")
