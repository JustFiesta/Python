#!/usr/bin/env python

def remove_duplicates_from_list(list):
    temp_set = set(list) #removes duplicates

    list = tuple(temp_set)
    return list

list = [2, 5, 7, 3, 2, 44, 420, 7]
print(f"List before: \n{list}")

list = remove_duplicates_from_list(list)
print(f"List after: \n{list}")

print("min: " + str(min(list)))
print("max: " + str(max(list)))