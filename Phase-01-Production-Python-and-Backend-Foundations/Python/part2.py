# Task - Print Name 3 times

#Pythonic weired way
# print("Jayesh" * 3,sep="\n") # it doesn't print jayesh in new line. as string passsed to print function is "JayeshJayeshJayesh"
# print("Jayesh\n" * 3) # issue = prints one extra line as end='\n' by default
# print("Jayesh\n" * 3,end='') # correct

# While loop
# n=0;
# while n < 3:
#     print("Jayesh")
#     n += 1

#For loop 
# for i in [0,1,2]: # Problem - what if I need to print 1000000 times??
#     print("Jayesh")

# for loop using range
# for _ in range(3):
#     print("Jayesh")

# Task - get input from user and check if the number is greater than 0. then print the name.
# def main():
#     name,n = getInput()
#     # printName(name,n)
#     printName()

# def getInput():
#     name = input("Enter your Name: ")
#     while True:
#         n = int(input("How many times your name should be displayed? "))
#         if n<=0:
#             continue
#         else:
#             return [name,n] # return as list
#             return name, n # return as tuple

# def printName(name="jayesh",n=1):
#     for _ in range(n):
#         print(name)

# main()

#Tuple as dict
# people = ("Jayesh","Latha","Kannan","Suba")
# family = {
#     people: "MSK Family"
# }
# print(family[people])
# print(family[("Jayesh","Latha","Kannan","Suba")])

# list
# family = ["Jayesh","Suba","Latha","Kannan"]

# 1st way
# for member in family:
#     print(member)

# 2nd way - len returs the length of the list by taking the list as an argument
# for i in range(len(family)):
#     print(family[i])

# Dict
# Task - To print who knows what car.
# family = [
#     {"Name": "Kannan", "Location": "Bhavani", "Car": ["Maurthi Alto"]},
#     {"Name": "Balu", "Location": "Bhavani", "Car": ["Mahindra xuv 300"]},
#     {"Name": "Kumar", "Location": "Salem", "Car": ["Kia seltos","Ambasadar"]},
#     {"Name": "Sekar", "Location": "Salem", "Car": ["Hyundai"]}
# ]

# def main():
#     printCars()

# def printCars():
#     for eachFamily in family:
#         print(getName(eachFamily),": ",getCar(eachFamily))

# def getName(oneFamily):
#     return oneFamily["Name"]

# def getCar(oneFamily):
#     return oneFamily["Car"]

# def getLocation(oneFamily):
#     return oneFamily["Location"]

# main()

#Task - to print:
###
###
###

# 1st basic nested loop way
# for _ in range(3):
#     for _ in range(3):
#         print("#",end=' ')
#     print()

# Pythonic way
# for _ in range(3):
#     print("#"*3)

# numbers = {
#     True: "Zero",
#     True: "One",
#     False: "Two",
#     True: "Three"
# }

'''
Explanation:
Python treats True == 1 and False == 0. It keeps replacing as and when it's getting a new value for an existing key
The final dict will look like:
{
    True: "Three",
    False: "Two"
}
'''
# print(numbers[True]) # Prints Three

d = {
    1: "one",
    True: "true"
}

print(d) # Output: {1: 'true'}
# As python treats 1 and True are same, the latest value for the key is updated.

