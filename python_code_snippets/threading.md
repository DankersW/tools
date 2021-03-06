# Python threading

## Queue between threads
```python
from queue import Queue
from threading import Thread
from time import sleep
from random import randint

class WorkerThreat(Thread):
    def __init__(self, data_queue) -> None:
        super(WorkerThreat, self).__init__()
        self.queue = data_queue

    def run(self) -> None:
        for i in range(5):
            sleep_time = randint(1, 4)
            print(f'sleeping {sleep_time} seconds')
            sleep(sleep_time)
            self.queue.put(sleep_time)

class MainThreat:
    def __init__(self):
        event_queue = Queue(maxsize=100)
        worker = WorkerThreat(data_queue=event_queue)

        worker.start()
        while True:
            if not event_queue.empty():
                item = event_queue.get()
                print(f"got sleep time: {item}")
                
if __name__ == '__main__':
    m = MainThreat()
```

## Starting a pool of threats concurrently 

```python
import concurrent.futures

def foo(threat_name, more_param):
    print(f'threat {threat_name} started with params {more_param}')

threaths = ['a', 'b', 'c']
with concurrent.futures.ThreadPoolExecutor() as executor:
    [executor.submit(foo, threat_name, more_param=12) for threat_name in threaths]
```

## Wait for threat to be started

```python
from threading import Thread, Event
import time

class T1(Thread):
    def __init__(self, thread_event: Event):
        Thread.__init__(self)
        self._ready_event = thread_event

    def run(self) -> None:
        time.sleep(2)
        print("T1: ready")
        self._ready_event.set()

class T2(Thread):
    def __init__(self, thread_event: Event):
        Thread.__init__(self)
        self._ready_event = thread_event

    def run(self) -> None:
        time.sleep(5)
        print("T2: ready")
        self._ready_event.set()

thread_ready = Event()
observers = [T1(thread_event=thread_ready), T2(thread_event=thread_ready)]
for obs in observers:
    obs.start()
    thread_ready.wait()
```
