import difflib

with open("pre-file", "r") as left, open("post-file", "r") as right:
    
    differences = difflib.unified_diff(left.readlines(), right.readlines())
        
    for difference in differences:  # difference is empty if no differences
        print(difference)