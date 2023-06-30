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
def addsum(list, k):
    for i in range(0, len(list)):
        for j in range(i+1, len(list)):
            if (list[i] + list[j]) == k:
                print(i, j)

addsum([2, 7, 11, 15], 9)

# 4
def is_palindrome(word):
    for i in range(len(word)//2):
        if word[i] != word[-i-1]:
            print("The word {} is not a palindrome.".format(word))
            return
    print("The word {} is not a palindrome.".format(word))

is_palindrome("word")

# 5
def selection(arr):
    n = len(arr)
    
    for i in range(n):
        min_idx = i
        
        for j in range(i+1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    
    print(arr)

selection([64, 25, 12, 22, 11])

# 6
from queue import Queue

class Stack:
    def __init__(self):
        self.queue = Queue()

    def push(self, value):
        # Move all elements from the main queue to a temporary queue
        temp_queue = Queue()
        while not self.queue.empty():
            temp_queue.put(self.queue.get())

        # Add the new value to the main queue
        self.queue.put(value)

        # Move the elements back from the temporary queue to the main queue
        while not temp_queue.empty():
            self.queue.put(temp_queue.get())

    def pop(self):
        if self.queue.empty():
            return None
        return self.queue.get()

stack = Stack()
output = []

stack.push(1)
output.append(str(stack.pop()))

stack.push(2)
output.append(str(stack.pop()))

stack.push(3)
output.append(str(stack.pop()))
output.append(str(stack.pop()))
output.append(str(stack.pop()))

result = ", ".join(output)
print(result)

# 7
def fizzBizz():
    str = ""
    for i in range(1, 100):
        if i%3 == 0 and i%5 ==0:
            str += "FizzBizz, "
        elif i%3 == 0 and i%5 != 0:
            str += "Fizz, "
        elif i%3 != 0 and i%5 == 0:
            str += "Bizz, "
        else:
            str += "{}, ".format(i)
    str += "{}".format(100)
    print(str)

fizzBizz()

# 8
