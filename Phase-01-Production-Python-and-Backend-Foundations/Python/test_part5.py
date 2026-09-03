from part5 import hello

def main():
    # test_hello_normally()
    # test_hello_assertively()
    test_hello_assertively_understandable_way()

def test_hello_normally():

    '''
    The below approach takes way more line than
    the actual code. Not very effective
    '''
    if hello("Jayesh") != "hello Jayesh":
        print("Oops! The program expects to print \"hello jayesh\"")

    if hello("jayesh") != "hello jayesh":
        print("Oops! The program expects to print \"hello Jayesh\"")


def test_hello_assertively():
    '''
    It just Asserts, but it doesn't throws error in
    a understable way. Even I can't interpret that.
    '''
    assert hello("Jayesh") == "hello Jayesh"
    assert hello("jayesh krishna") == "hello jayesh krishna" # asserts because I did .title() when I print. Output - "hello Jayesh Krishna"

def test_hello_assertively_understandable_way():
    try:
        assert hello("Jayesh") == "hello Jayesh"
    except AssertionError:
        print(f"I expect an output of \"hello Jayesh\"")

    try:
        assert hello("jayesh krishna") == "hello jayesh krishna" 
    except AssertionError:
        print(f"I expect an output of \"hello jayesh krishna\"")

if __name__ == "__main__":
    main()