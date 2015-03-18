import json, requests, ast
from sentimentanalysis import sentiment, cleaner
import sentimentanalysis.FullNNP as fullname
from textblob import TextBlob
from Gender import gender
from Ner import ner
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
singularPronounsOld = ["i", "me", "myself", "mine", "my", "yourself", "he", "him", "himself", "his", "she", "her", "herself", "hers", "her", "it", "itself", "its", "one", "oneself", "one's"]
singularPronouns = ["i", "me", "myself", "mine", "my", "yourself"]
singularPronounsNoMF = ["i", "me", "myself", "mine", "my"]
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
lst_sent_pos = []
lst_head = []


# get pos tags of a sentence
def get_pos(sent):
	lst_sent_pos = []
	text = nltk.word_tokenize(sent)
	lst_sent_pos = nltk.pos_tag(text)
	
	return lst_sent_pos


def fix_lst_np(list_of_nps, tmp_lst_pos):
	
	print "\n >>>>> fix np  <<<<<\n"
	print "##",list_of_nps
	print "##", tmp_lst_pos

	l = len(list_of_nps)

	# print "@@@@####", tmp_lst_pos
	i = 0
	# for i in range(l):
	while i < l:
		if i > 0 and i < l-1:
			# print "len", l, "ii",i
			# print "ii", list_of_nps[i]
			curr = list_of_nps[i]
			# pos = get_pos(list_of_nps[i])
			pos = tmp_lst_pos[i]
			# pos = pos[0][1]

			# print " >>>> i", i , " l ", l, list_of_nps
			prev = list_of_nps[i-1]
			next = list_of_nps[i+1]

			print ":prev->", prev, ":curr->",curr, ":next ->", next, ":pos->",pos

			if "NN" in pos:
				if curr in prev or curr in next:
					print "removing ", list_of_nps[i], "index ", i
					list_of_nps.pop(i)
					tmp_lst_pos.pop(i)
					i -= 1
					print tmp_lst_pos
			# print "len->", l, "ii->",i
		if i == l-1:
			curr = list_of_nps[i]
			prev = list_of_nps[i-1]

			if curr in prev:
				list_of_nps.pop(i)
				tmp_lst_pos.pop(i)

		l = len(list_of_nps)
		i += 1
		# print "iiii", i
	print "fixed ", list_of_nps
	print "fixed ", tmp_lst_pos

	return list_of_nps,tmp_lst_pos



# t = open('np.txt','w')
def get_lst_sent_np_rel_lvl_head(lst_of_sent):
	for i,j in enumerate(lst_of_sent):
		tree = make_tree(" ".join(j.split()))
		#list of head words for a sentence
		lst_head_tmp = sentiment.get_np_head(tree[0], tree[0])
		# print "head s ---->", lst_head_tmp
		
		#list of noun phrase for a senetnce
		list_of_nps= sentiment.get_np(tree[0], tree[0])


		print "@@@", list_of_nps
		# list_of_nps = fix_lst_np(list_of_nps, j)

		# res = str(i) + "|" + str(list_of_nps) + "\n"
		
		res = str(list_of_nps) + "\n"
		# t.write(res)

		#making tree for a sentence
		sentiment.tree_parse(tree[0])
		# print "^^^", list_of_nps
		
		#temporary lists containing NP, relation, Level; to append in the main list
		tmp_lst = []
		tmp_lst_rel = []
		tmp_lst_lvl = []
		tmp_lst_pos = []
		#k1 item in the list i.e. the NP 
		for k1 in (list_of_nps):
			#In sentiment.py function get_np returned empty lis1 if NNP not found 
			#so included False to indicate the absence of NP 
			# try :

			# if k1:
			# 	print "asdasd", k1[0]



			if len(k1[1]) > 0 and len(k1[0]) > 0 and k1[0][0] != False:	
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
					pos = k1[1][0]
					# print "poss", pos
					tmp_lst_rel.append(k2)
					tmp_lst_lvl.append(lvl)
					tmp_lst_pos.append(pos)
			# except:
			# 	continue
				
		# print "after", tmp_lst_pos
		tmp_list,tmp_lst_pos = fix_lst_np(tmp_lst, tmp_lst_pos)
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
			lst_sent_pos.append(tmp_lst_pos)
			lst_head.append(lst_head_tmp)


lst_sent_np_gender = []
#list of np with its head word per sentences
lst_np_hw_sent = []
#list of np with its rel per sentences
lst_np_rel_sent = []
#list of np with its lvl per sentences
lst_np_lvl_sent = []
lst_np_pos_sent = []

def get_np_hw_np_rel_np_lvl(lst_sent_np):
	for i in range(len(lst_sent_np)):
		# print lst_sent_np[i]
		#temporary list for (np, hw), (np, rel), (np, level) per sentence 
		temp = []
		tmp1 = []
		tmp2 = []
		tmp3 = []

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
					tmp3.append((lst_sent_np[i][j],lst_sent_pos[i][j]))
				# print vis
		lst_np_hw_sent.append(temp)
		lst_np_rel_sent.append(tmp1)
		lst_np_lvl_sent.append(tmp2)
		lst_np_pos_sent.append(tmp3)
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
	print "\n inside quotation sieve \n"
	for i,j in enumerate(lst_of_sent):
		if "\"," in j or "\" ," in j:
			# pos_tags = get_pos(j)
			pos_tags = lst_np_pos_sent[i]
			print "in here",pos_tags
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
def get_index(lst_np_hw_sentnum_npnum, k, sent_no, lookup):
	if lookup == 0:
		for i,j in enumerate(lst_np_hw_sentnum_npnum):
			if j[0] == k and j[2] == sent_no:		
				return j
	else:
		c = 0
		for i,j in enumerate(lst_np_hw_sentnum_npnum):
			if j[0] == k and j[2] == sent_no and c == 1:		
				return j
			if j[0] == k and j[2] == sent_no and c == 0:		
				c += 1

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
						idx1 = get_index(lst_np_hw_sentnum_npnum, k, l-1-i,0) 
						idx2 = get_index(lst_np_hw_sentnum_npnum, j, l,0)
						# print idx1, idx2
						lst_np_hw_sentnum_npnum = get_update(lst_np_hw_sentnum_npnum, idx1[3], idx2[3])
		l -= 1
	return lst_np_hw_sentnum_npnum

#returns list: items of list are list with 3 values each
#0. male/female 1.probability 2.no of docs
def get_gender_np_sent(lst_sent_np):
	lst_sent_np_gender = []
	lst = lst_sent_np

	for k,i in enumerate(lst):
		if len(i) != 0:
			tmp = []
			# print "i", i
			for j in  range(len(i)):
				# print i[j]
				t = (i[j]).split()
				if len(t) > 1:
					# i[j] = t[0]
					r = gender.getGenders(t)
					l = len(r)
					c = 0
					for g1,g2 in enumerate(r):
						c += 1
						if g2[0] != "unknown":
							# print "her-------->"
							tmp.append(g2)
							break 
					# print "cc", c, "ll", l
					if c == l:
						tmp.append(("unknown", 0))
				else:
					# print  "iiiii", i
					tmp.extend(gender.getGenders(t))
			lst_sent_np_gender.append(tmp)
		else:
			lst_sent_np_gender.append([False])
		# print "l1", len(i)
		# print "l2", len(lst_sent_np_gender[k])

	return lst_sent_np_gender


def np_last_name(lst_sent_np, lst_np_hw_sentnum_npnum, level_up, start_sent, last_name):
	print "\n inside np_last_name \n"
	ln = len(last_name)
	lst1 = [1 for x in range(ln)]
	last_name_dict = dict(zip(last_name,lst1))

	l = start_sent
	
	# while l >= 0:
	np_lst = lst_sent_np[l]
	flag = 0
	# print "np ", np_lst
	for i,j in enumerate(np_lst):
		w = j
		if w.lower() in pluralPronouns:
			continue
		if w.lower() in neutralPronouns:
			continue
		if w.lower() in singularPronounsNoMF:
			continue
		print "w ", w

		pos = lst_np_pos_sent[l][i][1]
		print "poss@@ @ ",pos

		if pos == "PRP":
			for j in (range(level_up)):
				if l-j-1 >= 0:
					np_lst_up = lst_sent_np[l-j-1]

					for k1,k2 in enumerate(np_lst_up):
						pos1 = lst_np_pos_sent[l-j-1][k1][1]
						if pos1 == "NNP":
							print "k2 ", k2
							np = k2.split()
							if len(np) > 1:
								for n in np:
									if n in last_name_dict:
										print "nnnnn", n
										flag = 1
										idx1 = get_index(lst_np_hw_sentnum_npnum, k2, l-j-1,0)
										idx2 = get_index(lst_np_hw_sentnum_npnum, w, l,0)
										print "idx"
										print idx1
										print idx2
										for ll in lst_np_hw_sentnum_npnum:
											if ll[2] == l and ll[3] == idx2[3]:
												ll[3] = idx1[3]
							else:
								if np[0] in last_name_dict:
									print "here i am", np[0]
									flag = 1
									idx1 = get_index(lst_np_hw_sentnum_npnum, k2, l-j-1,0)
									idx2 = get_index(lst_np_hw_sentnum_npnum, w, l,0)
									# print "idx"
									# print idx1
									# print idx2
									for ll in lst_np_hw_sentnum_npnum:
										if ll[2] == l and ll[3] == idx2[3]:
											ll[3] = idx1[3]
						if flag == 1:
							break
				if flag == 1:
					break

	# l -= 1


	return lst_np_hw_sentnum_npnum


def pronoun_gender(lst_sent_np, lst_np_hw_sentnum_npnum, level_up, lst_sent_np_gender, start_sent, last_name):
	# l = len(lst_sent_np) - 1 - start_sent
	print "\n inside pronoun gender \n"
	l = start_sent

	# while l >= 0:
	np_lst = lst_sent_np[l]
	inSingular = 0
	outflag = 0
	print "l===>", l
	for e,i in enumerate(np_lst):
		pos1 = lst_np_pos_sent[l][e][1]
		if pos1 != "PRP" or i.lower() in neutralPronouns:
			print i,"continue 1"
			continue
		if i.lower() in malePronouns or i.lower() in femalePronouns:
			
			print "ii---->", i

			prp = 0
			prp_female = 0
			prp_male = 0
		
			if i.lower() in femalePronouns:
				prp_female = 1
			elif i.lower() in malePronouns:
				prp_male = 1

			print i, prp_male, prp_female
			
			it = np_lst.index(i)
			if it != 0:
				for x in range(it-1):
					if np_lst[x].lower() in singularPronouns:
						inSingular = 1


			for j in (range(level_up)):
				if l-j-1 >= 0:
					flag = 0
					np_lst_up = lst_sent_np[l-j-1]
					gendr_lst_up = lst_sent_np_gender[l-j-1]
					
					print "######", np_lst_up
					print "######", lst_np_pos_sent[l-j-1]
					
					for k1,k2 in enumerate(np_lst_up):
						
						if inSingular == 1 and k1 == 0:
							print "k1---->", k1
							continue
						inSingular = 0

						# t = get_pos(k2)
						# pos = t[0][1]
						pos = lst_np_pos_sent[l-j-1][k1][1]
						gendr = gendr_lst_up[k1][0]
						print ">>",k2, pos, gendr



						if (prp_male == 1 and pos == "NNP" and gendr.decode('utf-8') == "male"):
							flag = 1
							outflag = 1
							print "m ", k2
							
							idx1 = get_index(lst_np_hw_sentnum_npnum, i, l, 0)
							idx2 = get_index(lst_np_hw_sentnum_npnum, k2, l-j-1, 0)
							# print idx1
							# print idx2
							lst_np_hw_sentnum_npnum = get_update(lst_np_hw_sentnum_npnum, idx1[3], idx2[3])
							for item in lst_np_hw_sentnum_npnum:
								print item
							
						elif(prp_female == 1 and pos == "NNP" and gendr.decode('utf-8') == "female"):
							flag = 1
							outflag = 1
							print "f ", k2
							print "i <->", i
							idx1 = get_index(lst_np_hw_sentnum_npnum, i, l, 0)
							idx2 = get_index(lst_np_hw_sentnum_npnum, k2, l-j-1, 0)
							# print idx1
							# print idx2
							lst_np_hw_sentnum_npnum = get_update(lst_np_hw_sentnum_npnum, idx1[3], idx2[3])
							# for i in lst_np_hw_sentnum_npnum:
							# 	print i
						
						if flag == 1:
							print "BREAK 1", i
							break
				else:
					print "BREAK 2", i
					break
				if flag == 1:
					break
		if outflag == 0:
			print "\ngoing foe last name with ", i, "\n"
			# print "<<<<<<<<<<<<<<<<<<<<<<talking bussiness>>>>>>>>>>>>>>>>>>>"
			lst_np_hw_sentnum_npnum = np_last_name(lst_sent_np, lst_np_hw_sentnum_npnum, level_up, start_sent, last_name)

		# l -= 1
	
	return lst_np_hw_sentnum_npnum

def pronoun_same_sent(lst_sent_np, lst_np_hw_sentnum_npnum, lst_np_lvl_sent, last_name):

	print "\n inside pronoun same sentence \n"
	lst1 = lst_sent_np

	lst = ast.literal_eval(str(lst1))

	lst_sent_np_gender = get_gender_np_sent(lst)
		
	l = len(lst_sent_np)
	print "l ", l, "inside"
	for i in reversed(range(l)):
		print i
		print "NP ", lst_sent_np[i]
		print "POs", lst_np_pos_sent[i]
		# print lst_np_lvl_sent[i]
		male = 0
		female = 0

		if (len(lst_sent_np[i]) != 0):
			# print "@@@@@", len(lst_sent_np[i])
			ll = len(lst_sent_np[i])
			
			for j in reversed(range(ll)):

				# print "upper", lst_sent_np[i][j]
				if lst_sent_np[i][j].lower() in pluralPronouns:
					print "HERE continue 1", lst_sent_np[i][j]
					continue

				# index = lst_sent_np[i].index(lst_sent_np[i][j])
				#flag is to check for the condition that if there is pronoun found 
				#in the sentence but no NNP present in the same sentence
				flag = 0
				# print "j-->", j
				# print ">>>",lst_np_lvl_sent, i , j
				L = lst_np_lvl_sent[i][j][1]
				W = lst_sent_np[i][j]
				print "WWWW", W, 
				# pos = get_pos(W)
				pos = lst_np_pos_sent[i][j][1]
				length = len(lst_sent_np[i])
				print "pp", lst_np_pos_sent[i][j]
				if "PRP" in pos and length > 1 and W not in pluralPronouns:

					print "here ", W
					
					if W in malePronouns:
						male = 1
					elif W in femalePronouns:
						female = 1
					# print "length------>", length
					ki = j-1
					print "j ", j , "k ", ki
					while ki in reversed(range(j)):
						print "kkkkk", ki

						W2 = lst_sent_np[i][ki]
						L2 = lst_np_lvl_sent[i][ki][1]
						# pos = get_pos(W2)
						pos1 = lst_np_pos_sent[i][ki][1]

						print "w2 --->", W2
					
						gen = lst_sent_np_gender[i][j]

						# tempw2 = W2.split()
						# if len(tempw2) > 1:
						# 	gen = gender.getGenders(tempw2)
						# 	for it in gen:
						# 		if it[0][0] != "None":
						# 			gen = it
						# else:
						# 	gen = gender.getGenders([W2])


						print "gender----->", W, W2, gen[0], pos1, L, L2

						gen = gen[0]


						if "NNP" in pos1:

							#if NNP found in same senetence before pronoun then flag = 1
							# flag = 1
							#if level of NNP and PRP are different then PRP can refer to NNP of same sent
							if L != L2:
								print "fire in the hole"
								if male == 1 and gen == "male":
									flag = 1
									idx1 = get_index(lst_np_hw_sentnum_npnum, W2, i, 0)
									idx2 = get_index(lst_np_hw_sentnum_npnum, W, i, 0)
									# print "idx"
									# print idx1
									# print idx2
									for l1 in lst_np_hw_sentnum_npnum:
										if l1[2] == i and l1[3] == idx2[3]:
											l1[3] = idx1[3]
								elif female == 1 and gen == "female":
									flag = 1
									idx1 = get_index(lst_np_hw_sentnum_npnum, W2, i, 0)
									idx2 = get_index(lst_np_hw_sentnum_npnum, W, i, 0)
									# print "idx", 0
									# print idx1
									# print idx2
									for l1 in lst_np_hw_sentnum_npnum:
										if l1[2] == i and l1[3] == idx2[3]:
											l1[3] = idx1[3]

								
								#if level of NNP and PRP are equal then have to look in upper statements
							else:
								print "\n prp_gdr1 called with ", lst_sent_np[i] ,"\n"
								print "$$$$$$$$$$$$$$$$$$$$$$$$$$", ki
								lst_np_hw_sentnum_npnum = pronoun_gender(lst_sent_np, lst_np_hw_sentnum_npnum, 3, lst_sent_np_gender, i, last_name)
								
							#not used this break satetment yet
							#if more than one NNP present thn break fater finding one
							#otherwise all NNP of sentence before the PRP will cluster
							#in one single cluster
						
						ki -= 1
						print "decreased k", ki

						if flag == 1:
							print "HERE BREAK 2"
							print "FLAGG ", flag
							break
			
				print "FLAGG ", flag
				#flag = 0 that means NNP not found in the sentence so look up (sent above the curent sent) 
				if flag == 0 and "PRP" in pos:
					print "WWWW", W," FLAGGG",flag	
					print "\n pronoun_gender4 called with ", lst_sent_np[i] ,"\n"
					lst_np_hw_sentnum_npnum = pronoun_gender(lst_sent_np, lst_np_hw_sentnum_npnum, 3, lst_sent_np_gender, i, last_name)
					
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

def np_plural_nnp(lst_of_sent, lst_sent_np, start_sent, level_up, last_name, lst_np_rel_sent):

	print "\n inside np_plural_nnp \n"
	l =  start_sent

	# while l >= 0:
	np_lst = lst_sent_np[l]
	
	for i in np_lst:
		if i.lower() in pluralPronouns:
			w = i
			idx1 = get_index(lst_np_hw_sentnum_npnum, w, l, 0)

			for j in (range(level_up)):
				FLAG = 0
				n = l-j-1
				if l-j-1 >= 0:
					np_lst_up = lst_sent_np[n]
					print "n ", n , np_lst_up

					for k in range(len(np_lst_up)):
						w1 = np_lst_up[k]
						pos = lst_np_pos_sent[n][k][1]

						c = 0
						print "realtion---->", lst_np_rel_sent[n]
						if k < len(np_lst_up):
							flag = 1
							lst = []
							lst_rel = []

							while k < len(np_lst_up):
								ww = np_lst_up[k]
								p = lst_np_pos_sent[n][k][1]
								# print "k->", k , " ;word->", w , " ;pos tag-> ", p
								idx2 = get_index(lst_np_hw_sentnum_npnum, ww, n, 0)
								# print "########",lst_sent_np[n]
								# print "@@@@@@@@", lst_np_rel_sent[n]
								rel = lst_np_rel_sent[n][k][1]
								# print ">>>> rel >>>", lst_np_rel_sent[n][k][0], lst_np_rel_sent[n][k][1]

								if p == "NNP":
									print "w1  ", w1
									print "rel ", rel
									if c == 0:
										if rel == "nsubj" or rel == "nn":
												print "if1",c,"rel ", rel, "w1  ", w
												lst.append(idx1[3])
												lst_rel.append(rel)
												c += 1
									elif c == 1: 
										if rel == "conj" or rel == "pobj"or rel == "nn":
											print "if2",c,"rel ", rel, "w1  ", w
											lst.append(idx1[3])
											lst_rel.append(rel)
											c += 1
									elif c > 1:
										if rel == "conj" or rel == "pobj":
											print "if3",c,"rel ", rel, "w1  ", w
											lst.append(idx1[3])
											lst_rel.append(rel)
											c += 1
									elif c > 1:
										if rel == "nn":
											break

									# c += 1 
								k += 1
						# print "cc", c, "k ", k
						if c > 1:
							# FLAG = 1
							t = 0
							print "RELATION", lst_rel
							print "NPPPPPPP", lst
							# for rl in range(len(lst_rel)):
							# 	if rl == 0 and lst_rel[rl] == "nsubj" or :
							# 		continue
							# 	elif rl > 0 and lst_rel[rl] == "conj" or lst_rel[rl] == "pobj" or lst_rel[rl] == "nn":
							# 		continue
							# 	else:
							# 		t = 1
						 	
						 	if t == 0:	
						 		# print "============================================================H!N3333"
						 		FLAG = 1
						 		temp = []
						 		temp.append(w)
						 		temp.append(idx1[3])
						 		temp.append(lst)
						 		# print "temppp", temp
						 		plural_cluster.append(temp)

						if FLAG == 1:
							break
					if k == len(np_lst_up):
								break
				if FLAG == 1:
					break
			print plural_cluster

		# l -= 1


def corefer_plural_up(lst_of_sent, lst_sent_np, lst_np_rel_sent, start_sent, level_up, last_name, prp_word):

	print "\n inside corefer plural pronoun\n"
	l = start_sent
	print "prp_word", prp_word
	while l >= 0:
		np_lst = lst_sent_np[l]
		flag = 0
		go = 0
		print "l---> ", l
		for i in reversed(np_lst):
			# print "LOL", i
			if i.lower() in pluralPronouns and i == prp_word:
				# print "lol ", i
				start_sent = i
				prp_word = i
				go = 1

		if go == 1:
			# print "go i ", i
			inflag = 0
			for j in (range(level_up)):
				FLAG = 0
				n = l-j-1
				if l-j-1 >= 0:
					np_lst_up = lst_sent_np[n]
					print "n ", n , np_lst_up
					for k in range(len(np_lst_up)):
						w = np_lst_up[k]
						wt = w
						wt = wt.split()
						if len(wt) > 1:
							pos = get_pos(w)
						else:
							pos = lst_np_pos_sent[n][k]

						# print "poss", pos
						# inflag = 0

						words = w.split()
						if len(words) > 1:
							print "------change-----"
							for p in pos:
								r = lst_np_rel_sent[n][k][1]
								if p[1] == "NNS" and r == "nsubj":
									print "NP => ", w
									# inflag = 1
									print "============================================================H!N1"
									FLAG = 1
									inflag = 1
									idx1 = get_index(lst_np_hw_sentnum_npnum, w, n, 0)
									idx2 = get_index(lst_np_hw_sentnum_npnum, prp_word, l, 0)
									# print "idx"
									# print idx1
									# print idx2
									for ll in lst_np_hw_sentnum_npnum:
										if ll[2] == l and ll[3] == idx2[3]:
											ll[3] = idx1[3]
							if FLAG == 1:
								break

						elif len(words) == 1 and FLAG == 0 and pos[1] == "NNS":
							print "pppp", pos[0]
							print "www", w
							# if pos[0][1] == "NNS":
							print "============================================================H!N2222"
							FLAG = 1
							inflag = 1
							idx1 = get_index(lst_np_hw_sentnum_npnum, w, n, 0)
							idx2 = get_index(lst_np_hw_sentnum_npnum, prp_word, l, 0)
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
									p = lst_np_pos_sent[n][k][1]
									# print "k->", k , " ;word->", w , " ;pos tag-> ", p
									idx1 = get_index(lst_np_hw_sentnum_npnum, w, n, 0)
									# print "########",lst_sent_np[n]
									# print "@@@@@@@@", lst_np_rel_sent[n]
									rel = lst_np_rel_sent[n][k][1]
									# print ">>>> rel >>>", lst_np_rel_sent[n][k][0], lst_np_rel_sent[n][k][1]

									if p == "NNP":
										# print "rel ", rel, "w1  ", w
										if c == 0:
											if rel == "nsubj" or rel == "nn":
												print "if1",c,"rel ", rel, "w1  ", w
												lst.append(idx1[3])
												lst_rel.append(rel)
												c += 1
										elif c == 1: 
											if rel == "conj" or rel == "pobj"or rel == "nn":
												print "if2",c,"rel ", rel, "w1  ", w
												lst.append(idx1[3])
												lst_rel.append(rel)
												c += 1
										elif c > 1:
											if rel == "conj" or rel == "pobj":
												print "if3",c,"rel ", rel, "w1  ", w
												lst.append(idx1[3])
												lst_rel.append(rel)
												c += 1
										elif c > 1:
											if rel == "nn":
												break
										# lst.append(idx1[3])
										# lst_rel.append(rel)
									
										# c += 1 
									k += 1
					 		print "cc", c, "k ", k
						 	if c > 1 and len(lst_rel) > 1:
						 		# FLAG = 1
						 		t = 0
						 		print "RELATION", lst_rel
						 		# for rl in range(len(lst_rel)):
									# if rl == 0 and lst_rel[rl] == "nsubj" or lst_rel[rl] == "nn":
									# 	continue
									# elif rl == 1 and lst_rel[rl] == "conj" or lst_rel[rl] == "pobj"or lst_rel[rl] == "nn":
									# 	continue
									# elif rl > 1 and lst_rel[rl] == "conj" or lst_rel[rl] == "pobj":
									# 	continue
									# else:
									# 	t = 1

						 		idx1 = get_index(lst_np_hw_sentnum_npnum, prp_word, l, 0)
							 	
							 	if t == 0:	
							 		print "============================================================H!N3333"
							 		FLAG = 1
							 		inflag = 1
							 		temp = []
							 		# print "jjj", prp_word
							 		temp.append(prp_word)
							 		temp.append(idx1[3])
							 		temp.append(lst)
							 		# print "temppp", temp
							 		plural_cluster.append(temp)

						print plural_cluster
						print "length ", len(np_lst_up)
						if k == len(np_lst_up):
							break
					if FLAG == 1:
						break

				print "====>> Flag", FLAG
				# print "------> inflag", inflag
				if FLAG == 1:
					break
					# print "@@@", np_lst_up
		if inflag == 0 and l != 0:
			print "ll", l
			print "<<<<<<<<<<<<<<<<<<<<<< talking business >>>>>>>>>>>>>>>>>>>"

			np_plural_nnp(lst_of_sent, lst_sent_np, l, level_up, last_name, lst_np_rel_sent)


		l -= 1



def pronoun_plural(lst_of_sent, lst_sent_np, lst_np_rel_sent,lst_np_hw_sentnum_npnum, last_name):
	print "\n inside plural sentences\n"
	n = len(lst_of_sent)
	# print lst_np_rel_sent
	(lst_sent_np, lst_np_rel_sent) = arrange_np_sent(lst_of_sent, lst_sent_np, lst_np_rel_sent)
	print "arranged\n", lst_sent_np

	for i in reversed(range(n)):
		print "------------------------------------------------------------------------------"
		for j in reversed(lst_sent_np[i]):
			# print "jjjj->>>", j
			if j.lower() in pluralPronouns:
				FLAG = 0
				idx = lst_sent_np[i].index(j)
				print "plural word idx :: ", idx, j

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
							r = lst_np_rel_sent[i][k][1]
							if p[1] == "NNS" and r == "nsubj":
								# print "dasafsafasdfaa"
								FLAG = 1
								idx1 = get_index(lst_np_hw_sentnum_npnum, w, i, 0)
								idx2 = get_index(lst_np_hw_sentnum_npnum, j, i, 0)
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
						idx1 = get_index(lst_np_hw_sentnum_npnum, w, i, 0)
						idx2 = get_index(lst_np_hw_sentnum_npnum, j, i, 0)
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
									idx1 = get_index(lst_np_hw_sentnum_npnum, w, i, 0)
									
									rel = lst_np_rel_sent[i][k][1]
									# print ">>>> rel >>>", rel

									if p == "NNP":
										if c == 0:
											if rel == "nsubj" or rel == "nn":
												print "if1",c,"rel ", rel, "w1  ", w
												lst.append(idx1[3])
												lst_rel.append(rel)
												c += 1
										elif c == 1: 
											if rel == "conj" or rel == "pobj"or rel == "nn":
												print "if2",c,"rel ", rel, "w1  ", w
												lst.append(idx1[3])
												lst_rel.append(rel)
												c += 1
										elif c > 1:
											if rel == "conj" or rel == "pobj":
												print "if3",c,"rel ", rel, "w1  ", w
												lst.append(idx1[3])
												lst_rel.append(rel)
												c += 1
										elif c > 0:
											if rel == "nn":
												break
									k += 1

					 		# print "cc", c, "k ", k
						 	if c > 1:
						 		FLAG = 1
						 		t = 0
						 		print "lst_rel", lst_rel
						 		
						 		# for rl in range(len(lst_rel)):
									# if rl == 0 and lst_rel[rl] == "nsubj" or lst_rel[rl] == "nn":
									# 	continue
									# elif rl == 1 and lst_rel[rl] == "conj" or lst_rel[rl] == "pobj" or lst_rel[rl] == "nn":
									# 	continue 
									# elif rl > 0 and lst_rel[rl] == "conj" or lst_rel[rl] == "pobj":
									# 	continue
									# else:
									# 	t = 1					 				

						 		idx1 = get_index(lst_np_hw_sentnum_npnum, j, i, 0)
						 		# print "tttt", t
						 		if t == 0 and len(lst_rel) >= 2:
						 			# print "append fire in the hole ->", j
						 			temp = []
							 		temp.append(j)
							 		temp.append(idx1[3])
							 		temp.append(lst)
							 		# print "temppp", temp
							 		plural_cluster.append(temp)

						print "PC",plural_cluster

					if k == idx:
						break

				# print "  FLAG ", FLAG
				if FLAG == 0:
					print "\n going upwards \n"
					corefer_plural_up(lst_of_sent, lst_sent_np, lst_np_rel_sent, i, 3, last_name, j)

				# print "\n right side of plural word ", j
				# for k in range(idx+1, len(lst_sent_np[i])):
				# 	print "right"
				# 	w =  lst_sent_np[i][k]
				# 	# pos = get_pos(w)

				# 	pos = lst_np_pos_sent[i][k]
				# 	print "posss", pos
				# 	pos = pos[0][1]
					
				# 	if pos  == "NNS":
				# 		print "right => fire in the hole ----> ", w, pos
				# 		idx1 = get_index(lst_np_hw_sentnum_npnum, j, i, 0)
				# 		idx2 = get_index(lst_np_hw_sentnum_npnum, w, i, 0)
				# 		# print "idx"
				# 		# print idx1
				# 		# print idx2
				# 		for l in lst_np_hw_sentnum_npnum:
				# 			if l[2] == i and l[3] == idx2[3]:
				# 				l[3] = idx1[3]
		print "--------------------------------------------------------------------------"
	return lst_np_hw_sentnum_npnum


#first person pronoun refer to the NNP having relation as nsubj
def corefer_frst_person(lst_of_sent, lst_sent_np, lst_np_hw_sentnum_npnum,lst_np_rel_sent, start_sent, level_up):
	
	print "\n inside corefer first person \n"
	l = start_sent

	for i in lst_sent_np:
		print i

	prev = False
	curr = False

	while l >= 0:
		np_lst = lst_sent_np[l]
		lookup = 0

		for i1,i2 in enumerate((np_lst)):
			if i2.lower() in singularPronounsNoMF:
				w = i2
				print "w", w
				curr = w
				if curr == prev:
					lookup = 1
				else:
					lookup = 0

				for j in (range(level_up)):
					FLAG = 0
					n = l-j-1
					if n >= 0:
						print "n-->", n
						np_lst_up = lst_sent_np[n]
						print "np_up ", np_lst

						for k in reversed(range(len(np_lst_up))):
							w1 = np_lst_up[k]

							pos = lst_np_pos_sent[n][k][1]
							rel = lst_np_rel_sent[n][k][1]
							print "w1 ", w1
							print "pos ", pos
							print "rel ", rel
						
							if pos == "NNP" and rel == "nsubj":
								prev = curr
								print "i1---->", i1
								print "w", w
								print "k----->", k
								print "w1 ", w1
								FLAG = 1
								idx1 = get_index(lst_np_hw_sentnum_npnum, w, l, lookup)
								idx2 = get_index(lst_np_hw_sentnum_npnum, w1, n, 0)
								print "idx"
								print idx1
								print idx2
								for ll in lst_np_hw_sentnum_npnum:
									if ll[2] == l and ll[3] == idx1[3]:
										ll[3] = idx2[3]

								for i in lst_np_hw_sentnum_npnum:
									print i
								
							if FLAG == 1:
								break
					if FLAG == 1:
						break	
 
		l -= 1

	return lst_np_hw_sentnum_npnum




def pronoun_frst_person(lst_of_sent, lst_sent_np, lst_np_hw_sentnum_npnum,lst_np_rel_sent):

	print "\n inside pronoun first prson \n"
	for i in lst_np_rel_sent:
		print i

	l = len(lst_of_sent) - 1

	while(l >= 0):
		np_lst = lst_sent_np[l]
		flag = 0
		for i,w in enumerate(np_lst):
			if w.lower() in singularPronounsNoMF:

				w1 = w
				for idx in range(i):
					w2 = np_lst[idx]
					# print "w2222222", w2
					# pos = get_pos(w2)
					pos = lst_np_pos_sent[l][idx][1]
					rel = lst_np_rel_sent[l][idx][1]
					print "posss", pos, "relll", rel

					if pos == "NNP" and rel == "nsubj":
						flag = 1
						print "w1",w1,"w2",w2
						idx1 = get_index(lst_np_hw_sentnum_npnum, w2, l, 0)
						idx2 = get_index(lst_np_hw_sentnum_npnum, w1, l, 0)
						print "idx"
						print idx1
						print idx2
						for ll in lst_np_hw_sentnum_npnum:
							if ll[2] == l and ll[3] == idx2[3]:
								ll[3] = idx1[3]
					if flag == 1:
						break
		if flag == 0:
			print ">>>>>>>>>>>talking business First<<<<<<<<<<<<<<<<"
			lst_np_hw_sentnum_npnum = corefer_frst_person(lst_of_sent, lst_sent_np, lst_np_hw_sentnum_npnum,lst_np_rel_sent, l, 3)
		l -= 1 

	return lst_np_hw_sentnum_npnum


def pronoun_sec_person(lst_of_sent, lst_sent_np, lst_np_hw_sentnum_npnum):

	print "\n inside second pronoun\n"
	l = len(lst_of_sent)-1
	print "type", type(l)

	while l >= 0:
		np_lst = lst_sent_np[l]
		for idx in range(len(np_lst)):
			w1 = np_lst[idx]
			if w1.lower() in secondPersonPronouns:
				print idx, np_lst[idx]
	
				for k in reversed(range(idx)):
					w2 =  np_lst[k]
					pos = get_pos(w2)
					pos = pos[0][1]
					if pos == "NNP":
						print "fire in the hole", np_lst[k]
						idx1 = get_index(lst_np_hw_sentnum_npnum, w1, l, 0)
						idx2 = get_index(lst_np_hw_sentnum_npnum, w2, l, 0)
						print "idx"
						print idx1
						print idx2
						for l in lst_np_hw_sentnum_npnum:
							if l[2] == i and l[3] == idx2[3]:
								l[3] = idx1[3]

		l -= 1
	return lst_np_hw_sentnum_npnum


def get_final_result(lst_of_sent, lst_np_hw_sentnum_npnum):

	print "\n inside get final result \n"

	lst_of_sent = [x.rstrip('.') for x in lst_of_sent]
	lst_of_sent = [" "+x+" " for x in lst_of_sent]

	for i in (plural_cluster):
		# print i
		w = i[0]
		cluster_id = i[1]
		# print lst_np_hw_sentnum_npnum[cluster_id]
		s = ""
		for j in i[2]:
			coref_w = lst_np_hw_sentnum_npnum[j][0] 
			# print j, lst_np_hw_sentnum_npnum[j][0]
			s += " "+coref_w + " "
		# print i[2]
		s = s[:-1]
		sn = lst_np_hw_sentnum_npnum[cluster_id][2]
		lst_of_sent[sn] = lst_of_sent[sn].replace(w,s)


	id_dict = {}
	
	k = -1
	lst = sorted(lst_np_hw_sentnum_npnum, key = operator.itemgetter(3), reverse = False) 
	# for i in lst:
	# 	print i
	for i in lst:
		if i[3] not in id_dict:
			k = i[3]
			id_dict[k] = i[0]

	# for k,v in id_dict.items():
	# 	print k,v

	for j,i in enumerate(lst_np_hw_sentnum_npnum):
		sn = i[2]
		w = " "+i[0]+" "
		idn = i[3]
		rw = " "+id_dict[idn]+" "
		# print sn ,w, rw
		# print "prev-->", lst_of_sent[sn]
		lst_of_sent[sn] = lst_of_sent[sn].replace(w,rw,1)
		# print "curr-->", lst_of_sent[sn]
		# print

	# for i in lst_of_sent:
	# 	print i
	# print

	# print "lenn", len(plural_cluster)


	lst_of_sent = [x.strip() for x in lst_of_sent]
	lst_of_sent = [x+'.' for x in lst_of_sent]
	# for i in lst_of_sent:
	# 	print i

	return lst_of_sent


def final_process(lst_of_sent, lst_sent_np, lst_np_hw_sentnum_npnum, window):
	print "\n inside final process \n"

	l = len(lst_sent_np)-1
	lst_np_hw_sentnum_npnum = sorted(lst_np_hw_sentnum_npnum, key = operator.itemgetter(2), reverse = False) 

	while l >= 0:
		np_lst = lst_sent_np[l]
		for i in np_lst:
			c = np_lst.count(i)
			if c > 1:
				idx = np_lst.index(i)
				temp_l = np_lst[idx+1:]
				idx = temp_l.index(i)

		l -= 1

	while l >= 0:
		np_lst = lst_sent_np[l]

		for idx,i in enumerate(np_lst):
			m_p = 0
			f_p = 0
			p_p = 0
			w = i
			idx1 = get_index(lst_np_hw_sentnum_npnum, w, l,0)
			# print "dddd",lst_np_pos_sent[l][idx] 
			if lst_np_pos_sent[l][idx][1] == "PRP":

				if i.lower() in malePronouns:
					m_p = 1
				elif i.lower() in femalePronouns:
					f_p = 1
				elif i.lower() in pluralPronouns:
					p_p = 1

				# print "w ",w, m_p, f_p, p_p

				for j in (range(window)):
					FLAG = 0
					n = l-j-1
					if n >= 0:
						np_lst_up = lst_sent_np[n]

						for k,w1 in enumerate(np_lst_up):
							m_p1 = 0
							f_p1 = 0
							p_p1 = 0

							idx2 = get_index(lst_np_hw_sentnum_npnum, w1, n,0)

							if idx1[3] != idx2[3]:
								# print "idx1", idx1
								# print "idx2", idx2

								if w1.lower() in malePronouns:
									m_p1 = 1
								elif w1.lower() in femalePronouns:
									f_p1 = 1
								elif w1.lower() in pluralPronouns:
									p_p1 = 1

								# print "w1", w1, m_p1, f_p1, p_p1

								if m_p == 1 and m_p1 == 1 or f_p == 1 and f_p1 == 1 or p_p == 1 and p_p1 == 1:
									# print "got you"
									FLAG = 1
									for ll in lst_np_hw_sentnum_npnum:
										if ll[2] == l and ll[3] == idx1[3]:
											ll[3] = idx2[3]
									# print lst_np_hw_sentnum_npnum
					# print
					if FLAG == 1:
						break
		l -= 1

	return lst_np_hw_sentnum_npnum


if __name__ == "__main__":

	last_name = open("/media/shive/New Volume/Untitled Folder/Coreference/LastName/NameListV02.txt").read().split("\n")
	# last_name = " ".join(last_name)
	last_name = [x.rstrip("\r") for x in last_name]
	# for i in last_name:
	# 	print i

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


	# lst_sent_np_gender = get_gender_np_sent(lst_sent_np)
	# for i in range(len(lst_sent_np)):
	# 	print lst_sent_np[i]
	# 	print lst_sent_np_gender[i]

	for i in range(len(lst_np_rel_sent)):
		print i
		print "sent  ",lst_of_sent[i]
		print "np    ",lst_sent_np[i]
		print "np,hw ",lst_np_hw_sent[i]
		print "np,rl ",lst_np_rel_sent[i]
		print "np,lv ",lst_np_lvl_sent[i]
		print "np,pos",lst_np_pos_sent[i]
		# print "np,gen",lst_sent_np_gender[i]


	lst_np_hw_sentnum_npnum = quotation_sieve(lst_of_sent, lst_np_hw_sentnum_npnum, lst_np_lvl_sent)
	print "\ncluster_1 quotation_sieve\n"
	for i,j in enumerate(lst_np_hw_sentnum_npnum):
		print i, j

	# lst_np_hw_sentnum_npnum = exact_match(lst_sent_np, lst_np_hw_sentnum_npnum, 3)
	# print "\ncluster_2 exact_head_match_sieve\n"
	# for i,j in enumerate(lst_np_hw_sentnum_npnum):
	# 	print i, j


	# print "\npronoun_gender\n"
	# lst_np_hw_sentnum_npnum = pronoun_gender(lst_sent_np, lst_np_hw_sentnum_npnum, 2, lst_sent_np_gender, 0, last_name)
	# for i,j in enumerate(lst_np_hw_sentnum_npnum):
	# 	print i, j


	lst_np_hw_sentnum_npnum = pronoun_same_sent(lst_sent_np, lst_np_hw_sentnum_npnum, lst_np_lvl_sent, last_name)
	print "\n cluster 2\n"
	for i,j in enumerate(lst_np_hw_sentnum_npnum):
		print i, j

	lst_np_hw_sentnum_npnum = pronoun_plural(lst_of_sent, lst_sent_np, lst_np_rel_sent, lst_np_hw_sentnum_npnum, last_name)
	print "\n cluster 3\n"
	for i,j in enumerate(lst_np_hw_sentnum_npnum):
		print i, j

	# # lst_np_hw_sentnum_npnum = pronoun_sec_person(lst_of_sent, lst_sent_np, lst_np_hw_sentnum_npnum)
	# # print "\ncluster_4 quotation_sieve\n"
	# # for i,j in enumerate(lst_np_hw_sentnum_npnum):
	# # 	print i, j

	lst_np_hw_sentnum_npnum = pronoun_frst_person(lst_of_sent, lst_sent_np, lst_np_hw_sentnum_npnum,lst_np_rel_sent)
	print "\ncluster 4 \n"
	for i,j in enumerate(lst_np_hw_sentnum_npnum):
		print i, j


	lst_np_hw_sentnum_npnum = final_process(lst_of_sent, lst_sent_np, lst_np_hw_sentnum_npnum, 3)
	print "\ncluster 5 \n"
	for i,j in enumerate(lst_np_hw_sentnum_npnum):
		print i, j


	''' Final Result '''
	print "\n final result\n"
	for i in lst_of_sent:
		print i
	print
	lst_of_sent = get_final_result(lst_of_sent, lst_np_hw_sentnum_npnum)
	for i in lst_of_sent:
		print i


	print "calling NER" 

	print ner.final_NER("Orange")

	# text = "google"

#x	# NP -> key noun phrase
#x	#	 -> Proper Nouns (nn etc)

	# herself like prp not in NP so catch them using pos



	# Gender API ->
	# 	None, NNP, PERSONNAME


#x  #update lst_sent_np

#x 		do we they
#x 		plural pronoun them do later
#x 		correct the methon fix np 

#x     """"""""	SOLVED """"" np_plural_nnp  hard rule for only 2 NNP there can be 3 or more nnp in continuation
#x 							rule for 2 bacause in example "President Obama and Prime Minister Modi are coming to india. 
#x 							They will be visiting to places."
#x 	3rd nno i.e india is also NNP but shold not be coreferred by they

#x 		John and Jonna are playing. he is a god player. He never give up. He give himself a new record to break.
#x 		in above eg himselg was not corefering John solved by removing break condition in the function pronoun_gender

