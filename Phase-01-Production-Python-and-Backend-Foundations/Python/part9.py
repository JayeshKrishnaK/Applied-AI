import argparse

balance = 0 # I cannot so something like global balance = 0 [Sololy global is just to define the scope of a existing variable]

def main():
    # using_set()
    # using_global_constant()
    # print("Balance is",balance)
    # using_typehints()
    # using_argparser()
    # using_unpacking()
    # using_map()
    # using_list_comprehensions()
    # using_filter()
    # using_dict_comprehensions()
    using_enum()
    # using_oneLast()

def oneLast_helper(x):
    for i in range(x):
        yield "sheep"*i

def using_oneLast():
    for s in oneLast_helper(3): # here this function is a generator function object which is a iterable one.
        print(s)

def using_enum():
    family = ["Jayesh","Kannan","Latha","Suba"]
    print(*enumerate(family,start=1))

def using_dict_comprehensions():
   # Task - get the people who's father is "Kannan"
    family = [
        {"name": "Jayesh","father": "Kannan"},
        {"name": "Kannan","father": "Krishnaswamy"},
        {"name": "Latha","father": "Duraiswamy"},
        {"name": "Suba","father": "Kannan"}
    ]

    # list of dictionaries
    '''
    expected output: [{'name': 'Jayesh', 'father': 'Kannan'}, {'name': 'Suba', 'father': 'Kannan'}]
    '''

    # normal way
    # result = []
    # for memebr in family:
    #     if memebr["father"] == "Kannan":
    #         result.append(memebr)
    # print(result)

    #using list comprehension
    # print([member for member in family if member["father"] == "Kannan"])

    # dict comprehensions
    '''
    expected output: {'Jayesh': 'Kannan', 'Suba': 'Kannan'}
    '''
    print({member["name"]: member["father"] for member in family if member["father"] == "Kannan"})

def using_filter():
    '''
    for a picked value, if the functionr return true, then this 
    filter obj gets the value instead of the return value from function
    '''
    family = ["Santhi","Suresh","Jayesh","Latha","Kannan","Ramesh","Suba","Sithiksha"]
    filter_obj = filter(lambda x: x == "Jayesh" or x == "Kannan" or x == "Latha" or x == "Suba", family)
    print(*filter_obj) # Jayesh Latha Kannan Suba

def using_list_comprehensions():
    family = ["Jayesh","Kannan","Latha","Suba"]
    print([member.upper() for member in family]) # ['JAYESH', 'KANNAN', 'LATHA', 'SUBA']

    # using conditonals in list comprehensions
    print([member.upper() for member in family if member=="Jayesh"])
    # print([member.upper() if member=="Jayesh" for member in family]) # error

    # print([member.upper() for member in family if member=="Jayesh" else member.lower()]) # error

    print([member.upper() if member=="Jayesh" else member.lower() for member in family])
    print([
        member.upper() if member=="Jayesh" 
        else member.lower() if member=="Kannan"
        else member.capitalize()
        for member in family
        ])

def square_list(x):
  return x*x

def square_dict(x=0,y=0):
  return x*y

def using_map(): 

    name = ["Jayesh","Krishna"]
    print(list(name))
    print(*name) # print(*name) unpacks it as print("Jayesh","Krishna")

    name = {"fname": "Jayesh", "lname": "Krishna"}
    print(dict(name)) # Out - ['Jayesh', 'Krishna']
    # print(**name) #error - because print function has no named parameter called fname/lname when dict unpacks
    
    mp = map(square_list,[1,2,3])
    print(*mp)

    # error
    # mp = map(square_dict,[{"x":2,"y":2}]) 
    # print(*mp) # square_dict({"x": 2, "y": 2}) - this is what it does

    mp = map(lambda x: square_dict(**x),[{"x":2,"y":2}]) 
    print(*mp)

# def unpack_helper(a,b="1",c="2"):
def unpack_helper(*family,**details):
    '''
    Usual notation:
    Positional parameter - *args
    Named parameter - **kwargs

    Positional args should always be before named args
    *args - unpacks it with comma 
    **kwargs - unpacks it with name 
    '''
    print(type(family)) # tuple
    for name in family:
        print(name)

    print(type(details)) # dict
    for eachDetail in details:
        print(eachDetail,"-",details[eachDetail])
    # print(a,b,c)
    # return a+b+c

def using_unpacking():
    # coins = [1,2,3]
    # print(unpack_helper(*coins))
    # print(unpack_helper(c=5,b=1,a=2))
    # coins = {"a":1,"c":2,"b":3}
    # print(unpack_helper(**coins)) # the exact key should be in arguments of unpack_helper
    unpack_helper("Jayesh","Krishna",birthMonth="August",birthDay=20,birthYear=2002)

def using_argparser():
    parser = argparse.ArgumentParser(description="Prints a name N times")
    parser.add_argument("-n","--number",default="1",help="Speicify number of times to print a name",type=int,dest="n")
    parser.add_argument("--name",default="Jayesh",help="Specify the name",type=str,dest="fname")
    # parser.add_argument("--isFamily",help="Specify if he belong to family or not",type=bool)
    # parser.add_argument("--isFamily",action=argparse.BooleanOptionalAction,help="Specify if he belong to family or not")
    parser.add_argument("--isFamily",action="store_true",help="Specify if he belong to family or not")
    args = parser.parse_args()

    print("outside",args.isFamily)
    if args.isFamily:
        print("inside",args.isFamily)

    # for _ in range(int(args.n)):
    #     print(args.fname)

def using_global_constant():
    global balance # Always should be at the start of the function
    # if not declared global here, then that variable balance will behave as a constant. (only read, no edit)
    print("Balance is",balance)
    balance +=1
    print("Balance is",balance)

def using_typehints() -> None:
    x: int = input("Enter a value for x: ") # Deliberatly caused error
    """
    part9.py:17: error: Incompatible types in assignment (expression has type "str", variable has type "int")  [assignment]
    Found 1 error in 1 file (checked 1 source file) 
    """

    #Docstring
    '''
    Add x, y and print the result.

    :params : None
    :rtype: None
    .. So on.. refer the video of David J Malan Week 9 https://cs50.harvard.edu/python/weeks/9/
    '''
    y: int = int(input("Enter a value for x: "))
    print(x+y)

def using_set():
    family_members = ["jayesh","kannan","latha","kannan","jayesh","suba","suba"]
    unique_family_members = set()

    for member in family_members:
        if member.upper() not in unique_family_members:
            unique_family_members.add(member.upper())

    print(sorted(unique_family_members))

if __name__ == "__main__":
    main()