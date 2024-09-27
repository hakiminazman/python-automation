import difflib

with open("rpintbgr5w-0314-001-pre_logs_14_22-4-2022.txt", "r") as left, open("rpintbgr5w-0314-001-post_logs_14_22-4-2022.txt", "r") as right:
    
    differences = difflib.unified_diff(left.readlines(), right.readlines())
        
    for difference in differences:  # difference is empty if no differences
        print(difference)