# Thread-Machine

_By FarukOzderim_

Thread-machine is virtual machine running some number of workers, and you can assign generators as threads to this Thread Machine.


# Run
```
python3 main.py
```

# Usage
```
from thread_machine import GreenThreadMachine
machine = GreenThreadMachine(5)

def fn_green_thread_example():
    for i in range(10):
        i * i  # Do some work
        yield  # Yield control back
    # Stop working

#Put 20 threads
for i in range(20):
    machine.spawn(fn_green_thread_example())

machine.start()
```
