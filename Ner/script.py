import json, requests, ast
from sentimentanalysis import  cleaner, sentiment
import sentimentanalysis.FullNNP as fullname

possible_objs = ["pobj","iobj","dobj","obj","npadvmod" ]
possible_subjs = ["nsubj","nsubjpass","csubjpass","subj","csubj","xsubj"]

positives = open("sentimentanalysis/data/positives.txt").read().split("\n")
negatives = open("sentimentanalysis/data/negatives.txt").read().split("\n")

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

positives = [x.strip() for x in positives]
negatives = [x.strip() for x in negatives]

def word_sentiment(word):
	word = word.lower()

	if word in positives:
		return 2
	elif word in negatives:
		return -2
	else:
		return 0

def filter_node(word):
	word = word.strip().replace("-> ","")
	word = str(word.rsplit("-",1)[0])
	return word

def get_reln(word):
	word = word.strip()
	i = word.find("(")
	f = word.find(")")
	pos = str(word[i+1:f])
	return pos

def tree_parse(tree):
	overall_sentiment = 0
	for subTree_dic in tree:
		orig_node = subTree_dic['node']
		node = filter_node(orig_node)
		inside_trees = subTree_dic['subTree'] 
		if len(inside_trees) == 0:
			# print orig_node
			sentiment = word_sentiment(node)
		else:
			print orig_node
			sentiment = word_sentiment(node) + tree_parse(inside_trees)
		overall_sentiment += sentiment
	return overall_sentiment
l = []
''' Utility function to get the POS of the word'''
def get_pos(word):
	word1 = word.strip().replace("-> ","")
	# print word1
	word2 = word1
	word1 = str(word1.rsplit("-",1)[-1])
	word1 = word1.split(" ")[0]

	if any ( [word1 == 'NNP' , word1 == 'NN'] ):
		wow =  sentiment.filter_node(word)
		l.append(wow)
		

	return word1

ans = []
def get_np(tree, origtree , each):

	res = []
	a = []
	for subTree_dic in tree:
		# print subTree_dic
		orig_node = subTree_dic['node']
		# print orig_node
		node = filter_node(orig_node)
		# print node 
		inside_trees = subTree_dic['subTree'] 
		# print inside_trees
		pos = get_pos(orig_node)
		# print pos
		rel = get_reln(orig_node)
		# print "__"
		# print rel 
		strn = node + "-" + pos
		# print strn 
		
		lis1 = fullname.fullnnp(origtree, strn)
		
		if rel in possible_subjs:
			a.append(node)
			a.append(rel)

			if lis1:
				c = lis1[0][0]
				a.append(c)


			# print str(node)
			# try :
			# 	c = (lis1[1][0])
			# 	a.append(c)
			# except:
			# 	continue



		
		if rel in possible_objs:
			a.append(' | ')
			a.append(node)
			a.append(rel)
			# print   node , rel  
			# print '?', node


			if lis1:
				c = lis1[0][0]
				a.append(c)


			# try:
			# 	a.append(lis1[1][0])
			# # 	print lis1[0][0] 
			# except:
			# # 	print '## Error ##'
			# 	# print lis1
			# 	continue 		
		# print a 

		if len(inside_trees) == 0:
			pass
		else:
			a.extend(get_np(inside_trees, origtree,each))

		# aa.extend(a)
		# print "aa" , aa
	return a



	

fo = open('ner_dataset.txt' ,'r').read().split('\n')
dic = {}
for i , each in enumerate(fo):
	print i
	if i==47:	
	 	enumerat
		a = []
		tree = make_tree(each)
		# print tree
		# sentiment.tree_parse(tree[0])
		
		a = get_np(tree[0], tree[0] , each)
		print a 
		# dic[each] = a
		# print dic
		# tree_parse(tree[0])

		print "________"






