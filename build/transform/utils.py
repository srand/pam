##############################################################################
#
# (C) 2016 - Robert Andersson - All rights reserved.
#
# This file and its contents are the property of Robert Andersson
# and may not be distributed, copied, or disclosed, in whole or in part,
# for any reason without written consent of the copyright holder.
#
##############################################################################


import subprocess
import os
import threading
import multiprocessing
from Queue import Queue, Empty
import sys

_lock = threading.Lock()

def print_locked(format, *args, **kwargs):
	_lock.acquire()
	print(format.format(*args, **kwargs))
	_lock.release()


def execute(cmdline, env=os.environ):
	p = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, env=env)
	s = []
	for line in iter(p.stdout.readline, b''):
		line = line.strip()
		print_locked(line)
		s.append(line)
	p.wait()
	return p.returncode, s


class Thread(threading.Thread):
	def __init__(self, index, input, output):
		super(Thread, self).__init__()
		self.daemon = True
		self.index = index
		self.input = input
		self.output = output

	def run(self):
		while True:
			job = self.input.get()
			if not job:
				return
			try:
				if job.required and not job.completed:
					print_locked('[{}]{}', self.index, job.info)
					job.execute()
				self.output.put(job)
			except Exception as e:
				self.output.put(e)


class Pool(object):
	def __init__(self):
		self.input = Queue()
		self.output = Queue()
		self.threads = []
		print('Threads: {}'.format(multiprocessing.cpu_count()))
		for i in range(multiprocessing.cpu_count()):
			thread = Thread(i, self.input, self.output)
			self.threads.append(thread)
			thread.start()

	def put(self, job):
		self.input.put(job)

	def get(self):
		item = self.output.get()
		if isinstance(item, Exception):
			raise item
		return item

	def get_nowait(self):
		try:
			item = self.output.get_nowait()		
			if isinstance(item, Exception):
				raise item
			return item            
		except Empty:
			return None

	def stop(self):
		for thread in self.threads:
			self.input.put(None)
		for thread in self.threads:
			thread.join()
