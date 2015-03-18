# import sys
# reload(sys)  # Reload does the trick!
# sys.setdefaultencoding('utf-8')
# input_suffix = open('suffix.txt' ,'r').read().split('\n')
# for each in (input_suffix):
# 	token =  each.decode('utf-8').encode('ascii' , 'ignore')
# 	print token

import re
search="pvt ltd"
b = search.split(" ")
print b 
fullstring="infosys pvt ltd"

s =  fullstring.split(" ")
print s 

i = len(s)
i = i-1
for x in reversed(range(len(b))):
	print b[x],s[i]
	if b[x] !=s[i]:
		# return False
		print "false"
		break
	i = i-1 

# return True 
print "true"

# for x in reversed(range(len(fullstring))) , y in reversed(range(len(search)):
# 	print fullstring[x] , search[y]

# print len(s)
