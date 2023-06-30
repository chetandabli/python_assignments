# 1
def pattern():
    x = ""
    for i in range(1, 6):
        x += "{}".format(i)
        print(x)
        x += " "

pattern()

# 2
numbers = [12, 75, 150, 180, 145, 525, 50]
def filter(nums):
    for num in nums:
        if num%5 == 0 and num < 151:
            print(num)

        if num > 501:
            return
        
filter(numbers)

# 3
s1 = "Ault"
s2 = "Kelly"

def placeinmid(s1, s2):
    newstr = ""
    mid = len(s1) // 2
    for i in range(0, mid):
        newstr += s1[i]
    newstr += s2
    for i in range(mid, len(s1)):
        newstr += s1[i]
    print(newstr)

placeinmid(s1, s2)

# 4
str1 = "PyNaTive"
def sort_string(str):
    lowercase = []
    uppercase = []
    
    for char in str:
        if char.islower():
            lowercase.append(char)
        else:
            uppercase.append(char)
    
    sorted_string = ''.join(lowercase + uppercase)
    print(sorted_string)

sort_string(str1)

# 5
list1 = ["M", "na", "i", "Ke"]
list2 = ["y", "me", "s", "lly"]

def con(list1, list2):
    for i in range(len(list1)):
        list1[i] += list2[i]
    print(list1)

con(list1, list2)

# 6
listx1 = ["Hello ", "take "]
listx2 = ["Dear", "Sir"]

def coninner(list1, list2):
    newlist = []
    for i in range(len(list1)):
        for j in range(len(list2)):
            newlist.append(list1[i] + list2[j])
    print(newlist)

coninner(listx1, listx2)

# 7
listnum1 = [10, 20, 30, 40]
listnum2 = [100, 200, 300, 400]

def intra(list1, list2):
    j = len(list2)-1
    for i in range(len(list1)):
        print("{} {}".format(list1[i], list2[j]))
        j -= 1

intra(listnum1, listnum2)

# 8
employees = ['Kelly', 'Emma']
defaults = {"designation": 'Developer', "salary": 8000}

def makeobj(employees, defaults):
    newobj = {}
    for employee in employees:
        newobj[employee] = defaults
    print(newobj)

makeobj(employees, defaults)

# 9
sample_dict = {
    "name": "Kelly",
    "age": 25,
    "salary": 8000,
    "city": "New york"}

# Keys to extract
keys = ["name", "salary"]

def extract(sample_dict, keys):
    newobj = {}
    for key in keys:
        newobj[key] = sample_dict[key]
    print(newobj)

extract(sample_dict, keys)

# 10
tuple1 = (11, [22, 33], 44, 55)

nested_list = list(tuple1)

nested_list[1][0] = 222

tuple1 = tuple(nested_list)

print(tuple1)


