import os
from dotenv import load_dotenv

load_dotenv()

'''
Although I used "" only for Name. it treates both NAME and AGE as string
'''
print(os.environ["AGE"])
print(os.environ["NAME"])

print(os.environ["PATH"])
print(os.getenv("DEBUG","Nothing"))