# Basics
'''
print function
parameters, arguments
positional,named parameters using print function
formated string
Escape sequence
string concatenation
string methods - strip, captitalize,title,split
Clubing mutiple methods together
interactive mode - execute one line of code at a time.
integer - input() always returns a string. The user entered value is always treated as string although he entered a number.
int() - what ever argument is passed, convert it to integer.
Nesting one function inside another. return value of innner fn is argument of another
flaot() - similar to int, it converts the given string to float
round() - round the floating point to nearest integer. Takes an optional parameter which decides how many numbers to be there after decimal.
Expressing numbers using format string :
   - eg: 1000 can be represented as 1,000 for redability f"{z:,}"
   - eg: 0.66666 can be rounded to 0.67 w/o round() function. f"{z:.2f}"
Defining a function and convention of using main
2*3 - multiply, 2**3 -> 2^3, pow(2,3) = 2**3
'''

'''
Questions:
int() - what if our argument is not a number?
'''

# strings

'''
# print("hello")
name = ""
# name = input("Enter your name: ")
# print("hello",name,sep='  ',end=' ')
# print(name)

# Remove white spaces at beginning and end.
name = name.strip()

#Captitalize - Make the first letter of first word in a sentence captial
name = name.capitalize()

#title - captitalize every first letter of word in a sentence
name = name.title()

# In a single line
name = input("Enter your name: ").strip().title()


#Spliting the string into multiple substrings by what ever separation we want
fname, lname = name.split(" ") # Gonna return a squence of strings

print(f"Hello \"{fname}\"")

'''

# int

# The below concatenate x and y
# x = input("Enter a number for variable x: ")
# y = input("Enter a number for variable y: ")

#type conversion and nesting of functions
# x = int(input("Enter a number for variable x: "))
# y = int(input("Enter a number for variable y: "))
# print(x+y)

def main():
    name = input("What's your name? ")
    hello(name)

def hello(to="World"):
    return print(f"hello {to}")

main()