import time
import asyncio

def main():
    # synchronous_programming()
    '''
    Creating a event loop with main/initial coroutine asynchronous_programming.
    Uses single CPU core efficiently
    '''
    asyncio.run(asynchronous_programming())

async def asynchronous_programming():
    '''
    async -> Tells this function is a special function called coroutine function
    await -> It should always be in a async function. This indicates to event loop that
    "I'm going to wait on this, you can take other tasks that are scheduled".
    '''
    # Creating coroutine and adding to event loop and calling it right away
    await boil_rice()
    await cook_veggies()

    # via create task - Add it to event loop and execute them when ever we want
    # task1 = asyncio.create_task(boil_rice()) # creates a task object, event loop can work on it as well
    # task2 = asyncio.create_task(cook_veggies())
    # print(await task1) # I finished boiling rice
    # await task2

    #via gather - Add all coroutines and create one single gather object. It also can be used by event loop
    task1 = boil_rice()
    task2 = cook_veggies()
    # print(await asyncio.gather(task1,task2)) # ['I finished boiling rice', None]
    
    # The above line can also be done by
    gather = asyncio.gather(task1,task2)
    await gather

async def cook_veggies():
    print("I'm starting to cook veggis")
    await asyncio.sleep(10)
    print("I finished coking veggies")   

async def boil_rice():
    print("I'm starting to boild the rice")
    await asyncio.sleep(5)
    print("I finished boiling rice")
    return "I finished boiling rice"

def synchronous_programming():
    windows_staring()
    check_teams()

def windows_staring():
    print("Im getting turned ON!!!!!!!!")
    time.sleep(10)
    print("I' now turned ON!!!!!!!!!!!!")

def check_teams():
    print("Starting to check Teams!!!!!!!!")
    time.sleep(10)
    print("Finished checkiong Teams!!!!!!!!")

if __name__ == "__main__":
    main()