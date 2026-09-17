import argparse

balance = 0 # I cannot so something like global balance = 0 [Sololy global is just to define the scope of a existing variable]

def main():
    # using_set()
    # using_global_constant()
    # print("Balance is",balance)
    # using_typehints()
    # using_argparser()
    using_unpacking()

def unpack_helper(a,b="1",c="2"):
    print(a,b,c)
    return a+b+c

def using_unpacking():
    # coins = [1,2,3]
    # print(unpack_helper(*coins))
    coins = {"a":1,"c":2,"b":3}
    # print(unpack_helper(c=5,b=1,a=2))
    # print(unpack_helper(**coins))

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