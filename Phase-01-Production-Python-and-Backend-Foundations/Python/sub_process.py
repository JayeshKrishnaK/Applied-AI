import subprocess
import os
import sys
import time

def process_other_options():
    # To pass input from terminal
    result = subprocess.run(
                ["python","-c","print(input().upper())"],
                input="Jayesh\n",
                capture_output=True,
                text=True
                )
    print(result.stdout)

    # To set a timeout
    try:
        subprocess.run(
            "timeout 5",
            shell=True,
            timeout=4
        )
    except subprocess.TimeoutExpired as e:
        # raise e
        print("OOPS!! TImeout expired for timeout :)")
        '''
        O/P: Waiting for 1OOPS!! TImeout expired for timeout :)
        why?
        Our cursor(|): Waiting for  2| seconds, press a key to continue ...
        It redraws the same line using carriage returns (\r), so the number changes from 5 to 4 to 3 
        and so on, all on one line and without a newline until it finishes.
        '''

    #cwd - To execute the program from the path we give, 
    #env -> to start a process with the env variables we give
    '''
    by default the process we start gets all the env variables we have in our main program
    '''
    print()
    env = os.environ.copy()
    env["NAME"] = "JAYESH KRISHNA"
    result = subprocess.run(
        "echo %NAME%",
        capture_output=True,
        text=True,
        shell=True,
        cwd="C:\\Users\\2019j\\OneDrive\\Documents\\Applied-AI\\Phase-01-Production-Python-and-Backend-Foundations\\Python",
        env=env
    )
    print(result.stdout)

    # TO run another python script by the same interpreter which runs this main program
    # Here we didn't lauch a new python program. sys.executable contains full path of py interpreter
    subprocess.run(
        [sys.executable,"debug.py"]
    )


def process_basics():
    '''
    run() args:
    -> The first arg is a list and in that list the first value tells the program name and rest all
       it's arguments
    -> capture_output=True -> output of the program we gave is piped out to stdout and not to terminal
       similarly error as well to stderr
    -> text=True -> stdout will now have UTF-8 decoded string instead of raw byte

    What does run() return?
    -> CompleteProcess object
    -> eg: CompletedProcess(args=['git', 'stattus'], returncode=1, stdout='', stderr="git: 'stattus' 
       is not a git command. See 'git --help'.\\n\\nThe most similar command is\\n\\tstatus\\n")

    What if the program doesn't exists?
    -> FileNotFoundError exception object is thrown from run().
    -> eg: ["gi","status"] -> Here there is no program called "gi" can be found on my pc. So
       the process not at all created and run() throws FIleNotFoundError exception

    What if program exists but it fails?
    -> Depdens on check=True/False (False is default) argument in run()
    -> if check=False and our program fails:
          It silently ignores. stdout will be empty stderr will have the error message from our program
    -> if check=true and our program fails:
          It throws a CalledProcessError exception. Which we can use try/execpt to handle it.

    Attributes of run:
    -> stdout - output of process
    -> stdin - input to be given to the program
    -> return_code - 0 if sucess, if any other value, then that means failure
    -> stderr - error from the program
    
    RAW BYTE:
    - A byte has 8 bits
    -> By default, the process outputs the data (error/output/anything) in raw bytes (0's and 1's)
    -> Python by default convertes binary represented output from process to decimal
       (eg: 'H' -> 72)
    -> This representation is then put it into bytes object (it starts with "b'" to denote its a byte not a string)
    -> The __str__ method in byte object does convert the decimal representation to a human readable
       text using ASCII rule book.
    -> by specifying "text=True" as one of args to run() or result.stdout.decode('UTF-8') we get
       human readable string
    '''
    try:
        result = subprocess.run(
            ["git","status"],
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e: # Note exception exists inside the subprocess
        # As check is set to True, CompletedProcess object is not stored to result, as run() didn't
        # return and instead it throwed an exception. So there is no variable called result here.
        raise e
    except FileNotFoundError as e:
        raise e
    else:
        print(result.stdout)
        # print(result.stdout.decode('UTF-8')) # type = byte object if not text=True included in run()

    
    print("****************************************")
    
    #shell = True -> refer note
    result = subprocess.run("dir",shell=True,capture_output=True)
    print(result.stdout.decode('UTF-8'))

def subprocess_popen():
    p = subprocess.Popen(
        "timeout 5",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    # p.poll() # non-blocking 
    '''
    poll()
        -> Non Blocking.
        -> If process still running, it returns None immdiately
        -> If process compeleted, it gonna check and update the popen obj and return the returncode
    wait()
        -> blocking
        -> if process is running, it waits for it to finish there by blocking main process. 
           Once done, update popen object and return the return code
        -> if process completed, it returns its returncode immediately
    '''
    # print(p.wait()) # blocking
    print(p.poll()) # None obj - as the process is still running
    print(p.returncode) # None obj - as still running
    print(p.stdout) # Buffer Reader obj, similar to file object
    stdout, stderr = p.communicate()
    print(stdout.decode('UTF-8'))
    print(p.poll()) # 0 as process completed successfully
    print(p.returncode) # 0 as process completed successfully
    # print(p.stdout.read().decode('UTF-8'))

if __name__ == "__main__":
    # process_basics()
    # process_other_options()
    subprocess_popen()

'''
********threads with subprocess********

from concurrent.futures import ThreadPoolExecutor

def run_cmd(cmd):
    return subprocess.run(cmd, capture_output=True, text=True).stdout

cmds = [["python", "--version"], ["git", "--version"], ["uv", "--version"]]

with ThreadPoolExecutor(max_workers=3) as executor:
    outputs = list(executor.map(run_cmd, cmds))

**********aysncio with subprocess***********

import asyncio

async def run_cmd(*args):
    proc = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE
    )
    stdout, _ = await proc.communicate()
    return stdout.decode()

async def main():
    results = await asyncio.gather(
        run_cmd("python", "--version"),
        run_cmd("git", "--version"),
    )
    print(results)

asyncio.run(main())

***********Comparision over all 4********** (refer clause AI)

	asyncio	threading	multiprocessing	subprocess
Runs	coroutines	Python functions in threads	Python functions in processes	external programs
Best for	I/O waiting	I/O waiting	CPU-heavy Python code	using tools outside Python
Multiple cores	No	No (GIL)	Yes	Yes (separate processes)
Memory shared with your code	Yes	Yes	No	No
How you get data back	return values	shared variables	Pool.map, queues	stdout/stderr text and return code
Main hazard	blocking the loop	race conditions	passing data around	shell injection, silent failures
'''