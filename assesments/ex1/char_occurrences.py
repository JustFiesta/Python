#!/usr/bin/env python

usr_str = str(input("Please input string to process: "))

char_list = list(usr_str)
char_dict = dict.fromkeys(char_list, 0)

for char in char_list:
    if char in char_dict:
        char_dict[char] += 1

print(char_dict)