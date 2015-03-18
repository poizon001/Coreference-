import json
import urllib2



def getGenders(names):
	result = []
	for name in names:
		# print "name :" , name

		url = "https://gender-api.com/get?name={0}&key=ANyVSrjLrTmeqohppZ".format(name)
		# print "url :", url
		data = json.load(urllib2.urlopen(url))
		# print "Gender: " + data["gender"]
		t1 = data["gender"]
		t2 = data["accuracy"]
		result.append((t1,t2))

	return result

if __name__ == '__main__':

	names = ["John", "janna", "George", "Obama", "Narendra", "Allen","Piter","Parker","Rose"]

	r = getGenders(names[0])
	for i in r:
		print i[0],i[1]
