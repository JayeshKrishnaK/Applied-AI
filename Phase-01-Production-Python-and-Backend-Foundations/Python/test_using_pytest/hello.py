def main():
    name = input("Please enter your name: ")
    print(hello(name))

def hello(name="Jayesh"):
    return f"hello {name.title()}" 
    '''
    I avoided side effect here by not printing inside the function itself.
    if I had done, then I wouldn't be able to test it via pytest.
    '''

if __name__ == "__main__":
    main()