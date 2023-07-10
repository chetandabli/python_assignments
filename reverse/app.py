def reverse_str(str):
    newstr = ""
    for char in str:
        newstr = char + newstr
    
    print(newstr)

reverse_str("Python is fun")