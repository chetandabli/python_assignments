# 1
listoftuple = [("John", 25), ("Jane", 30)]

def itrate(list):
    output = ""
    for tup in list:
        output += "{} is {} years old. ".format(tup[0], tup[1])
    print(output)

itrate(listoftuple)

# 2
obj = {
    "John": 26
}

def update(name, age):
    obj[name] = age

update("chetan", 23)
print(obj)

# 3
def addsum(list):
    for i in len:
        for()