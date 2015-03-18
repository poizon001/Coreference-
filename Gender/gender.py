import json
import requests

def getGenders(names):
	result = []
	for name in names:
		url = "http://api.namsor.com/onomastics/api/json/gendre/{0}/Kumar".format(name)
		response = requests.get(url)
		gender = response.json()['gender']
		result.append((gender,0))
		# print gender
	return result


if __name__ == '__main__':

	# names = ["John", "janna", "George", "Obama", "Narendra", "Allen","Piter","Parker","Rose"]
	# s = "In December 2004, we loaned a total of US $971 thousand to the four minority shareholders, who hold an aggregate of the shares of RMGC, to facilitate a statutory requirement to increase RMGC's total share capital."
	# s = s.rstrip('.')
	# s = s.split();
	names = ["ice cream"]
	# names = s
	r = getGenders(names)
	for i in r:
		print i

