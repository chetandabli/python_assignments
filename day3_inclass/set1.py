# 1
print("Hello World!")

# 2
num = 1
float = 3.14
str = "chetan"
bool = True
citis = ["mumbai", "delhi", "bengaluru"]
tupleexample = ("hm", "hey", "hello", "hii")
dictory = {
    "name": "chetan",
    "city": "bengaluru"
}
setexa = {1, 5, 55, 56}

# 3
def listcreate():
    listofnums = []
    for i in range(1, 11):
        listofnums.append(i)
    print(listofnums)
    return listofnums

listfun = listcreate()
listfun.pop(-3)
print(listfun)
listfun.append(5)
print(listfun)
listfun.append(4)
print(listfun)
listfun.sort()
print(listfun)

# 4
def find_sum_avg(list):
    sum = 0
    for nums in list:
        sum += nums
    print("Sum: {} Average: {}".format(sum, round(sum/len(list), 2)))

find_sum_avg(listfun)

# 5
def strreverse(str):
    newstr = ""
    for i in reversed(range(0, len(str))):
        newstr += str[i]
    print(newstr)

strreverse("chetan")

# 6
def countvow(str):
    count = 0
    for i in range(len(str)):
        if str[i] == "a" or str[i] == "e" or str[i] == "i" or str[i] == "o" or str[i] == "u":
            count += 1
    print("Number of vowels: {}".format(count))

countvow("chetan")     

# 7
def is_prime(number):
    if number < 2:
        print("{} is not a prime number.".format(number))
        return
    for i in range(2, int(number**0.5) + 1):
        if number % i == 0:
            print("{} is not a prime number.".format(number))
            return
    print("{} is a prime number.".format(number))

is_prime(4)

# 8
def factorial(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    print("The factorial of {} is: {}".format(n, result))

factorial(10)

# 9
def fibonacci(n):
    sequence = []
    if n >= 1:
        sequence.append(0)
    if n >= 2:
        sequence.append(1)
    for i in range(2, n):
        next_num = sequence[i - 1] + sequence[i - 2]
        sequence.append(next_num)
    print(sequence)

fibonacci(15)

# 10
def listseq():
    sequence = []
    for x in range(1, 11):
        sequence.append(x ** 2)
    print(sequence)

listseq()





