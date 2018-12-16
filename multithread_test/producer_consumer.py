from threading import Condition, Thread, current_thread
import time
import random
import unittest

AQUIRE = 'AQUIRE'
RELEASE = 'RELEASE'
WAIT = 'WAIT'
NOTIFY = 'NOTIFY'


class FakeCondition():
    def __init__(self, log, real_condition):
        self.log = log
        self.real_condition = real_condition

    def acquire(self):
        self.real_condition.acquire()
        if current_thread().ident in self.log:
            self.log[current_thread().ident].append(AQUIRE)
        else:
            self.log[current_thread().ident] = [AQUIRE]

    def release(self):
        if current_thread().ident in self.log:
            self.log[current_thread().ident].append(RELEASE)
        else:
            self.log[current_thread().ident] = [RELEASE]
        self.real_condition.release()

    def notify(self):
        if current_thread().ident in self.log:
            self.log[current_thread().ident].append(NOTIFY)
        else:
            self.log[current_thread().ident] = [NOTIFY]
        self.real_condition.notify()

    def wait(self):
        self.real_condition.wait()
        if current_thread().ident in self.log:
            self.log[current_thread().ident].append(WAIT)
        else:
            self.log[current_thread().ident] = [WAIT]


queue = []
MAX_NUM = 3


class ProduceConsume():
    def __init__(self, queue, condition):
        self.queue = queue
        self.condition = condition

    def produce(self):
        nums = range(5)
        for _ in range(10):
            self.condition.acquire()

            if len(self.queue) == MAX_NUM:
                print("Queue full, producer is waiting")
                self.condition.wait()
                print("Space in queue, Consumer notified the producer")
            num = random.choice(nums)
            self.queue.append(num)
            print("Produced", num)
            self.condition.notify()

            self.condition.release()

            time.sleep(random.random())

    def consume(self):
        for _ in range(10):
            self.condition.acquire()

            if not self.queue:
                print("Nothing in queue, consumer is waiting")
                self.condition.wait()
                print("Producer added something to queue and notified the consumer")
            num = self.queue.pop(0)
            print("Consumed", num)
            self.condition.notify()

            self.condition.release()

            time.sleep(random.random())


class MultiThreadTest(unittest.TestCase):
    def setUp(self):
        self.queue = []
        self.log = {}
        self.condition = FakeCondition(self.log, Condition())

    def test_producers_consumers(self):

        producers = [ProduceConsume(self.queue, self.condition) for _ in range(1)]
        consumers = [ProduceConsume(self.queue, self.condition) for _ in range(1)]

        producer_threads = [Thread(target=ProduceConsume.produce, args=(producer,)) for producer in producers]
        consumer_threads = [Thread(target=ProduceConsume.consume, args=(consumer,)) for consumer in consumers]

        threads = producer_threads + consumer_threads

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        EMPTY_ITEM = ''
        prev_item = EMPTY_ITEM
        for _, log in self.condition.log.items():
            for item in log:
                self.assertIn(item, (AQUIRE, RELEASE, WAIT, NOTIFY))
                if item == AQUIRE:
                    self.assertIn(prev_item, (EMPTY_ITEM, RELEASE))
                elif item == RELEASE:
                    self.assertEquals(prev_item, NOTIFY)
                elif item == WAIT:
                    self.assertEquals(prev_item, AQUIRE)
                elif item == NOTIFY:
                    self.assertIn(prev_item, (WAIT, AQUIRE))

                prev_item = item


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(unittest.makeSuite(MultiThreadTest))
