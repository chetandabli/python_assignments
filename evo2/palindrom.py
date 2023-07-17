
def palindrome(n):
    new_num = str(n)
    new_rev_num = new_num[::-1]

    if new_num == new_rev_num:
        return True
    else:
        return False
    
print(palindrome(141))