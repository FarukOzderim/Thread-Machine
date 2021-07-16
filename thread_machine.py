import random
import queue
import time
from concurrent.futures import ThreadPoolExecutor

LOGGING = False
 
class GreenThreadMachine:
    """
    A ``virtual machine`` that executes any number of ``green threads``.
 
    A green thread is simply a ``generator``, which does a little bit of
    work and then ``yield``s back control to the machine; eventually it
    stops working, and is removed from the machine's collection of green
    threads.
 
    The Green Thread Machine maintains a fixed pool of native threads and
    balances their workload. When a green thread is done (when it returns),
    the native thread that ran it inspects other native threads to find one
    whose collection  of green threads is sufficiently larger than the
    current one's to make rebalancing worthwhile. If the current thread
    finds one, it "steals" one of other thread's green threads so the stolen
    green thread's future execution happens on the current thread.
 
    Note: All implementation code below is just a suggestion to get you started.
 
    .. code-block:: python
 
        machine = GreenThreadMachine(5)
        machine.start()
 
        def fn_green_thread_example():
            for i in range(10):
                i * i  # Do some work
                yield  # Yield control back
            # Stop working
 
        machine.spawn(fn_green_thread_example())
    """
    def __init__(self, num_native_threads):
        self._workers = [Worker() for i in range(0, num_native_threads)]
        self.num_native_threads = num_native_threads
        #Put a connection between workers and the machine for stealing work from other threads when necessary
        for worker in self._workers:
            worker.setParentMachine(self)

    #Assume all green threads are given before the start
    def start(self):
        """
        Starts the Green Thread Machine.
        """
        print("Machine starts, the machine is:",self)
        #Run all the workers
        executor = ThreadPoolExecutor(self.num_native_threads)
        for worker in self._workers:
            future = executor.submit(worker.run)
        print("\n$$$$$$   Machine did start on all the workers\n")
        if LOGGING:
            executor.submit(self.logger)
        executor.shutdown()
 
    def spawn(self, green_thread):
        """
        Submits a new green thread to be executed on the Green Thread Machine.
        Args:
            green_thread: Submitted green thread.
        """
        print("Machine spawns green thread:",green_thread)
        
        '''
        Select a random worker,
        We could select the worker with least green_threads however it seems there is no performance expectation from the assingment.
        
        '''
        self._workers[random.randint(0,self.num_native_threads-1)].green_threads.put(green_thread)
        
    
    def sayHello(self):
        print("Hi I am a GreenThreadMachine")

    def logger(self):
        time.sleep(3)
        for i in range(5):
            time.sleep(0.3)
            for worker in self._workers:
                print("###")
                print(worker)
                print(worker.green_threads)
                print(worker.green_threads.qsize())
            print("### ###")
        print("### ### ###")

class Worker:
 
    def __init__(self):
        self.green_threads = queue.Queue()
        self.parentMachine = None
    
    #For connection with the ParentMachine, for _steal_work
    def setParentMachine(self, parent):
        self.parentMachine = parent
    

    def run(self):
        while True:
            green_thread = self.green_threads.get(timeout=0.1)
            try:
                next(green_thread)
                self.green_threads.put(green_thread)
                
            except StopIteration:
                print(f"StopIteration happened at Worker:{self}, its current length of the queue is:{self.green_threads.qsize()}, stealing work from another worker now")
                self._steal_work()
                
 
    def _steal_work(self):
        """
        Select a worker who has green_thread size bigger than my green_thread_size+1
        We could select the worker with most green_threads using a priority queue however it seems there is no performance expectation from the assingment.
        """
        parentsWorkers = self.parentMachine._workers
        for worker in parentsWorkers:
            if worker.green_threads.qsize() > self.green_threads.qsize()+1:
                #Steal the first green thread
                print(f"\n Worker {self} is stealing from the worker:{worker}")
                self.green_threads.put(worker.green_threads.get(timeout=0.1))
                break




    def sayHello(self):
        print("Hi I am a Worker, My Parent Machine is:",self.parentMachine)

