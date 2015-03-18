import re
import string

# word1 = 'FeedMee<3!'
# word1 = "Goonies!:)"

# exclude = list(set(string.punctuation))

# ex = [':','<']
# for x in ex:
# 	if x in word1:
# 		word1 = word1[:word1.find(x)] + " " + word1[word1.find(x):]


import emo
for x, y in emo.emo.iteritems():
	if len(x) == 0:
		print x
		
		