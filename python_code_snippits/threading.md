# Python threading

## Queue between threads
```python
from queue import Queue
from threading import Thread

class WorkerThreat(Thread):
    def __init__(self, data_queue) -> None:
        super(WorkerThreat, self).__init__()
        self.queue = data_queue

    def run(self) -> None:
        for i in range(5):
            sleep_time = randint(1, 4)
            print("sleeping " + str(sleep_time))
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
