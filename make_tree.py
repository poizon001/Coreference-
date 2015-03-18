import json, requests, ast
from sentimentanalysis import sentiment, cleaner
import sentimentanalysis.FullNNP as fullname
import nltk
import operator

def getData1(text, delimiter, bd, sentiment):
    url = 'http://localhost:8080/sae-1.0.0-BUILD-SNAPSHOT/analytics/analyse'
    json_data = {"sentence":text, "bd":bd, "sentiment":sentiment, "delimiter":delimiter}
    headers = {"Content-type": "application/json","Accept": "application/json"}
    jsonData = json.dumps(json_data)
    response = requests.post(url, headers=headers, data=jsonData)
    return response.json()

def make_tree(line):
	bd = getData1(line, bd=True, sentiment=False, delimiter="-")
	bd = "["+str(bd)+"]"
	bd = ast.literal_eval(bd)
	return bd

data = open('need_tree.txt','r').read().split('\n')

lines = []
for k,i in enumerate(data):
	# print k
	i = i.split('|')
	lines.append(i[7])
	# if k == 5:
	# 	break

result = open('tree.txt','w')
for i,j in enumerate(lines):
	print i
	tree = make_tree(" ".join(j.split()))
	result.write(str(data[i])+'|'+str(tree)+"\n")
	


