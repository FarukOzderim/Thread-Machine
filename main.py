from thread_machine import GreenThreadMachine


def fn_green_thread_example():
    #print("Hello from fn_green_thread_example")
    for i in range(10):
        i * i  # Do some work
        yield  # Yield control back
    # Stop working


machine = GreenThreadMachine(5)

#Assign 20 threads
for i in range(20):
    machine.spawn(fn_green_thread_example())

machine.start()
print("\n$$$$ Hello after machine started\n") 