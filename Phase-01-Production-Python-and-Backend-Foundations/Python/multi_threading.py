from threading import Thread, Lock
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def make_rice():
    print("Starting to make rice")
    time.sleep(3.000000000001) # Just to demonstrate -> Now the finied print statement randomly prints some times rice first and some times veggies first
    print("Finished to make rice")

def make_veggies():
    print("Starting to make veggies")
    time.sleep(3)
    print("Finished to make veggies")

def thread_basics():
    t1 = Thread(target=make_rice)
    t2 = Thread(target=make_veggies)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print("Done!!!!")

count = 0
def helper_thread_lock(lock):
    '''
    Mistake:
    global count
    for _ in range(100):
        time.sleep(0.01)
        count = count + 1

    -> Here all though bug happens, it's not clearly visible. Because, one sleep() hits, it goes to another thread.
    -> Another thread also hits sleep(), so it combacks to original thread and does the work(count = count + 1) w/o switching between.
    -> As the original thread just received the GIL back, probability of python internal taking away the GIL is very very negligible.

    On the other hand, the current code will surely hit the bug we exepect:
    global count
    for _ in range(100):
        tmp  = count
        time.sleep(0.01)
        count = tmp + 1
     
    -> assume count =0
    -> thread1: tmp stores the cnt. Hits the sleep(). GIL was taken away and given back to thread2 [tmp = 0 cnt = 0]
    -> thread2: tmp stores the cnt. Hits the sleep(). GIL back to thread1 now. [tmp = 0 cnt = 0]
    -> thread1: does update cnt and now goes to next iteration. [tmp = 0 cnt = 1]
    -> thread1: In next itertaion, copy tmp to cnt and hits the sleep(). GIL back to thread2 [tmp = 1 cnt = 1]
    -> thread2: Now it updates cnt with tmp as 0 and now cnt value is changed back to 1 and goes to next iteration [tmp = 0 cnt = 1] => Here cnt should be 2 (bug)
    
    ***ISSUE WITH NOT HAVING A SHARED LOCK BETWEEN THREADS***

    A lock only blocks someone who asks that same lock

    Locking works like this: with lock: means "wait until this lock is free, then take it." 
    Thread 2 only waits if the lock it asks for is held.

    In your code:

    python
    with Lock() as lock:   # every call builds a brand-new lock
    t1 creates lock A and takes it. Lock A is free, so no waiting.
    t2 creates lock B and takes it. Lock B is also free, so no waiting.

    t2 never looks at lock A, so it has no reason to wait for t1. Both threads run inside the with block at the same time.

    Compare the two timelines

    Your code (two different locks), both threads inside at once:

    t1: takes lock A, tmp = 0, sleeps...
    t2: takes lock B, tmp = 0, sleeps...     # not blocked, A and B are unrelated
    t1: count = 1
    t2: count = 1                            # overwrote with the same value

    When t1 hits sleep(), it releases the GIL (but holds the lock) and the OS scheduler runs t2 and it acquires GIL. 
    If t2 asks for the same lock, it blocks (also releasing the GIL), so t1 gets to wake up, 
    update count, and release the lock. Then t2 acquires it.
    '''
    global count
    for _ in range(100):
        # lock.acquire()
        # tmp  = count
        # time.sleep(0.01)
        # count = tmp + 1
        # lock.release() 

        # using with
        with lock:
        # with Lock() as lock: # A lock only blocks someone who asks that same lock
            tmp  = count
            time.sleep(0.01)
            count = tmp + 1

def thread_lock():
    lock = Lock()
    # lock=0
    t1 = Thread(target=helper_thread_lock,args=(lock,))
    t2 = Thread(target=helper_thread_lock,args=(lock,))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print(count)

    print("Done!!!!")

def helper_thread_executors(n):
    if n == 3:
        time.sleep(5)
    print(f"Hi from {n}")
    return n

def thread_executors_map():
    '''
    if res = executors.map(helper_thread_executors,[1,3]), then output will be:
    Hi from 1
    HIIIIIIIIIIIIIIIIIIIII
    1
    Hi from 3
    3

    if res = res = executors.map(helper_thread_executors,[3,1]), then output will be:
    Hi from 1
    HIIIIIIIIIIIIIIIIIIIII
    Hi from 3
    3
    1

    Explanation:
    -> map() immedidately starts both the thread and returns a generator object.
    -> In general, worker thread gets priority over main thread. So here is an approximate flow:
        for [3,1]:
            -> main thread starts both the thread, as helper(3) is called first, it gets the GIL (consider as thread1)
            -> thread1 starts and hits sleep() and so GIL taken back
            -> GIL given to thread2 which has helper(1). It has no wait so it prints "Hi from 1" and its return value is 
               stored in a list inside map() function in ***inorder***.
            -> main receives the GIL back and prints "HIIIIIIIIIII" and hits the for loop. Here it behaves same as imap of Poll in multiprocessing.
            -> It waits for return value from helper(3) which is thread1. So GIL taken back as it waits and given to thread1.
            -> It finishes waiting and prints "Hi from 3" and returns 3 to the list
            -> GIL given back to only existing thread and the values in list are printed as "3 1"
        for [1,3]:
            -> As 1 is present first, it thread executes and stores 1 to the list and thread2 gets GIL and waits.
            -> main gets back and prints "HIIIIIIIIII" and also prints "1" as 1 is thread1 (printing in inorder) and now it waits for helper(3)
            -> helper(3) finishes and prints "Hi from 3" and returns the value to list and we finally see "3"

    '''
    executors = ThreadPoolExecutor(max_workers=3)
    res = executors.map(helper_thread_executors,[1,3])
    print("HIIIIIIIIIIIIIIIIIIIII")
    for result in res: #List
        print(result)
    executors.shutdown(wait=True) # if False - kills running and waiting thread. One more option: cancel_futures=True kills waiting and waits for current running thread

def helper_completed(future):
    if future.cancelled():
        print(" :) Our thread cancelled")
    elif future.exception() is not None:
        raise future.exception()
    else:
        print(f"{future.result()} HI from helper_completed")

def thread_executors_submit():
    '''
    -> submit() -> similar to async doesn't take args as individual positional argument for multiple function calls
    -> It gonna start the worker threads and return a future object for each thread.

    Future object methods:
    -> add_done_callback() -> takes a function object(we can also pass a list of fn objs) 
                              which gonna get called as and when a thread is finished. It by default 
                              passes the future object itself as a parameter to our function
    -> result() -> contains the return value of the task(fuction) executed by thread
    -> cancelled() -> Boolean. True=> cancelled False=> completed
    -> exception() -> return the exception object if the thread failed. We can raise them.

    as_completed()
    -> argument is a list/any iterable containing future object as its values.
    -> it gonna yeild the future object as and when a thread finishes. Unlike map, it won't follow the order of tasks.

    Output:
    Hi from 1
    1 HI from helper_completed
    1
    Hi from 3
    3 HI from helper_completed
    3
    '''
    executors = ThreadPoolExecutor(max_workers=3)

    # helper_thread_executors([1,3]) -> not created as multiple threads with helper_thread_executors(1), helper_thread_executors(3)
    # f = executors.submit(helper_thread_executors,[1,3])
    # print(f)

    future_objs = []
    for n in [3,1]:
        f = executors.submit(helper_thread_executors,n)
        f.add_done_callback(helper_completed)
        future_objs.append(f)

    for future in as_completed(future_objs): # Gonna yeild the future obj of a thread as and wehen a thread finishes.
        print(future.result())

if __name__ == "__main__": # Not a necessary here in thread
    '''
    Why GIL?
    -> Thread-safe refrence counting. To keep track of number of variables references a object. As it uses shared memory, it can mess up.
       updating a value is 3 byte code: read it, add+1, write back.

    Risk in Thread
    -> Shared memory can lead to race condition(discussed in lock)
    '''
    # thread_basics()
    # thread_lock()
    # thread_executors_map()
    thread_executors_submit()

'''
                              asyncio	                           threading	                        multiprocessing
Best for	               I/O-bound waiting	                  I/O-bound waiting	            CPU-bound calculating
Genuine multi-core parallelism?	No (one core)	                  No (GIL, one core)	        Yes (separate processes)
Memory	                   Shared (one interpreter)	              Shared (one process)	        Separate per process
Cost to create one unit	   Very cheap (thousands fine)	          Cheap-ish (hundreds fine)	    Heavier (roughly one per core)
Switching control	       Voluntary, only at await;              The OS decides when, can      The OS schedules whole processes independently
                           deterministic	                      happen almost anywhere; unpredictable                              
Main hazard	Accidentally blocking the event loop	              Race conditions on shared data Passing data between separate memories
Needs if __name__ == "__main__":?	No	                          No	                         Yes
Needs async-aware libraries? Yes (httpx, aiofiles, ...)	          No — ordinary blocking libraries work fine	No
'''