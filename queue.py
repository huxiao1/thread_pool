# -*- encoding=utf-8 -*-

import threading
import time

class ThreadSafeQueueException(Exception):
	"""docstring for ThreadSafeQueueException"""
	def __init__(self, arg):
		pass
		


#thread queue
class ThreadSafeQueue(object):
	"""docstring for ClassName"""
	def __init__(self, max_size = 0):
		self.queue = []
		self.max_size = max_size
		self.lock = threading.Lock()
		self.condition = threading.Condition()

	def size(self):
		self.lock.acquire()
		size = len(self.queue)
		self.lock.release()
		return size

	def put(self,item):
		if self.max_size != 0 and self.size() > self.max_size:
			return ThreadSafeQueueException()
		self.lock.acquire()
		self.queue.append(item)
		self.lock.release()
		self.condition.acquire()  #size=0 可能发生阻塞，通知阻塞线程继续执行下去
		self.condition.notify()
		self.condition.release()


	def batch_put(self,item_list):
		if not isinstance(item_list,list):
			item_list = list(item_list)
		for item in item_list:
			self.put(item)

	def pop(self,block=False,timeout=None):   #block队列空是否要阻塞等待,timeout是等待时间
		if self.size == 0: 
			if block:  #需要阻塞等待
				self.condition.acquire()
				self.condition.wait(timeout=timeout)
				self.condition.release()
			else:
				return None
		else:
			self.lock.acquire()
			item = None
			if len(self.queue) > 0:
				item = self.queue.pop()
			self.lock.release()
			return item

	def get(self,index):
		self.lock.acquire()
		item = self.queue[index]
		self.lock.release()
		return item
		
if __name__ == '__main__':
	queue = ThreadSafeQueue(max_size=100)
	def producer():
		while True:
			queue.put(1)
			time.sleep(3)

	def consumer():
		while True:
			item = queue.pop(block=True,timeout=2)
			print('get item from queue: %d' % item)
			time.sleep(1)

	thread1 = threading.Thread(target=producer)
	thread2 = threading.Thread(target=consumer)
	thread1.start()
	thread2.start()
	thread1.join()
	thread2.join()