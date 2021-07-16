from thread_machine import GreenThreadMachine, Worker

################ Simple Unit Test ################
testMachine = GreenThreadMachine(2)
testWorker = Worker()

testWorker.sayHello()
testMachine.sayHello()


testMachine._workers[0].sayHello()
testMachine._workers[1].sayHello()
