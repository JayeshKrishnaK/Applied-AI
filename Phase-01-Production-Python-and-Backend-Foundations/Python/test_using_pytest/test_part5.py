from hello import hello
import pytest

def hi():
    print("I should not be run by pytest")
    assert False
    '''
    it as expected ignored this function and hello.py inside this folder.
    '''

def test_hello_default():
    assert hello() == "hello Jayesh"

def test_hello_simple():
    assert hello("jayesh") == "hello Jayesh"

def test_hello_complex():
    assert hello("jayesh krishna") == "hello Jayesh Krishna"

def test_hello_assertion():
    with pytest.raises(AttributeError):
        hello(2)
