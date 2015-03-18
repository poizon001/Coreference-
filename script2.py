import json, requests, ast
from sentimentanalysis import sentiment, cleaner
import sentimentanalysis.FullNNP as fullname
from textblob import TextBlob
from Gender import gender
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



def filter_node(word):
	word = word.strip().replace("-> ","")
	word = str(word.rsplit("-",1)[0])
	return word

firstPersonPronouns = ["i", "me", "myself", "mine", "my", "we", "us", "ourself", "ourselves", "ours", "our"]
secondPersonPronouns = ["you", "yourself", "yours", "your", "yourselves"]
thirdPersonPronouns = ["he", "He", "him", "himself", "his", "she", "her", "herself", "hers", "her", "it", "itself", "its", "one", "oneself", "one's", "they", "them", "themself", "themselves", "theirs", "their", "they", "them", "'em", "themselves"]
otherPronouns = ["who", "whom", "whose", "where", "when","which"]
demonstratives = ["this", "that", "these", "those"]
singularPronouns = ["i", "me", "myself", "mine", "my", "yourself", "he", "him", "himself", "his", "she", "her", "herself", "hers", "her", "it", "itself", "its", "one", "oneself", "one's"]
pluralPronouns = ["we", "us", "ourself", "ourselves", "ours", "our", "yourself", "yourselves", "they", "them", "themself", "themselves", "theirs", "their"]
malePronouns = ["he", "him", "himself", "his"]
femalePronouns = ["her", "hers", "herself", "she"]
neutralPronouns = ["it", "its", "itself", "where", "here", "there", "which"]
pluralPronouns_t = ["we", "they"]

#lst_of_sent -> list conatining the sentences present in the file
lst_of_sent = []

def get_sentences(filename):
	text = open(filename, 'r').read()
	text = " ".join(text.split())
	text.decode('utf-8')
	sent = TextBlob(text)

	lst_of_sent = []

	for i in sent.sentences:
		lst_of_sent.append(str(i))

	return lst_of_sent


#lst conatining pair of(NP, sentence number)
lst_pair_np_sn = []
#lst of NP per sentence [(np11, np12..),(np21,np22,np23..)..]
lst_sent_np = []
#list of rel of NP per snetence
lst_sent_rel = []
#list of rel of NP per snetence
lst_sent_lvl = []

lst_head = []


# get pos tags of a sentence
def get_pos(sent):
	lst_sent_pos = []
	text = nltk.word_tokenize(sent)
	lst_sent_pos = nltk.pos_tag(text)
	
	return lst_sent_pos


def fix_lst_np(list_of_nps):
	
	print "\n >>>>> fix np  <<<<<\n"
	# print "##",list_of_nps
	l = len(list_of_nps)

	for i in range(l):
		if i > 0 and i < l-1:
			# print "ii", list_of_nps[i]
			
			curr = list_of_nps[i]
			pos = get_pos(list_of_nps[i])
			pos = pos[0][1]

			# print " >>>> i", i , " l ", l, list_of_nps
			prev = list_of_nps[i-1]
			next = list_of_nps[i+1]

			print curr, prev, next, pos

			if "NN" in pos:
				if curr in prev or curr in next:
					# print "dcsdavsdva"
					list_of_nps.remove(list_of_nps[i])
		l = len(list_of_nps)
	# print list_of_nps

	return list_of_nps



# t = open('np.txt','w')
def get_lst_sent_np_rel_lvl_head(lst_of_sent):
	for i,j in enumerate(lst_of_sent):
		tree = make_tree(" ".join(j.split()))
		#list of head words for a sentence
		lst_head_tmp = sentiment.get_np_head(tree[0], tree[0])
		# print "head s ---->", lst_head_tmp
		
		#list of noun phrase for a senetnce
		list_of_nps= sentiment.get_np(tree[0], tree[0])


		# print "@@@", list_of_nps
		# list_of_nps = fix_lst_np(list_of_nps, j)

		# res = str(i) + "|" + str(list_of_nps) + "\n"
		
		res = str(list_of_nps) + "\n"
		# t.write(res)

		#making tree for a sentence
		sentiment.tree_parse(tree[0])
		print "^^^", list_of_nps
		
		#temporary lists containing NP, relation, Level; to append in the main list
		tmp_lst = []
		tmp_lst_rel = []
		tmp_lst_lvl = []
		#k1 item in the list i.e. the NP 
		for k1 in (list_of_nps):
			#In sentiment.py function get_np returned empty lis1 if NNP not found 
			#so included False to indicate the absence of NP 
			# try :

			# if k1:
				# print "asdasd", k1[0]



			if len(k1[0]) > 0 and k1[0][0] != False:	
				# print ">>", k1
				for k2 in k1[0]:

					# print "I am here"

					k2 = k2.encode('utf-8')
					#appending the NP to temporary list
					tmp_lst.append(k2)
					#appending pair of NP and sentence number to a new list
					lst_pair_np_sn.append((k2, i))

					# for k2 in k1[2]:
					#k[2] -> realtion 
					#k[3] -> level of NP/PRP
					k2 = k1[2].encode('utf-8')
					lvl = k1[3]
					tmp_lst_rel.append(k2)
					tmp_lst_lvl.append(lvl)
			# except:
			# 	continue
				
		print "after", tmp_lst
		tmp_list = fix_lst_np(tmp_lst)
		#if the NP list is empty dont append in the lst_sent_np 
		#and dont append the head word lst in lst_head
		f = 1
		if len(tmp_lst) > 0:
			for i in tmp_lst:
				if len(i) < 0:
					f=0
					break
			
		if f==1:
			lst_sent_np.append(tmp_lst)
			lst_sent_rel.append(tmp_lst_rel)
			lst_sent_lvl.append(tmp_lst_lvl)
			lst_head.append(lst_head_tmp)



#list of np with its head word per sentences
lst_np_hw_sent = []
#list of np with its rel per sentences
lst_np_rel_sent = []
#list of np with its lvl per sentences
lst_np_lvl_sent = []

def get_np_hw_np_rel_np_lvl(lst_sent_np):
	for i in range(len(lst_sent_np)):
		# print lst_sent_np[i]
		#temporary list for (np, hw), (np, rel), (np, level) per sentence 
		temp = []
		tmp1 = []
		tmp2 = []

		length = len(lst_sent_np[i])
		#using visited so that two head word dont match to the same NP
		vis = [0 for x in range(length)]

		for k in lst_head[i]:
			for j in range(len(lst_sent_np[i])):
				if k in lst_sent_np[i][j] and vis[j] == 0:
					vis[j] = 1
					temp.append((lst_sent_np[i][j],k))
					tmp1.append((lst_sent_np[i][j],lst_sent_rel[i][j]))
					tmp2.append((lst_sent_np[i][j],lst_sent_lvl[i][j]))

				# print vis
		lst_np_hw_sent.append(temp)
		lst_np_rel_sent.append(tmp1)
		lst_np_lvl_sent.append(tmp2)
	# print "\nlst_np_hw_sent\n"
	# for i in lst_np_hw_sent:
	# 	for j in i:
	# 		print j
	# 	print '\n'


#lst_np_hw_sentnum_npnum = list containing NP, head word, sentence number, cluster_id/ID
lst_np_hw_sentnum_npnum = []

def get_lst_np_hw_sentnum_npnum(lst_np_hw_sent):
	for i in range(len(lst_np_hw_sent)):
		for j in range(len(lst_np_hw_sent[i])):
			tmp = []
			tmp.append(lst_np_hw_sent[i][j][0])
			tmp.append(lst_np_hw_sent[i][j][1])
			tmp.append(i)
			lst_np_hw_sentnum_npnum.append(tmp)
	
	for i,j in enumerate(lst_np_hw_sentnum_npnum):
		j.append(i)
		# print i, j
	
	return lst_np_hw_sentnum_npnum




#idx1 = new cluster id   idx2 = previous cluster id
#change the id of all cluster which match idx2 to idx1
def get_update(lst_np_hw_sentnum_npnum, idx1, idx2):
	for i,j in enumerate(lst_np_hw_sentnum_npnum):
		if j[3] == idx1:
			lst_np_hw_sentnum_npnum[i][3] = idx2

	# for i in lst_np_hw_sentnum_npnum:
		# print i

	return lst_np_hw_sentnum_npnum

def quotation_sieve(lst_of_sent, lst_np_hw_sentnum_npnum, lst_sent_np):
	for i,j in enumerate(lst_of_sent):
		if "\"," in j or "\" ," in j:
			pos_tags = get_pos(j)
			# print pos_tags
			l1 = j.index("\"")
			l2 = j.index("\",")

			#ii word present in sent with pos PRP$
			for ii in pos_tags:				
				tmp = j[l1:l2]
				
				if ii[0] not in tmp:
					continue
				# print "ii ", ii[0]
				#idx index of ii in the string from l1 to l2
				idx = tmp.index(ii[0])
				#if the word in between the quotation
				# if idx >= l1 and idx <= l2 and "PRP$" == ii[1] :
				if idx >= l1 and idx <= l2 and ii[0] in firstPersonPronouns :

					# print idx, ii[0], ii[1]
					#temporary string from l2 to end
					tmp = j[l2:len(j)]
					# print lst_sent_np[i]
					
					#k noun phrases in a sentence number i 
					for k in lst_sent_np[i]:
						# print "k ", k
						if k in tmp:
							#idx2 index of np present in sentence i in the string tmp(l2,end)
							idx2 = tmp.index(k, 0, len(tmp))
							t = nltk.pos_tag(k.split())
							
							# print k, t[0][1], t[0][0]
							if t[0][1] == "NNP":
								flag = 0
								np1 = -1
								np2 = -1
								x2 = 0

								for x,y in enumerate(lst_np_hw_sentnum_npnum):
									if k == y[0]:
										np1 = x
								
								for x,y in enumerate(lst_np_hw_sentnum_npnum):
									if ii[0] == y[0]:
										np2 = y[3]
											
								##adding a PRP$ into the lst_np_hw_sentnum_npnum if not present
								l = len(lst_np_hw_sentnum_npnum)
								if np2 == -1:
									tmpl = []
									tmpl.append(ii[0])
									tmpl.append(ii[0])
									tmpl.append(i)
									tmpl.append(l)
									# print "tmpl ", tmpl
									lst_np_hw_sentnum_npnum[np1][3] = l
									idx2 = np1
									idx1 = l
									lst_np_hw_sentnum_npnum.append(tmpl)
									lst_np_hw_sentnum_npnum = get_update(lst_np_hw_sentnum_npnum, idx1, idx2)
								else:
									idx2 = np2
									idx1 = np1
									lst_np_hw_sentnum_npnum = get_update(lst_np_hw_sentnum_npnum, idx1, idx2)
									
	return lst_np_hw_sentnum_npnum

#to get_update the index of NP in the list containing info of np, hw, sent id, cluster id
#k = np
def get_index(lst_np_hw_sentnum_npnum, k, sent_no):
	for i,j in enumerate(lst_np_hw_sentnum_npnum):
		if j[0] == k and j[2] == sent_no:		
			return j

def exact_match(lst_sent_np, lst_np_hw_sentnum_npnum, level_up):
	#temp 
	lst = []
	lst = (lst_np_hw_sentnum_npnum)
	lst = sorted(lst_np_hw_sentnum_npnum, key = operator.itemgetter(2), reverse = True) 

	l = len(lst_sent_np) - 1
	
	while l > level_up-1:
		np_lst = lst_sent_np[l]

		for i in (range(level_up)):
			np_lst1 = lst_sent_np[l-i-1]
			for j in np_lst1:
				for k in np_lst:
					# print j,k
					if j == k:
						idx1 = get_index(lst_np_hw_sentnum_npnum, k, l-1-i) 
						idx2 = get_index(lst_np_hw_sentnum_npnum, j, l)
						# print idx1, idx2
						lst_np_hw_sentnum_npnum = get_update(lst_np_hw_sentnum_npnum, idx1[3], idx2[3])
		l -= 1
	return lst_np_hw_sentnum_npnum

#returns list: items of list are list with 3 values each
#0. male/female 1.probability 2.no of docs
def get_gender_np_sent(lst_sent_np):
	lst_sent_np_gender = []
	lst = lst_sent_np
	for i in lst:
		# print "iiiii", i
		if len(i) != 0:
			# print "igggg", i
			for j in  range(len(i)):
				t = (i[j]).split()
				if len(t) > 1:
					i[j] = t[0]
			# print  "iiiii", i
			lst_sent_np_gender.append(gender.getGenders(i))
		else:
			lst_sent_np_gender.append([False])

	return lst_sent_np_gender

def pronoun_gender(lst_sent_np, lst_np_hw_sentnum_npnum, level_up, lst_sent_np_gender, start_sent):
	# l = len(lst_sent_np) - 1 - start_sent
	l = start_sent

	while l >= 0:
		np_lst = lst_sent_np[l]
		flag = 0

		for i in np_lst:
			# print "ii", i
			prp = 0
			prp_female = 0
			prp_male = 0
		
			if i.lower() in femalePronouns:
				prp_female = 1
			elif i.lower() in malePronouns:
				prp_male = 1

			# print i, prp_male, prp_female
			
			for j in (range(level_up)):
				if l-j-1 >= 0:
					np_lst_up = lst_sent_np[l-j-1]
					gendr_lst_up = lst_sent_np_gender[l-j-1]
					
					# print "######", np_lst_up
					
					for k1,k2 in enumerate(np_lst_up):
						t = get_pos(k2)
						pos = t[0][1]
						gendr = gendr_lst_up[k1][0]
						# print ">>",k2, pos, gendr

						if (prp_male == 1 and pos == "NNP" and gendr.decode('utf-8') == "male"):
							flag = 1
							print "m ", k2
							idx1 = get_index(lst_np_hw_sentnum_npnum, i, l)
							idx2 = get_index(lst_np_hw_sentnum_npnum, k2, l-j-1)
							# print idx1
							# print idx2
							lst_np_hw_sentnum_npnum = get_update(lst_np_hw_sentnum_npnum, idx1[3], idx2[3])
							
						elif(prp_female == 1 and pos == "NNP" and gendr.decode('utf-8') == "female"):
							flag = 1
							print "f ", k2
							idx1 = get_index(lst_np_hw_sentnum_npnum, i, l)
							idx2 = get_index(lst_np_hw_sentnum_npnum, k2, l-j-1)
							# print idx1
							# print idx2
							lst_np_hw_sentnum_npnum = get_update(lst_np_hw_sentnum_npnum, idx1[3], idx2[3])
						
						if flag == 1:
							break
				else:
					break
				if flag == 1:
					break
		l -= 1
	
	return lst_np_hw_sentnum_npnum

def pronoun_same_sent(lst_sent_np, lst_np_hw_sentnum_npnum, lst_np_lvl_sent):
	lst1 = lst_sent_np

	lst = ast.literal_eval(str(lst1))

	lst_sent_np_gender = get_gender_np_sent(lst)
		
	l = len(lst_sent_np)
	print "l ", l, "inside"
	for i in reversed(range(l)):
		# print i
		# print "NP", lst_sent_np[i]
		# print lst_np_lvl_sent[i]
		male = 0
		female = 0

		if (len(lst_sent_np[i]) != 0):
			# print "@@@@@", len(lst_sent_np[i])
			ll = len(lst_sent_np[i])
			
			#reversed because have to check for ronoun from end of the sentence
			lst_rev = reversed(lst_sent_np[i])
			lst_rev_lvl = reversed(lst_np_lvl_sent[i])
			
			for j in reversed(range(ll)):

				if j not in malePronouns or j not in femalePronouns:
					break
					
				#flag is to check for the condition that if there is pronoun found 
				#in the sentence but no NNP present in the same sentence
				flag = 0
				# print "j-->", j
				# print ">>>",lst_np_lvl_sent, i , j
				L = lst_np_lvl_sent[i][j][1]
				W = lst_sent_np[i][j]
				# print "WWWW", W, L
				pos = get_pos(W)
				length = len(lst_sent_np[i])
				# print "pp", pos[0][1]
				if "PRP" in pos[0][1] and length > 1 and W not in pluralPronouns:
					print "here"
					
					if W in malePronouns:
						male = 1
					elif W in femalePronouns:
						female = 1
					# print "length------>", length
					k = j-1
					while k in reversed(range(ll)):

						W2 = lst_sent_np[i][k]
						L2 = lst_np_lvl_sent[i][k][1]
						pos = get_pos(W2)

						# print "w2 --->", W2
						gen = gender.getGenders([W2])
						print "gender----->", W2, gen[0][0],L, L2
						gen = gen[0][0]

						if "NN" in pos[0][1]:

							#if NNP found in same senetence before pronoun then flag = 1
							# flag = 1
							#if level of NNP and PRP are different then PRP can refer to NNP of same sent
							if L != L2:
								print "fire in the hole"
								if male == 1 and gen == "male":
									flag = 1
									idx1 = get_index(lst_np_hw_sentnum_npnum, W2, i)
									idx2 = get_index(lst_np_hw_sentnum_npnum, W, i)
									# print "idx"
									# print idx1
									# print idx2
									for l in lst_np_hw_sentnum_npnum:
										if l[2] == i and l[3] == idx2[3]:
											l[3] = idx1[3]
								elif female == 1 and gen == "female":
									flag = 1
									idx1 = get_index(lst_np_hw_sentnum_npnum, W2, i)
									idx2 = get_index(lst_np_hw_sentnum_npnum, W, i)
									# print "idx"
									# print idx1
									# print idx2
									for l in lst_np_hw_sentnum_npnum:
										if l[2] == i and l[3] == idx2[3]:
											l[3] = idx1[3]


								#if level of NNP and PRP are equal then have to look in upper statements
							else:
								print "\n prp_gdr1 called\n"
								lst_np_hw_sentnum_npnum = pronoun_gender(lst_sent_np, lst_np_hw_sentnum_npnum, 3, lst_sent_np_gender, i)
							
							#not used this break satetment yet
							#if more than one NNP present thn break fater finding one
							#otherwise all NNP of sentence before the PRP will cluster
							#in one single cluster
						if flag == 1:
							break

						k -= 1
				#flag = 0 that means NNP not found in the sentence so look up (sent above the curent sent) 
				if flag == 0 and "PRP" in pos[0][1]:
					# print "WWWW", W," FLAGGG",flag	
					print "\n pronoun_gender4 called \n"
					lst_np_hw_sentnum_npnum = pronoun_gender(lst_sent_np, lst_np_hw_sentnum_npnum, 3, lst_sent_np_gender, i)
					
	return lst_np_hw_sentnum_npnum		

def arrange_np_sent(lst_of_sent, lst_sent_np, lst_np_rel_sent):
	print "\n inside arrange np nad np_rel \n"
	n = len(lst_of_sent)

	for i in range(n):
		tmp = []
		for j in lst_sent_np[i]:
			idx = lst_of_sent[i].find(j)
			tmp.append((idx, j))
	
		tmp1 = []
		for j in sorted(tmp):
			tmp1.append(j[1])
		lst_sent_np[i] = tmp1

	# print ">>>>>", len(lst_np_rel_sent), lst_np_rel_sent

	for i in range(n):
		tmp = []
		for j in lst_np_rel_sent[i]:
			# print "j", j
			idx = lst_of_sent[i].find(j[0])
			tmp.append((idx, j))
	
		tmp1 = []
		for j in sorted(tmp):
			tmp1.append(j[1])
		lst_np_rel_sent[i] = tmp1

	# print "<<<<<<", lst_np_rel_sent

	return (lst_sent_np, lst_np_rel_sent)

plural_cluster = []

def corefer_plural_up(lst_of_sent, lst_sent_np, lst_np_rel_sent, start_sent, level_up, prp_word):
	l = start_sent

	while l >= 0:
		np_lst = lst_sent_np[l]
		flag = 0
		go = 0
		print "l---> ", l
		for i in reversed(np_lst):
			# print "LOL", i
			if i.lower() in pluralPronouns:
				# print "lol ", i
				start_sent = i
				go = 1

		if go == 1:
			for j in (range(level_up)):
				FLAG = 0
				n = l-j-1
				if l-j-1 >= 0:
					np_lst_up = lst_sent_np[n]
					print "n ", n , np_lst_up
					for k in range(len(np_lst_up)):
						w = np_lst_up[k]
						pos = get_pos(w)

						words = w.split()
						if len(words) > 1:
							for p in pos:
								if p[1] == "NNS":
									FLAG = 1
									idx1 = get_index(lst_np_hw_sentnum_npnum, w, n)
									idx2 = get_index(lst_np_hw_sentnum_npnum, prp_word, l)
									# print "idx"
									# print idx1
									# print idx2
									for ll in lst_np_hw_sentnum_npnum:
										if ll[2] == l and ll[3] == idx2[3]:
											ll[3] = idx1[3]
							if FLAG == 1:
								break

						elif len(words) == 1 and FLAG == 0 and pos[0][1] == "NNS":
							print "www", w
							# if pos[0][1] == "NNS":
							FLAG = 1
							idx1 = get_index(lst_np_hw_sentnum_npnum, w, n)
							idx2 = get_index(lst_np_hw_sentnum_npnum, prp_word, l)
							# print "idx"
							# print idx1
							# print idx2
							for ll in lst_np_hw_sentnum_npnum:
								if ll[2] == l and ll[3] == idx2[3]:
									ll[3] = idx1[3]

							if FLAG == 1:
								break
						else:
							c = 0
							print "realtion---->", lst_np_rel_sent[n]
							if k < len(np_lst_up):
								flag = 1
								lst = []
								lst_rel = []

								while k < len(np_lst_up):
									w = np_lst_up[k]
									p = (get_pos(w))[0][1]
									# print "k->", k , " ;word->", w , " ;pos tag-> ", p
									idx1 = get_index(lst_np_hw_sentnum_npnum, w, n)
									# print "########",lst_sent_np[n]
									# print "@@@@@@@@", lst_np_rel_sent[n]
									rel = lst_np_rel_sent[n][k][1]
									# print ">>>> rel >>>", lst_np_rel_sent[n][k][0], lst_np_rel_sent[n][k][1]

									if p == "NNP":
										lst.append(idx1[3])
										lst_rel.append(rel)
									
									c += 1 
									k += 1
					 		# print "cc", c, "k ", k
						 	if c > 1:
						 		FLAG = 1
						 		t = 0
						 		print lst_rel
						 		for rl in range(len(lst_rel)):
									if rl == 0 and lst_rel[rl] == "nsubj":
										continue
									elif rl > 0 and lst_rel[rl] == "conj" or lst_rel[rl] == "pobj":
										continue
									else:
										t = 1

						 		idx1 = get_index(lst_np_hw_sentnum_npnum, prp_word, l)
							 	
							 	if t == 0:	
							 		plural_cluster.append(prp_word)
							 		plural_cluster.append(idx1[3])
							 		plural_cluster.append(lst)

						print plural_cluster
						print "length ", len(np_lst_up)
						if k == len(np_lst_up):
							break
		l -= 1



def pronoun_plural(lst_of_sent, lst_sent_np, lst_np_rel_sent,lst_np_hw_sentnum_npnum):
	print "\n inside plural sentences\n"
	n = len(lst_of_sent)
	# print lst_np_rel_sent
	(lst_sent_np, lst_np_rel_sent) = arrange_np_sent(lst_of_sent, lst_sent_np, lst_np_rel_sent)

	for i in reversed(range(n)):
		print "------------------------------------------------------------------------------"
		for j in reversed(lst_sent_np[i]):
			print "jjjj->>>", j
			if j.lower() in pluralPronouns:
				FLAG = 0
				idx = lst_sent_np[i].index(j)
				print "plural idx :: ", idx, j

				print "\n left side of plural word ---> ", j 
				for k in (range(idx)):
					# print "k", k
					flag = 0
					w = lst_sent_np[i][k]
					pos = get_pos(w)
					
					#if NP have more than single word eg: the jury members
					words = w.split()
					if len(words) > 1:
						print "in here1", words, pos
						for p in pos:
							if p[1] == "NNS":
								# print "dasafsafasdfaa"
								FLAG = 1
								idx1 = get_index(lst_np_hw_sentnum_npnum, w, i)
								idx2 = get_index(lst_np_hw_sentnum_npnum, j, i)
								# print "idx"
								# print idx1
								# print idx2
								for l in lst_np_hw_sentnum_npnum:
									if l[2] == i and l[3] == idx2[3]:
										l[3] = idx1[3]
						if FLAG == 1:
							break
					elif len(words) == 1 and FLAG == 0 and pos[0][1] == "NNS":
						print "in here2"
						# if pos[0][1] == "NNS":
						FLAG = 1
						idx1 = get_index(lst_np_hw_sentnum_npnum, w, i)
						idx2 = get_index(lst_np_hw_sentnum_npnum, j, i)
						# print "idx"
						# print idx1
						# print idx2
						for l in lst_np_hw_sentnum_npnum:
							if l[2] == i and l[3] == idx2[3]:
								l[3] = idx1[3]

						if FLAG == 1:
							break
					else:
						if FLAG == 0:
							print "in here 3"
							c = 0
							# print "kkkk", k
							if k < idx:

								flag = 1
								lst = []
								lst_rel = []

								while k < idx:
									w = lst_sent_np[i][k]
									p = (get_pos(w))[0][1]
									# print "kkkk", k , " www", w , "pos tag", p
									idx1 = get_index(lst_np_hw_sentnum_npnum, w, i)
									
									rel = lst_np_rel_sent[i][k][1]
									# print ">>>> rel >>>", rel

									if p == "NNP":
										lst.append(idx1[3])
										lst_rel.append(rel)
										c += 1 
									k += 1

					 		# print "cc", c, "k ", k
						 	if c > 1:
						 		FLAG = 1
						 		t = 0
						 		print "lst_rel", lst_rel
						 		
						 		for rl in range(len(lst_rel)):
									if rl == 0 and lst_rel[rl] == "nsubj":
										continue
									elif rl > 0 and lst_rel[rl] == "conj" or lst_rel[rl] == "pobj":
										continue
									else:
										t = 1					 				

						 		idx1 = get_index(lst_np_hw_sentnum_npnum, j, i)
						 		# print "tttt", t
						 		if t == 0 and len(lst_rel) >= 2:
						 			print "append ->", j
							 		plural_cluster.append(j)
							 		plural_cluster.append(idx1[3])
							 		plural_cluster.append(lst)

						print "PC",plural_cluster

					if k == idx:
						break

				# print "  FLAG ", FLAG
				if FLAG == 0:
					print "\n going upwards \n"
					corefer_plural_up(lst_of_sent, lst_sent_np, lst_np_rel_sent, i, 3, j)

				print "\n right side of plural word ", j
				for k in range(idx+1, len(lst_sent_np[i])):
					w =  lst_sent_np[i][k]
					pos = get_pos(w)
					pos = pos[0][1]
					
					if pos  == "NNS":
						idx1 = get_index(lst_np_hw_sentnum_npnum, j, i)
						idx2 = get_index(lst_np_hw_sentnum_npnum, w, i)
						# print "idx"
						# print idx1
						# print idx2
						for l in lst_np_hw_sentnum_npnum:
							if l[2] == i and l[3] == idx2[3]:
								l[3] = idx1[3]
		print "--------------------------------------------------------------------------"
	return lst_np_hw_sentnum_npnum

# def get_final_result(lst_of_sent, lst_np_hw_sentnum_npnum):

	# for i in lst_np_hw_sentnum_npnum:
	# 	print i




if __name__ == "__main__":

	lst_of_sent = get_sentences("data6.txt")
	no_of_sent = len(lst_of_sent)
	print "no of sent: ", no_of_sent
	# for i in lst_of_sent:
	# 	print i,"\n"

	get_lst_sent_np_rel_lvl_head(lst_of_sent)

	''' printing list of NP per sentence '''
	# print "printing list of NP per sentence"
	# for i in lst_sent_np:
	# 	print i
	

	get_np_hw_np_rel_np_lvl(lst_sent_np)

	lst_np_hw_sentnum_npnum = get_lst_np_hw_sentnum_npnum(lst_np_hw_sent)	
	# print "lst_np_hw_sentnum_npnum\n"
	# for i in lst_np_hw_sentnum_npnum:
	# 	print i


	print "start\n"
	for i,j in enumerate(lst_np_hw_sentnum_npnum):
		print i, j


	for i in range(len(lst_np_rel_sent)):
		print i
		print "sent  ",lst_of_sent[i]
		print "np    ",lst_sent_np[i]
		print "np,hw ",lst_np_hw_sent[i]
		print "np,rl ",lst_np_rel_sent[i]
		print "np,lv ",lst_np_lvl_sent[i]


	lst_np_hw_sentnum_npnum = quotation_sieve(lst_of_sent, lst_np_hw_sentnum_npnum, lst_np_lvl_sent)
	# print "\ncluster_1 quotation_sieve\n"
	# for i,j in enumerate(lst_np_hw_sentnum_npnum):
		# print i, j

	# lst_np_hw_sentnum_npnum = exact_match(lst_sent_np, lst_np_hw_sentnum_npnum, 3)
	# print "\ncluster_2 exact_head_match_sieve\n"
	# for i,j in enumerate(lst_np_hw_sentnum_npnum):
	# 	print i, j

	# lst_sent_np_gender = get_gender_np_sent(lst_sent_np)
	# for i in range(len(lst_sent_np)):
	# 	print lst_sent_np[i]
	# 	print lst_sent_np_gender[i]

	# print "\npronoun_gender\n"
	# lst_np_hw_sentnum_npnum = pronoun_gender(lst_sent_np, lst_np_hw_sentnum_npnum, 2, lst_sent_np_gender, 0)
	# for i,j in enumerate(lst_np_hw_sentnum_npnum):
	# 	print i, j


	lst_np_hw_sentnum_npnum = pronoun_same_sent(lst_sent_np, lst_np_hw_sentnum_npnum, lst_np_lvl_sent)
	print "\n cluster 2\n"
	for i,j in enumerate(lst_np_hw_sentnum_npnum):
		print i, j

	lst_np_hw_sentnum_npnum = pronoun_plural(lst_of_sent, lst_sent_np, lst_np_rel_sent, lst_np_hw_sentnum_npnum)
	print "\n cluster 3\n"
	for i,j in enumerate(lst_np_hw_sentnum_npnum):
		print i, j

	# get_final_result(lst_of_sent, lst_np_hw_sentnum_npnum)

#x	# NP -> key noun phrase
#x	#	 -> Proper Nouns (nn etc)

	# herself like prp not in NP so catch them using pos



	# Gender API ->
	# 	None, NNP, PERSONNAME


#x  #update lst_sent_np

#do we they
#plural pronoun them do later
