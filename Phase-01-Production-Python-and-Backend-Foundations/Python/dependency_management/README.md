### Dependency Management

1. Creating env

**pip way**

python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass (need to check what this means)
.\.venv\Scripts\activate.ps1
deactivate

**uv way**

uv venv
\.venv\Scripts\activate - activate it and we can run as usual (python hello.py)
uv run hello.py(not recommended) - it finds the venv from the pyproject.toml and runs, if there is no toml file then it arbitarily cheks all over the parent folders and uses it. (unexplanatory behaviour)


2. Initializing a project so it can be tracked by uv

uv init --bare -> it creates a bare minimum setup in our project so it can be used by uv for managing dependencies. ie., we can add/remove packages

it creats
* pyproject.toml:

[project]
name = "dependency-management"
version = "0.1.0"
requires-python = ">=3.14"
dependencies = [] # contains direct dependencies

* uv.lock(lock file) - contains the exact dependency version. Both direct and transitive 

******* These files are updated when we add/remove/modify dependencies*********
 
3. Add & remove a dependency

**pip way**

pip install requests
if already we have requests and we can use --force-reinstall
pip uninstall requests

* pip no where updates the dependencies and its version.

**uv way**

uv add requests
uv remove requests 

*  Ensure we haven't open uv.lock anywhere, if opened it will throw os error as the 
   transitive dependency of the package we install would have been opened through uv.lock
   
*  uv automatically updates the pyproject.toml and uv.lock. 'pip' doesn't update anywhere. if needed we 
   can view the list of dependencies in our env by using "pip freeeze"
   
*  pip freeze > requirements.txt -  via pip to copy the dependencies used by our project.

*  if need to run on any python environment, we can just "pip install -r requirements.txt"

4. How running our project elsewhere becomes easy?

***pip way****

While pushing our project to git, we push code, requirements.txt
clone our project from git
create a env
pip install -r requirements.txt

***uv way***
We push code,pyproject.toml,uv.lock. We dont push the .venv
clone from git
run "uv sync" - uv will look into uv.lock and create a .venv with the packages mentioned in our uv.lock

5. dev dependencies

Not all dependencies are needed all the time. Big projects may use n number of dependencies.
Suppose a user is just going to run the project and no development activities was planned, then
it's a pkg called pytest doesn't need to be there in his venv.

To separate runtime and dev dependencies we have:

****pip way****

pip freeze -r requirements-dev.txt [Not a ideal way, cause freeze puts all dependencies we have currently and manually we need to remove them here]

****uv way****

To overcome drawback of pip, uv create a separate section called [dependency-groups] 
and we create a key which of list type. it contains all dependencies needed for development. 
Runtime dependencies are present in dependencies list under [project] section.
cmd: uv add --dev pytests [The above said is done automatically for us if we use "--dev"]


# Packaging

*Important* - once the folder is initilaized by uv with --bare, then it can't be initialized again with --package or any other. We need to manually update the toml file inorder to make it as package.

Initial project structure:

sample2/hello.py

hello.py

import requests
print("hello from sample2/hello.py")

1. Initialize uv

uv init --package

The above command alters the folder structure as:

sample2/
├── hello.py                  <- loose file, not part of the package
├── pyproject.toml
└── src/
    └── sample2/
        └── __init__.py       <- the package

*Note*: A file sitting next to pyproject.toml is just a loose script: it isn't in the wheel, and import hello won't work once your project is installed by someone.

2. Explanation of contents in pyproject.toml

[project.scripts]
sample2 = "sample2:main"

[build-system]
requires = ["uv_build>=0.12.4,<0.13.0"]
build-backend = "uv_build"

[project.scripts] - its a table under which we specify a key value pair:
key - terminal command to be ran
value - "module/package/package.module:main"

*Note*: a package is also a module when imported it runs its __init__.py file.

In our case, it runs sample2/__init__.py and under the file it calls main() function when we run "sample2" on our terminal after installing the wheel file/ package (if uploaded to pyPI).

[build-system] - it specifies which module is responsible for building our project. Its specified in 'build-backend' key. We have another key called 'requires' which tells what dependencies our build-backend module needs.

In our case uv_build is the module and it needs to be present in the environment we are building.

3. Making hello part of the package sample2

Move hello.py from sample2/ to sample2/src/sample2 and its now part of sample2 package.

Now to print the message we have:

*Important* - Code that runs from a command should live in a function, because top-level print(...) runs at import time (the moment anything imports the file). So change hello.py to:

import requests

def main():
    print("Hello from sample/hello.py")

and the [project.scripts] is now updated to "sample2.hello:main"

4. Make sure our pyproject.toml contains all runtime dependencies.

After our initialization, the dependencies variable under [projects] table will be empty. So add the requests by running "uv add requests"

Now we have all set to build our project to generate the whl file.

5. Building

uv build - this command creates a folder called dist/ which will be present in the same folder which hosts our .venv/

It has whl file and zip file. The whl file can be shared to anyone and once installed, two things happen:

* Their own python/lib/site-packages will now have the package we created

sample2/
    __init__.py
    hello.py

* Terminal command. under python/Scripts we will be having sample.exe

6. Using our package

* Importing our package

from sample2.hello import main
main()

Output:
Hello from sample/hello.py

* Running cmd on terminal

sample

if "sample2.hello:main"
Output:
Hello from sample/hello.py

if "sample2.main"
output:
Hello from sample2!


******Important************

uv init --package only creates a skeleton. if our folder has multiple folder eg: sample/hello/hello.py and sample/bye/bye.py, then we need to move them to src/sample in order to make it a part of sample package.

By default when we initialize the folder as a package, it creates:
1. src/sample
2. sample folder will also be created in site-packages, where it doesn't have any content but a pointer poiting to the src/sample. So it behaves as if I installed it. This is called as editable install. So every time we dont need to build and install the wheel. 
3. The terminal command too referenced to toml file. say-hello.exe/__main__.py where the main file contents is essentially tracked by say-hello variable updates in toml file.