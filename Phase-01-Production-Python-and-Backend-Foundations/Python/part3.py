'''
Questions:
1. Why SyntaxError can't be anticipated? if not, then why it exists just like other error types?
2. How to write exceptions if we don't know error type?
3. In the below block, if try succeeds, x is printed.. if not the below code throws a NameError (x is not defined)
try:
    x = int(input("Enter value for x: "))
except ValueError:
    print("Oops!! x is not a integer")

print(f"Value of x is {x}")

How the scope of x works here?
'''

# line 20 thows NameError if try fails because exception occured before assigining value to x. So x is undefined.
# try:
#     x = int(input("Enter value for x: "))
# except ValueError:
#     print("Oops!! x is not a integer")

# print(f"Value of x is {x}")

# To overcome above problem we use else which gets executed only if try succeeds
# try:
#     x = int(input("Enter value for x: "))
# except ValueError:
#     print("Oops!! x is not a integer")
# else:
#     print(f"Value of x is {x}")

#Reprompting until try succeeds.
# while True:
#     try:
#         x = int(input("Enter value for x: "))
#     except ValueError:
#         print("Oops!! x is not a integer")
#     else:
#         break # instead of else , we can introduce break at end of try block.

# usage of pass and abstraction and simplification of lines of code

# def main():
#     x = get_int()
#     print(f"value of x is {x}")

# def get_int():
#     while True:
#         try:
#             return int(input("Enter value for x: "))
#         except ValueError:
#             #print("Oops!! x is not a integer")
#             pass

# main()

# raise - to delibreately raise an exception
# try:
#     x = int(input("Enter value for x: "))
# except ValueError:
#     print("Invalid input")
#     raise # Halts execution by throwing the exception being caught

# raising an exception
age = int(input("Enter age: "))
if age < 18:
    raise ValueError("Your are not adult") # Rasing an existing exception with our own message.