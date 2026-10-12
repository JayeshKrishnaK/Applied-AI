from multiprocessing import Process, Pool, Array, Value, Queue, Lock
import time

flag = 0
exception = ""

def countup(n,m): # m - just to showcase multiple arguments
    '''
    What this function does?
    - Just prints number from [0,n).
    - m is a dummy parameter used to illustrate on how to pass multiple args to a function via pool
    objects methods.

    Why this function?
    - It's going to be the task that we going to assign it to processes we created via Pool.

    Misc:
    print(f"{i} ",end="") 
    . This is will print whole output after 1*4 (if n=4) seconds,
    . because end="" makes print to accunulate it instead of flushing out to console.
    . As we have print() in line 11 it ouputs over there. Can we verified by:

    print("Jk",end="")
    print()
    time.sleep(4)
    print("Jk",end="")

    print("Jk",end="")
    time.sleep(4)
    print()
    print("Jk",end="")
    '''
    for i in range(n):
        print(f'{i} ')
        time.sleep(1)
    print()
    return "Hi"

def countupWrapper(args):
    return countup(*args)

def resultOnSuccess(out):
    print(f"{out} from usingPool function and our result succeded :) P𝗲𝗿𝗳𝗲𝗰𝘁!🎀")

def resultOnFailure(out):
    global flag, exception
    flag = 1
    exception = out
    # raise AttributeError(f"{out} and I'm from usingPool function and our result failed :( 🤕")
    print(f"{out} and I'm from usingPool function and our result failed :( 🤕")

def usingPoolMap(pool):
    ''' 
    How it works?
    - 1st argument - targeted task(Not a named parameter, it's positional). A function
    - 2nd Argument - A tuple with each value referring to argument for one function call.
      example: pool.map(countup,(1,2,3)) -> countup(1) countup(2) countup(3)
    - It works best when our target has only one argument. if multiple arguments exists there are
      two options: 1. Using a wrapper function 2. starmap
    - It internally assigns each target to a process we created as a task to them. Our main program
      waits at the function call(pool.map()) untill all process are executed.

    What it returns?
    - A list with each value containing the return value of our target for each of the arguments we provided.

    Multiple arguments scenario explanation:
    - We pass as a list of tuple.
    - The wrapper function will get tuple and while passing it to our original target it unpacks it.

    Drawback:
    - We need to use wrapper for multiple arguments. - solution: starmap
    - Outputs the results only after all tasks execution are done. If a process finishes a task faster
      and we have its return value, then we can't get that return value
      untill are tasks we created has finished. - solution: imap,imap_unordered,apply_async
    '''
    p1 = pool.map(countupWrapper,[(2,3),(3,2)])
    print(p1) #list

def usingPoolStarMap(pool):
    '''
    How it works?
    - Same as map, but it has capability to unpack tuple and pass it as positional values to our
      target function without a wrapper.
    
    What it retunrs? , Drawbacks
    - same as map
    '''
    p1 = pool.starmap(countup,[(2,3),(3,2)])
    print(p1)

def usingPoolIMap(pool):
    '''
    How it works? , What it returns?
    - Once we call the function, it immdidately dispatches tasks we want to the processes and didn't
      wait for them to complete unlike map().
    - The process are executing the tasks at background and it keeps on updating the return values
      to a list.
    - It returns a iterator object.
    - usually next() in normal(not pool.map()) will call function and execute them and we get 
      return value of that function as a out of next(itr_obj), but here the target function is 
      already running as processes. So what we get in next()?
    - IMap works on ordered manner - example:
        pool.imap(countUpWrapper,[(100,3),(2,2)])
        1st task - countWrapper((100,3))
        2nd task - countWrapper((2,2))
       Here the first task is gonna take significantly more time than 2nd task. So when we call next(p1)
       for first time, it will wait untill all of the execution is compelted for 1st task and the process 
       gonna update the list present in Pool.py (our module/class) and the next(p1) is gonna read them
    - So our main program is haulted untill the countWrapper([100,3]) finishes.

    What if we don't use close() and join() and why it is used?
    - It will cause OS handle error stating we didn't handle the closure of process we created.
    - OS expects the ownder who created the process to handle the cleanup as well. In map() its done
      by that method itself for us.
    - close() - Closes the gate. We can't submit any new tasks to existsing process.
    - join() - Haults the main untill all processes completes its execution.
    - terminate() - Abrubtly closing all in-progress and queueed tasks.

    Usage of with:

    '''
    p1 = pool.imap(countupWrapper,[(5,3),(2,2)])
    print(p1) # Iterator
    for itr in p1:
        print(itr)
    pool.close()
    pool.join()

def usingPoolIMapUnordered(pool):
    '''
    How it works? What it returns?
    - All same as imap(), but here the next(p1) won't wait on tasks in ordered way.
    - it prints the return value as and when process finishes and updates the list in pool.py
    - So we get result in unordered way purely depends on who finishes first.
    '''
    p1 = pool.imap_unordered(countupWrapper,[(5,3),(2,2)])
    print(p1) # Iterator
    for itr in p1:
        print(itr)
    pool.close()
    pool.join()

def usingPoolApplyAsync(pool):
    '''
    How it works? , How it differs from rest of all? , What it returns?
    - 1st arg - A positional argument - target function.
    - 2nd arg - A named argument (args) - paramters. Note: Each value corresponds to each paramter
      in function. Unlike others it does not represent differnt tasks here.
    - 3rd arg - a named argument (callback) - called by the thread (explained later) upon successfull
      completion of a task. We decide what to call once our process succeds. It's a function.
    - 4th arg - a named argument (error_callback) - again called by thread. Called up on successfull failure
      of the task.

    - It returns a ApplyResult Object immdidately after assigning tasks to processes. The proceses works
      on them in background.
    
    _handle_results_ thread:
    - This thread is created by Pool class which sits inside a loop and keeps on monitoring
      all the process running. It's duty is to call callback upon success and error_callback up on
      failure.
    - pool.join() and pool.close() actively waiting up on this thread to complete monitoring
      successfully and report them once all processes are done and dusted.

    deadlock:
    - In error_callback we decide to raise the Exception object received.
    - Upon doing this, kills the thread that monitors the processes which then makes a deadloack as
      our join() and close() will be waiting on a thread that had already died.

    Best way to handle the exception:
    - The thread uses IPC (Inter Process Communication) and gets the traceback data as strings and
      wraps them inside a Exception object and passes that object as a parameter to callback.
    - This thread also adds it to __cause__ of the Exception object, so when we raise the exception,
      we can view the traceback of why our task is failed.
    - As rasising in error_callback causes deadlock, We can  have a flag and get to know that process
      is failed.
    - Once all processes are cleanup, we can read the flag and raise exception.

    The above exception was the direct cause of the following exception.....:
    - As __cause__ already has one exception that was created by thread, When we raise the exception
      object we got, it's treated as a chain of exceptions by python.

    ****** Remove one parameter in countup and create the failing scenario ******
    '''
    # for args in ([(10,2),[2,2]]):
    #     p1 = pool.apply_async(countup,args,callback=resultOnSuccess,error_callback=resultOnFailure)
    p1 = pool.apply_async(countup,args=(2,"j"),callback=resultOnSuccess,error_callback=resultOnFailure)
    # print(p1.get()) # This ApplyResult Object has a get() function if any exception was noticed from a process by _handle_results_ thread
    pool.close()
    pool.join()
    # Notice the order. Only after closing the processes, we are checking for exception.
    # if flag == 1:
    #     print(type(exception))
    #     raise exception

def using_apply(pool):
    '''
    What it is?
    - The synchronous version of apply_async.
    - Once assigned tasks to a process, it waits there untill its done (haulting main). Unlike apply_async
      it doesn't return a ApplyResult object and move on with next lines of code in main.
    - Has no callback,error_callback as apply_async

    return value:
    - As and when once task is done, we get's its return value.
    '''
    for args in [(2,10), (3,20), (4,30)]:
        result = pool.apply(countup, args)   # waits here each time
        print(result)

def usingPool():
    '''
    Purpose:
    - To avoid complexity in tracking multiple processes. Here we define number of processes
    that are going to be created prior and we assign tasks to them later.
    - We can execute a task(function) multiple times by just one line. Unlike Process class we don't
    need to specify multiple times.
    - It has various methods - map.imap,imap_unordered,apply_async

    Overview of Pool:
    - It's a class. Pool(processes=3) returns a object of class Pool. Above mentioned functions
    are methods of this class.
    '''
    pool = Pool(processes=3)

    #using map
    # usingPoolMap(pool)

    #using starmap
    # usingPoolStarMap(pool)

    #using imap
    # usingPoolIMap(pool)

    #using imap_unordered
    # usingPoolIMapUnordered(pool)

    #using apply_async
    # usingPoolApplyAsync(pool)

    #using apply
    using_apply(pool)

def usingProcess():
    p1 = Process(target=countup,args=(5,))
    p2 = Process(target=countup,args=(10,))

    p1.start()
    time.sleep(5) # Im deliberatly starting process after 5 second delay. So output will now be mixed up.
    p2.start()

    p1.join()
    p2.join()

    print("The End!")

result = []

def append_numbers(n,arr,val,q):
    global result # if we dont include this python will create a new local variable inside this function
    i=0
    for no in n:
        # result.append(i)
        arr[i] = no
        i=i+1
    val.value = 10.9 # note we are accessing via .value
    q.put("Jayesh")
    q.put(2)

def interprocessDataSharing():
    '''
    - These data exists in a comman memory space between processes.
    - Sharing data between processes.
    - value - it's "v.value" not just v
    - array - unlike normal array/list it doesn't have append
    - queue - It's similar to normal queue. Only differenece is our queue lies in shared memory
    '''
    numbers = [1,2,3]
    #Array & value & queue
    arr = Array('i',3)
    val = Value('d',2.2)
    q = Queue()
    p1 = Process(target=append_numbers,args=(numbers,arr,val,q))

    p1.start()
    p1.join()

    # print(*result)
    print(*arr)
    print(val.value)
    while q.empty() is False:
        print(q.get())

def add_balance(balance,lock):
    for _ in range(2000):
        lock.acquire()
        balance.value= balance.value + 1
        lock.release()

def withdraw_balance(balance,lock):
    for _ in range(2000):
        lock.acquire()
        balance.value = balance.value - 1
        lock.release()

def multiprocessingLock():
    '''
    After long try, we got 1744 as final balance:
    python .\\multi_processing.py
    1744

    - Multiple process acessing same variable causing race condition.
    - read, add+1, update back. Before p1 updates backs, if p2 also reads, it will create a mess
      and thats why we got 1744.
    - it's always good to use lock at places where we are working with shared variables.
    - acquire(), release()
    '''
    balance = Value('i',200)
    lock = Lock()
    p1 = Process(target=add_balance,args=(balance,lock))
    p2 = Process(target=withdraw_balance,args=(balance,lock))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print(balance.value)


if __name__ == "__main__":
    '''
    Why multi-processing needed and GIL: https://www.youtube.com/watch?v=XVcRQ6T9RHo
    Short explanation:
    - We have a list [1,2,3,4,5,6,7,8,9,10] and task is to sum up. We decide to multi-threading
    - thread1 - [1,2] thread2 - [3,4] ... thread5 - [9,10]
    - Now all are multiple threads present inside the process which runs the python interpretator
    - Interpreator will only process a thread if it has GIL. GIL doesn't always stick to one thread.
    - It keeps switching between multiple threads such that no thread waits longer for CPU's time.
    - So parallelism is not acheived here.
    - Even though OS allocates CPU time for a thread, if it doesn't have GIL interpreter not goona
      execute it.
    - On Contrary, In multiprocessing, each process gets their own interpreter there by not
      fighting for single lock. and they run simultaneously as they have been running on different cores /
      efficeintly switched between tasks by OS schedular.
    - async - I/O bound task (where CPU is idle)
    - multiprocessing - CPU bound task (CPU is on very head load on single core, so lets split them to save time) 
    
    ****IMP: why "if __name__ == "__main__":" is important?
    - This is a real, common trap, so it's worth pausing on. Starting a new process means 
    literally starting a brand-new Python interpreter, which has to re-import your script
    from scratch to know what count_up even is. If you didn't guard your Process(...).start() calls
    behind if __name__ == "__main__":, then when the new process re-imports your file, 
    it would hit those same Process(...).start() lines again, and try to launch more 
    processes, which would try to launch more, endlessly. 
    The guard ensures "only start new processes when this file is being run directly, not when 
    it's being re-imported by a child process."

    Drawbacks & trade-offs:
    - As each process is independent, each have its own resources(memory,storage etc.,) which pile ups.
      On other hand, all thread uses same resources shared by them as all part of one process.
    - Code change made by one program (side effects) won't be reflecting in main as they are same code
      of different copy.

    example code:
        counter = 0

        def increment():
            global counter
            counter += 1          # this only changes THIS process's private copy

        if __name__ == "__main__":
            p = Process(target=increment)
            p.start()
            p.join()
            print(counter)         # still 0! the worker's change never reached here
    '''
    # usingProcess()
    # usingPool() # it essentially does map and reduce (map - divide, reduce - aggregate back)
    # interprocessDataSharing()
    multiprocessingLock()


