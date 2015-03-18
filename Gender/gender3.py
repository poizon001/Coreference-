import json
import Queue
import urllib2
import threading
import logging

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-s) %(message)s',)


def getGenders(name, q, p):
	logging.debug('Starting')

	url = "https://gender-api.com/get?name={0}&key=ANyVSrjLrTmeqohppZ".format(name)
	# print "url :", url
	data = json.load(urllib2.urlopen(url))
	# print "Gender: " + data["gender"]
	t1 = data["gender"]
	t2 = data["accuracy"]
	# result.append((t1,t2))
	q.put((p,(t1,t2)))
	# return result
	# print q.qsize()
	# print q.get()
	logging.debug('Exiting')

	return q

if __name__ == '__main__':

	names = ["John", "janna", "George", "Obama", "Narendra", "Allen","Piter","Parker","Rose"]
	# names = ["John"]
	q = Queue.PriorityQueue()
	threads = []

	for i,name in enumerate(names):
		t = threading.Thread(name = 't'+str(i), target = getGenders, args = (name,q,i))
		t.start()
		threads.append(t)
	for t in threads:
		t.join()

	print "size: ", q.qsize()
	while not q.empty():
		print q.get()
