'''
Conditionals
if
elif
else
bool - need use True / False. Captial first letter
match - case_: for default
'''

'''
Questions:
I can pass any huge number to find that it's a odd/even.. unlike c++ here it doesn't have any limit, how does it works?
'''

# name = input("Enter your name: ")

# # Match
# match name:
#     case "Jayesh" | "Latha" | "Kannan" | "Suba":
#         print("MSK family")
#     case _:
#         print("who")

# #if else, elif

# if name == "Suba" or name == "Kannan" or name == "Latha":
#     print("MSK")
# elif name == "Sankar":
#     print("CSK")
# else:
#     print("Who?")

# odd /even

def main():
    x = int(input("Enter a number: "))
    if isEven(x):
        print(f"{x} is even")
    else:
        print(f"{x} is odd")

def isEven(n):
    # return True if n%2 == 0 else False # one liner
    return n%2 == 0  # simple one liner

main()