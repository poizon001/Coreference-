'''
Rule Based Sentiment Analysis
Python Script which calculates Sentiment Scores of a sentence, Sub Sentiments of Subject, Object and Verb triplet.

Input: Basic Dependency Trees of sentences, BD Trees are created using Stanford Core NLP Parser.
Output: TUPLE: (Sentence, Sentiment, Subject, Subject-POS, Verb, Object, Object-POS, Sub-Sentiment)
'''

import FullNNP as fullname
import ast

''' Create Positive and Negative Bag Of Words '''
positives = open("sentimentanalysis/data/positives.txt").read().split("\n")
negatives = open("sentimentanalysis/data/negatives.txt").read().split("\n")

# sub_sentiments = []
visited_verbs = []
possible_verbs = ["VB","VBD","VBP","VBG","VBN","VBZ"]
possible_objs = ["pobj","iobj","dobj","obj","npadvmod"]
possible_subjs = ["nsubj","nsubjpass","csubjpass","subj","csubj","xsubj"]
other_ignore = ["ccomp"]

''' Utility function to get the word from the root node '''
def filter_node(word):
	word = word.strip().replace("-> ","")
	word = str(word.rsplit("-",1)[0])
	return word


''' Utility function to get the relation of word with its parent '''
def get_reln(word):
	word = word.strip()
	i = word.find("(")
	f = word.find(")")
	pos = str(word[i+1:f])
	return pos

''' Utility function to get the POS of the word'''
def get_pos(word):
	word1 = word.strip().replace("-> ","")
	word1 = str(word1.rsplit("-",1)[-1])
	word1 = word1.split(" ")[0]
	return word1

''' Function to calculate the sentiment of a word based on occurance in positive and negative list '''
def word_sentiment(word):
	word = word.lower()
	if word in positives:
		return 2
	elif word in negatives:
		return -2
	else:
		return 0

''' Function to check if root word is obj or not, Used to decide weather to calculate root sentiment or not '''
def check_for_obj(reln):
	possible_objs1 = ["pobj","iobj","dobj","obj"]
	if reln in possible_objs1:
		return True
	else:
		return False


''' Decide if the child node is verb type or not'''
def checkvb(reln, pos):
	possible_pos1 = ["VB","VBD","VBG","VBN","VBP","VBZ"]
	possible_reln1 = ["ccomp"]
	if pos in possible_pos1:
		return True
	elif reln in possible_reln1:
		return True
	else:
		return False

		
''' Function to print and traverse the tree'''
def print_tree(tree):
	for subTree_dic in tree:
		orig_node = subTree_dic['node']
		inside_trees = subTree_dic['subTree']
		if len(inside_trees) == 0:
			print orig_node
		else:
			print orig_node
			print_tree(inside_trees)

''' Base function for parsing and printing '''
def tree_parse(tree):
	overall_sentiment = 0
	for subTree_dic in tree:
		orig_node = subTree_dic['node']
		node = filter_node(orig_node)
		inside_trees = subTree_dic['subTree'] 
		if len(inside_trees) == 0:
			print orig_node
			sentiment = word_sentiment(node)
		else:
			print orig_node
			sentiment = word_sentiment(node) + tree_parse(inside_trees)
		overall_sentiment += sentiment
	return overall_sentiment

''' Decide the factor depending upon the child parent relationship'''
def get_factor(cr):
	factor_1o5 = ["discourse","vmod"]
	factor_2 = ["quantmod", "npadvmod", "advmod"]	
	
	factor = 1
	if cr in factor_1o5:
		factor = 1.5
	elif cr in factor_2:
		factor = 2

	elif cr == "neg":
		factor = -1
	return factor

''' Convert the calculated sentiment into standard values '''
def convert_sentiment(senti):
	if senti == 0:
		senti = 0
	elif senti > 0 and senti < 2:
		senti = 1
	elif senti >= 2:
		senti = 2
	elif senti < 0 and senti >= -2:
		senti = -1
	elif senti < -2:
		senti = -2
	return senti

''' Function to extract subject and object from a tree '''
def extract_subj_obj(tree):
	s1 = []
	o1 = []
	spos = []
	opos = []
	
	tree = tree[0]
	node = tree['node']
	node_list = tree['subTree']

	node = filter_node(node)
	node_reln = get_reln(tree['node'])
	pos = get_pos(tree['node'])

	strn = node + "-" + pos
	lis1 = fullname.fullnnp(tree,strn)

	if lis1 and lis1[0] != "":
		node = lis1[0]
		pos = lis1[1]
	
	
	s2 = []
	o2 = []
	sp = []
	op = []
	if node_reln in possible_objs:
		o1.extend(node)
		opos.extend(pos)
	if node_reln in possible_subjs:
		s1.extend(node)
		spos.extend(pos)

	for sub_node in node_list:
		leaf = sub_node['node']
		leaf = filter_node(leaf)
		leaf_reln = get_reln(leaf)
		leaf_tree = sub_node['subTree']
		leaf_pos = get_pos(leaf)
		strn = leaf + "-" + leaf_pos
		lis1 = fullname.fullnnp(tree,strn)

		# lis = lis1[0]
		# pos1 = lis1[1]
		if lis1 and lis1[0] != "":
			leaf = lis1[0]
			leaf_pos = lis1[1]
		if leaf_reln in possible_subjs:
			s1.extend(leaf)
			spos.extend(leaf_pos)
		if leaf_reln in possible_objs:
			o1.extend(leaf)
			opos.extend(leaf_pos)

		if leaf_tree:
			s2, sp, o2, op = extract_subj_obj(leaf_tree)

#######################################################################

	for x in o2:
		if x not in o1:
			o1.extend(o2)
			opos.extend(op)

	for x in s2:
		if x not in s1:
			s1.extend(s2)
			spos.extend(sp)

	#subj1 = s1 + s2
	#obj1 = o1 + o2
	#sspos = spos + sp
	#oopos = opos + op
	return s1, spos, o1, opos

''' Function to get sentiment tuple for a tree '''
def get_root_sentiment(tree, root_node, visited_verbs):
	subj = []
	obj = []
	score = 0
	tot_fact = 1
	tree_dic = tree[0]
	subjpos1 = []
	objpos1 = []
	root = tree_dic['node']
	root = filter_node(root)
	root_reln = get_reln(tree_dic['node'])
	ps = word_sentiment(root)

	pt = 0
	nt = 0
	ft = 0
	tree_list = tree_dic['subTree']

	for item in tree_list:

		child = filter_node(item['node'])
		child_tree = item['subTree']

		reln = get_reln(item['node'])
		pos = get_pos(item['node'])
		fact = get_factor(reln)
		sent = word_sentiment(child)
		strn = child + "-" + pos
		lis1 = fullname.fullnnp(tree,strn)
		lis = lis1[0]
		pos1 = lis1[1]
		
		################################# NEW #######################################

		if lis1 and lis1[0] != "":
			child = lis1[0]
			pos = lis1[1]
		
		if reln in possible_subjs:
			subj.extend(child)
			subjpos1.extend(pos)
			sent = 0
			fact = 1
		elif reln in possible_objs:
			obj.extend(child)
			objpos1.extend(pos)
			sent = 0
			fact = 1

		if reln in other_ignore:
			sent = 0
			fact = 1




		if len(child_tree) != 0:
			newdic = []
			newdic.append(item)
			final, pt, nt, ft = tree_sentiment(newdic, root_node)
			sent = final

			########### Should i consider it or not Verb in the leaf
			if get_pos(item['node']) in possible_verbs:
				sent = 0
			####################

			if child != root_node and child not in visited_verbs:
				subj1, s1, obj1, o1 = extract_subj_obj(child_tree)


				for x in subj1:
					if x not in subj:
						subj.extend(subj1)
						subjpos1.extend(s1)


				for x in obj1:
				 	if x not in obj:
				 		obj.extend(obj1)
				 		objpos1.extend(o1)
			
		tot_fact *= fact
		score += sent

	tot_sent = ps + score
	tot_sent *= tot_fact
	''' New Script 5/9/2014 '''
	freq = pt + nt + ft
	if freq != 0:
		tot_sent = tot_sent/freq
	tot_sent = convert_sentiment(tot_sent)
	tot_sent = str(tot_sent)

	tple = (subj, subjpos1, root, obj, objpos1, tot_sent)

	return tple

''' For original tree get sub sentiments tuples list '''
def get_sub_sentiments(tree, root_node, sub_sentiments, visited_verbs):
	tree_dic = tree[0]
	root = tree_dic['node']
	leafs = tree_dic['subTree']
	for leaf in leafs:
		leaf_node = leaf['node']
		filter_leaf_node = filter_node(leaf_node)
		leaf_tree = leaf['subTree']
		if len(leaf_tree) != 0:
			newdic = []
			newdic.append(leaf)
			get_sub_sentiments(newdic, root_node, sub_sentiments, visited_verbs)
			leaf_reln = get_reln(leaf_node)
			leaf_pos = get_pos(leaf_node)
			if checkvb(leaf_reln, leaf_pos):
				visited_verbs.append(filter_leaf_node)
				tple = get_root_sentiment(newdic, root_node, visited_verbs)
				sub_sentiments.append(tple)

''' Analysing and calculating the complete sentiment for a tree '''
def tree_sentiment(tree, root_node):
	''' Iterate the multiple root nodes '''
	poscount = 0
	negcount = 0
	final = 0
	factor_count = 0

	for subTree_dic in tree:
		subtreefi = 0

		''' Create Root Node Tuple '''
		orig_node = subTree_dic['node']
		root_node1 = filter_node(orig_node)
		root_reln = get_reln(orig_node)
		root_pos = get_pos(orig_node)
		parent_tuple = (root_node1, root_pos, root_reln)
		inside_trees = subTree_dic['subTree']

		''' Calculate sentiment for root node '''
		if root_reln in possible_subjs or root_reln in possible_objs:
			ps = 0
			ignore = root_node1
		if root_reln in other_ignore:
			ps = 0
			ignore = root_node1
		# elif "JJ" in root_reln:
		# 	ps = word_sentiment(root_node1)
		# 	if ps == 2:
		# 		poscount += 1
		# 	elif ps == -2:
		# 		negcount += 1
		else:
			ps = word_sentiment(root_node1)

			if ps == 2:
				poscount += 1
			elif ps == -2:
				negcount += 1
			ignore = ""


		if root_node1 != ignore:
			''' Go Further down in its leafs '''
			leaf_xis = 0
			total_factor = 1
			for leafs in inside_trees:
				orig_node = leafs['node']
				child_node = filter_node(orig_node)
				child_reln = get_reln(orig_node)
				child_pos = get_pos(orig_node)
				
				''' Check if leaf is a tree or just a terminating point '''
				leaf_inside_trees = leafs['subTree']
			
				if len(leaf_inside_trees) == 0:	
					score = word_sentiment(child_node)

					if score == 2:
						poscount += 1
					elif score == -2:
						negcount += 1
					factor = get_factor(child_reln)
					if factor != 1:
						factor_count += 1
				else:
					dicleaf = []
					dicleaf.append(leafs)
					score, p, n, f  = tree_sentiment(dicleaf, root_node)
					factor = get_factor(child_reln)
					if factor != 1:
						factor_count += 1
					if f != 1:
						factor_count += f
					poscount += p
					negcount += n
				total_factor *= factor
				leaf_xis += score
		else:

			''' Just go one level '''
			leaf_xis = 0	
			for leafs in inside_trees:
				orig_node = leafs['node']
				child_node = filter_node(orig_node)
				child_reln = get_reln(orig_node)
				child_pos = get_pos(orig_node)
				if "JJ" in child_pos:
					score = word_sentiment(child_node)
					leaf_xis += score
			total_factor = 1

		subtreefi = ps + leaf_xis
		subtreefi *= total_factor
	final += subtreefi
	return final, poscount, negcount, factor_count

def flat(lis):
	res = []
	if lis:
		for item in lis:
			if type(item) != list:
				item = str(item)
				res.append(item)
			else:
				res.extend(flat(item))
	return res

def dup(lis):
	return list(set(lis))

def analyze_sentiment(bd, emo):	
	sub_sentiments = []
	visited_verbs = []
	result = {}
	resultlis = []
	line = str(bd)
	tree = line.decode('unicode_escape').encode('ascii','ignore')		
	tree = ast.literal_eval(tree)
	tree_orig = tree[0]
	temp = str(tree[0][0])
	root_node = tree_orig[0]['node']
	root_node = filter_node(root_node)

	sentim, pc, nc, fc = tree_sentiment(tree_orig, root_node)
	freq = pc + nc + fc
	if freq != 0:
		sentim = sentim/freq
	sentim = convert_sentiment(sentim)
	sentim = str(sentim)
	

	root_tple = get_root_sentiment(tree_orig, root_node, visited_verbs)
	sub_sentiments.append(root_tple)
	get_sub_sentiments(tree_orig, root_node, sub_sentiments, visited_verbs)
	
	for j in range(len(sub_sentiments)):
		subs_sent = list(sub_sentiments[j])
		calc_sent = subs_sent[5]

		# if emo:
		# 	emo = max(emo.split(","))
		# 	subs_sent.pop()
		# 	subs_sent.append(emo)

		nl = []	
		for x in subs_sent:
			if type(x) == list:
				y = ",".join(x)
			else:
				y = x
			nl.append(y)
		nlis = "|".join(nl)	
		resultlis.append(nlis)
	result['sub_sentiment_list'] = resultlis 
	return result

def get_adjective(tree):
	possible_adjectives = ["JJ", "JJS", "JJR", "RB", "RBR", "RBS"]
	tree_dic = tree[0][0]
	adj = []
	tree_list = tree_dic['subTree']
	for item in tree_list:
		child = filter_node(item['node'])
		child_tree = item['subTree']
		reln = get_reln(item['node'])
		pos = get_pos(item['node'])
		if pos in possible_adjectives:
			adj.append(child)
	return adj


def get_its_parent(tree, dc):
	parent = []
	if tree == dc:
		parent = []
		parent.append(tree[0]['node'])
		return parent
	
	for subTree_dic in tree:
		orig_node = subTree_dic['node']
		node = filter_node(orig_node)
		inside_trees = subTree_dic['subTree']

		if len(inside_trees) == 0:
			a = 1
		else:
			for leaf in inside_trees:
				if leaf == dc[0]:
					parent.append(orig_node)
			parent.extend(get_its_parent(inside_trees, dc))
	return parent


def isUsefulEntity(reln, pos):
	#check in parallel or check its parent node
	# if reln in possible_subjs:
	# 	return True
	# elif reln in possible_objs:
	# 	return True
	if pos in possible_verbs:
		return True
	# elif word in other_ignore:
	# 	return True
	else:
		return False


def checkPhrase(node, lookup, sentence):
	res = []
	for each in lookup[node.lower()].split(";"):
		each = each.strip()
		if each in sentence:
			res.append(each)
	return res



from lexicon import lexicon
def conflict_parser(origtree, tree, lookup, sentence):
	result = []
	sent = []
	for subTree_dic in tree:
		orig_node = subTree_dic['node']
		node = filter_node(orig_node)
		inside_trees = subTree_dic['subTree'] 
		pos = get_pos(orig_node)
		reln = get_reln(orig_node)
		
		if len(inside_trees) == 0:
			
			if node.lower() in lookup:
				
				if isUsefulEntity(reln, pos):

					### This node is level 1 useful             ##  node
					### Look for the complete phrase            ## multiples >> keyphrase, value
					### Check if complete pharse is useful or not

					eax = checkPhrase(node, lookup, sentence)
					if eax:
						# Now you have the keyphrases which are in the sentence
						trips = []
						for each1 in eax:
							trips.append((each1, lexicon[each1]))
						result.append((node, trips))

				else:
					di = {}
					di['node'] = orig_node
					di['subTree'] = inside_trees
					di1 = []
					di1.append(di)	
					parent = get_its_parent(origtree, di1)
									
					if parent:
						preln = get_reln(parent[0])
						ppos = get_pos(parent[0])
						if isUsefulEntity(preln, ppos):

							### This parent is useful level1
							### Check for complete phrase
							### Check if complete phrase if useful or not

							eax = checkPhrase(node, lookup, sentence)
							if eax:
								trips = []
								for each1 in eax:
									trips.append((each1, lexicon[each1]))
								result.append((filter_node(parent[0]), trips))




		else:
			if node.lower() in lookup:

				if isUsefulEntity(reln, pos):
					eax = checkPhrase(node, lookup, sentence)
					if eax:
						
						### This node is level 1 useful
						### Look for the complete phrase
						### Check if complete pharse is useful or not
						
						trips = []
						for each1 in eax:
							trips.append((each1, lexicon[each1]))
						
						result.append((node, trips))

				else:
					di = {}
					di['node'] = orig_node
					di['subTree'] = inside_trees
					di1 = []
					di1.append(di)	
					parent = get_its_parent(origtree, di1)

					############## NEW 1/10/2014
					ign = False
					relnto = get_reln(orig_node)
					if relnto in possible_subjs:
						ign = True
					elif relnto in possible_objs:
						ign = True
					if ign:	
					###################################
		
						if parent:
							preln = get_reln(parent[0])
							ppos = get_pos(parent[0])
							if isUsefulEntity(preln, ppos):
								eax = checkPhrase(node, lookup, sentence)
								if eax:
									### This parent is useful level1
									### Check for complete phrase
									### Check if complete phrase if useful or not
									trips = []
									for each1 in eax:
										trips.append((each1, lexicon[each1]))
									result.append((filter_node(parent[0]), trips))

			result.extend(conflict_parser(origtree, inside_trees, lookup, sentence))
	return result