# -*- encoding=utf-8 -*-

import psutil
import threading
from task import Task, AsyncTask
from queue import ThreadSafeQueue

#任务处理线程
class ProcessThread(threading.Thread):
	"""docstring for ProcessThread"""
	def __init__(self, task_queue, *args, **kwargs):
		threading.Thread.__init__(self, *args, **kwargs)

		self.dismiss_flag = threading.Event()    #线程停止标记
		self.task_queue = task_queue			#任务队列
		self.args = args
		self.kwargs = kwargs

	def run(self):
		while True:
			#判断线程是否被要求停止
			if self.dismiss_flag.is_set():
				break

			task = self.task_queue.pop()
			if not isinstance(task,Task):
				continue
			#通过函数调用执行task实际逻辑
			result = task.callable(*task.args, **task.kwargs)
			if isinstance(task, AsyncTask):
				task.set_result(result)

	def dismiss(self):
		self.dismiss_flag.set()

	def stop(self):
		self.dismiss()

#线程池
class ThreadPool(object):
	"""docstring for ThreadPool"""
	def __init__(self, size=0):
		if not size:
			#约定线程池大小为cpu核数的两倍。最佳时间
			size = psutil.cpu_count() * 2
		self.pool = ThreadSafeQueue(size)    #线程池
		self.task_queue = ThreadSafeQueue()		#任务队列

		for i in range(size):
			self.pool.put(ProcessThread(self.task_queue))

	def start(self):
		for i in range(self.pool.size()):
			thread = self.pool.get(i)
			thread.start()

	#停止线程池
	def join(self):
		for i in range(self.pool.size()):
			thread = self.pool.get(i)
			thread.stop()
		#停止完后清空线程池
		while self.pool.size():
			thread = self.pool.pop()
			thread.join()

	#向线程池提交任务
	def put(self, item):
		if not isinstance(item, Task):
			raise TaskTypeErrorException()
		self.task_queue.put(item)

	#批量提交任务
	def batch_put(self, item_list):
		if not isinstance(item_list, list):
			item_list = list(item_list)
		for item in item_list:
			self.task_queue.put(item)

	def size(self):
		return self.pool.size()



class TaskTypeErrorException(Exception):
	"""docstring for TaskTypeErrorException"""
	def __init__(self, arg):
		pass
		