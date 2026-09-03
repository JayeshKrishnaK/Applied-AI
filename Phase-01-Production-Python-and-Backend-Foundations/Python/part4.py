'''
Questions:
1. D/B modules and library and packages
2. What is namespace?? does that exists in python?
'''

# import modules
# from random import choice
# import statistics
# import sys
# import cowsay

#Random module

#choice method
# coin = random.choice(["head","tail"])
# coin = choice(["head","tail"])
# print(coin)

#randint
# number = random.randint(1,10)
# print(number)

#Shuffle
# cards = ["jack","king","queen"]
# random.shuffle(cards)
# print(cards)

#statistics module

#mean - to caluclate avgerage
# print(statistics.mean([95,95,95,99,100]),"%",sep='')

#sys module

#argv - to get input from command line
# print("My name is",sys.argv[1])

# What if user forgets to enter - we need exit using exit()
# if len(sys.argv) < 2:
#     sys.exit("Too few arguments")
# elif len(sys.argv) > 2:
#     sys.exit("Too many arguments")

# print("My name is",sys.argv[1])

# We can also pass multiple names and access them using index
#slice - to trim the list as per our wish
# if len(sys.argv) < 2:
#     sys.exit("Too few arguments")

# for arg in sys.argv[1:]:
#     print("My name is",arg)

# Getting the value from command line with options

# if sys.argv[1] == "--name":
#     print(sys.argv[2])

# cowsay package
# cowsay.trex("hello")

# Calling my own package Calculate

#Assuming no __init__.py

# fails
# import calculate
# calculate.add.add(2,3)

# pass
# import calculate.add
# print(calculate.add.add(2,3))

# fails
# import calculate.add.add
# print(calculate.add.add(2,3))


# from calculate import add
# print(calculate.add.add(2,3)) #fails
# print(add.add(2,3)) # pass

# from calculate.add import add
# print(calculate.add.add(2,3)) #fails
# print(add.add(2,3)) # fails
# print(add(2,3)) # pass

# fails
# from calculate import add.add  

# Assuming I have __init__.py with conetnts:
# from . import add
# from . import sub

# pass
# import calculate
# print(calculate.add.add(2,3))

# pass
# import calculate.add
# print(calculate.add.add(2,3))

# fails
# import calculate.add.add
# print(calculate.add.add(2,3))

# pass
# from calculate import add
# print(add.add(2,3))

# pass
# from calculate.add import add
# print(add(2,3))

# Assuming I have __init__.py with conetnts:
# from .add import add
# from .sub import sub

# pass
# import calculate
# print(calculate.add(2,3))

# import calculate.add
# print(calculate.add.add(2,3)) # fail
# print(calculate.add(2,3)) # pass

# from calculate import add
# print(add(2,3)) #pass

# from calculate.add import add
# print(add(2,3)) # pass

import requests
import json
response = requests.get("https://itunes.apple.com/search?entity=song&limit=1&term=arrahman")
# the above returns the reponse object
# print(response) #prints the response object
# print(response.headers)
# print(response.text) # JSON Format (text) -> this is what the server returns.
# print(response.json()) -> returns the data as a python dictionary
print(json.dumps(response.json(), indent=2)) # takes takes dict as input and output as text
# print(json.loads(response.text)) # takes input as text and output as dict