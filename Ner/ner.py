import json, requests, ast ,re
from sentimentanalysis import  cleaner, sentiment
import sentimentanalysis.FullNNP as fullname
from collections import Counter
from city_name_dict import *
from location_dictionary import *
from and_condition import *
# from time import tag
import time as tag 
import time as extract 
import sys
#coding: utf8 
import os
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('utf-8')
nnp_list_list = []
a = []
done = []
location_list = []
name_list = []
output_location = []
output_lastname = []
remaining = []
list_dictionary = []
def extract_curr(text):

    c101 = '(\-?\$\d{1,4}\.\d{1,2}\s(billion|Billion|million|Million|trillion|Trillion))'
    c102 = '\-?\$\d{1,4}'
    c104 = '((Rs)\s*\d+\s*(crore|lakh|thousand|rupees|Crore|Lakh|Thousand|Rupees))'
    c105 = '(\-?\$\d+\s(billion|Billion|million|Million|trillion|Trillion|dollars))'
    c106 = '((Rs)\s*\d+)'
    res = []
    
    bigger = False

    if bigger == False:
        cm105 = re.findall(c105, text)
        for x in cm105:
            # print "105" 
            res.append(x[0])
            bigger = True

        if bigger == False:
            cm102 = re.findall(c102, text)
            for x in cm102:
                # print "102" 
                res.append(x)
                # bigger = True

        bigger = False

    if bigger == False:
        cm104 = re.findall(c104, text)
        for x in cm104:
            # print "104"
            res.append(x[0])
            bigger = True

        if bigger == False:
            cm106 = re.findall(c106, text)
            for x in cm106:
                # print "106"
                res.append(x[0])
                bigger = True

        bigger = False 

    if bigger == False:
        cm101 = re.findall(c101, text)
        for x in cm101:
            # print "101"
            res.append(x[0])
            bigger = True

    

    # if bigger == False:
    #     cm103 = re.findall(c103, text)
    #     for x in cm103:
    #         print "103"
    #         # print '..', x[0]
    #         res.append(x[0])
    #         bigger = True

    return res


def extract(text):

    # text = text.lower() 
    text = text.replace(',' ,"")
    exp = "(next|last|coming|upcoming|past)"
    durs = "(years|days|week|months|quarters|quarter|month|year|day|minutes|minute|seeconds|second)"
    r8 = exp + "\s(\d*)\s" + durs # Next 120 days

    month = '(january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec|January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)'
    terms = '(tomorrow|today|yesterday|tonight|fiscal year|afternoon|noon|evening|morning|night|dawn|dusk)'
    days = '(monday|tuesday|wednesday|thrusday|friday|saturday|sunday|Monday|Tuesday|Wednesday|Thrusday|Friday|Saturday|Sunday)'
    year = "((18|19|20)\d{2})"
    date_no = "\d{0,2}(th|st|nd|rd|,)?"

    # r103= "\d{0,2}(th)?\s("+month+")\s((18|19|20)\d{2})" ## 20th Jan 2012 and similar
    # r3 = "(" + monthx + ")\s" + date_no ## Jan 10
    # r4 =  date_no + "\s(" + monthx + ")" ## 10 Jan
    r5 = year 
    # r6 = "(" + monthx + ")" 
    # r7 = r6 + "\s" + r5
    r61 = month
    r88 = '(\d+/\d+/\d+)'
    
    r107 = '(\d+[t|s|n][h|t|d]\s*'+month + ')'
    r101 = '\d{2}[-]\d{2}[-]\d{2,4}'
    r102 = '\d\d\s[A-Za-z][A-Za-z][A-Za-z]\s\d\d\d\d'
    r103 = '(((\d{1,2}[t|s|n][h|t|d]\s*'+month+'\s*\,*\s*\d+)))'
    # r111 = '((18|19|20)\d{2})'
    r104 = '(' + month + '\s* \d+[t|s|n][h|t|d]\,*\s*\,*\d+ )' 
    r106 = '(' + month + '\s* \d+[t|s|n][h|t|d]\s*)'
    r117 = '(' +month + '\s*\d+ )'
    r11 = terms 

    r108 = '(\d\d\s*' + durs + ')'
    r109 = '(((1?[0-9]|2[0-3]):[0-5][0-9])\s*[a|p][m])'
    r333 = days
    res = []
    
    bigger = False

    if bigger == False:
        m333 = re.findall(r333, text)
        # print m333[0]
        try :
            res.append(m333[0])
        except:
            bigger = False 
    # print res , "ppp"

    if bigger == False:
        m117 = re.findall(r117, text)
        for x in m117:
            # print "109" 
            res.append(x[0])

    if bigger == False:
        m103 = re.findall(r103, text)
        for x in m103:
            # print "103"
            res.append(x[0])
            bigger = True
        if bigger == False:
            m107 = re.findall(r107, text)
            for x in m107:
                # print "107"
                res.append(x[0])
                # bigger = True'''
        bigger = False 

    
    # if bigger == False:
    #         m111 = re.findall(r111, text)
    #         for x in m111:
    #             print "111" 
    #             res.append(x[0])
    #             # bigger = True
    if bigger == False:
            m109 = re.findall(r109, text)
            for x in m109:
                # print "109" 
                res.append(x[0])
                # bigger = True
    
    if bigger == False:
            m11 = re.findall(r11, text)
            for x in m11:
                # print "11" 
                res.append(x)
                # bigger = True

    if bigger == False:
            m101 = re.findall(r101, text)
            for x in m101:
                # print "101" 
                res.append(x)
                # bigger = True
    if bigger == False:
        m88 = re.findall(r88 , text)
        for x in m88:
            # print "88"
            res.append(x)
            # bigger = True



    if bigger == False:
        m104 = re.findall(r104, text)
        for x in m104:
            # print "104"
            res.append(x[0])
            bigger = True

        if bigger == False:
            m106 = re.findall(r106, text)
            for x in m106:
                # print "106"
                res.append(x[0])
                bigger = True

        bigger = False


    if bigger == False:
        m102 = re.findall(r102, text)
        for x in m102:
            # print "102"
            res.append(x)
            # print x
            bigger = True
    
    if bigger == False:
        m108 = re.findall(r108, text)
        for x in m108:
            # print "108" 
            res.append(x[0])
            # bigger = True
    
    return res

def number_presence(val):
    m = re.search('\d+', val)
    
    if m:
        return 1

def find_word_in_sent(sent, alist):
    sent = sent.lower()
    sent = sent.split(' ')
    result = []
    for ele in alist:
        if ele in sent:
            ind = sent.index(ele)
            string = ''
            if number_presence(sent[ind-1]) == 1:
                string = string +' ' + sent[ind-1]

            string = string +' ' + sent[ind]

            if number_presence(sent[ind+1]) == 1:
                string = string+ ' ' + sent[ind+1]
            string = string.strip()
            # print string
            result.append(string)

    return result


#Navigation dictionaries to find child dictionary of our NNP in question
def recursive_dict(dictum, nnp):
    # print dictum
    dictret = []
    if type(dictum) == dict:
        if dictum['node'].find(nnp)>0:
            dictret.append(dictum['node'])
            if len(recursive_dict(dictum['subTree'],nnp))>0:
                dictret.append(recursive_dict(dictum['subTree'],nnp))       
        else:
            if len(recursive_dict(dictum['subTree'],nnp))>0:
                dictret.append(recursive_dict(dictum['subTree'],nnp))
    else:
        for dictrow in dictum:
            if dictrow['node'].find(nnp)>0:
                dictret.append(dictrow['node'])
                if len(recursive_dict(dictrow['subTree'],nnp))>0:
                    dictret.append(recursive_dict(dictrow['subTree'],nnp))
                              
            else:
                if len(recursive_dict(dictrow['subTree'],nnp))>0:
                    dictret.append(recursive_dict(dictrow['subTree'],nnp))

    return dictret

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


def breakmultilist(l):
    outlist = []
    if len(l) == 0:
        outlist = l
    elif len(l)==1 and type(l[0]) == list:
        outlist = breakmultilist(l[0])
    elif len(l)>1 and type(l[0]) == list:
        outl = []
        for each in l:
            outl.append(breakmultilist(each))
        outlist = outl
    else:
        outlist = l
    return outlist

def cleannode(x):
    x = x[x.find('->')+2:]
    # x = x.split('(')[0]
    return x

def clean_actor(acters):
    actor_list=[]
    for actor in acters:
        # print actor
        if type(actor)!=list:
            actor=cleannode(actor).strip()
            actor_list.append(actor)
        else:
            actor=breakmultilist(actor)
            actor_list.extend(clean_actor(actor))
    return actor_list

####All NNP and NNS
def all_nnps(tree):
    all_nnp=[]
    keyword_pos=['NNP','NNS']
    for key in keyword_pos:
        actor_list=breakmultilist(recursive_dict(tree[0],key))
        # print actor_list
        clean_name=clean_actor(actor_list)
        all_nnp.append(clean_name)
    return all_nnp


def combine ( list1 , rel ):
    ans = []
    for i in list1:
        ans.append(i)

    ans.append(rel)

    return ans 


#####Build Dictionary for every sentence and its corresponding Noun Phrase , POS , relation#########
def build_dictionary(fo):
    ans = {}
    for i,each in enumerate(fo) :
        bb = []
        tree = make_tree(each)
        # print '__________________________________________________'
        # sentiment.tree_parse(tree[0])
        
        list1 = all_nnps(tree)
        # print list1 , "??"
        for ac in list1 :
            for li in ac:
                # print "li" ,li 
                if ( li != "") :
                    s = re.findall ('nn', li )
                    if ( len(s) == 0):
                        relation  = li.split('(', 1)[1].split(')')[0]
                        # print tree[0] ,li ,">>>>>>>"

                        ll = (fullname.fullnnp(tree[0],li))
                        # print ll ,"ll"
                        bb.append(combine ( ll , relation))

        ans[each] = bb

    return ans 




#######Inserting the elements in the dictionary in proper format#####
def insert_dictionary (final_dic , dic, fo) :
    for index , each in enumerate(fo):
        final_dic[index] = {}
        if (len(dic[each])) > 0:
            for i,j in enumerate(dic[each]):
                final_dic[index][i] = {}
                final_dic[index][i]['NounPhrase'] = dic[each][i][0][0].encode('utf-8')
                final_dic[index][i]['POS'] = dic[each][i][1][0].encode('utf-8')
                final_dic[index][i]['Relation'] = dic[each][i][2].encode('utf-8')

    return final_dic


#####Print the dictionary in proper format##########
def print_dictionary(final_dic):
    nnp_list_list = []
    for i , u in enumerate(final_dic):
        # print "Sentence Number :" , i
        nnp_list=[]
        for j,v in enumerate(final_dic[i]):
            nnp_info={}
            nnp_info['NounPhrase']=final_dic[i][j]['NounPhrase']
            nnp_info['POS']=final_dic[i][j]['POS']
            nnp_info['Relation']=final_dic[i][j]['Relation']
            nnp_list.append(nnp_info)

        nnp_list_list.append(nnp_list)

    # print nnp_list_list 
    return nnp_list_list

def location(address,key):
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address='
    api_key = str(key)
    fullurl = url + address + '&key=' + api_key
    r = requests.get(fullurl)

    data = json.loads(r.text)
    
    if len(data['results'])!=0:
        add = data['results'][0]['address_components']
        res = {}
        res['status']=data['status']
        return res , add 
    else:
        add = 'NULL'
        res={}
        res['status']=data['status']
        return res , add


def find_location(list_dictionary,done):
    a = []
    # if s not in done :
    #             try :
    #                 ff = City_name_changes[s]
    #             except:
    #                 ff = s
                
    #             try :
    #                 if ( dic_location[ff]  == 1):
    #                     a.append(ff)
                
    #             except :
    #             ###Output Files Address
                    
    #                 APi_Result=open('OutputV07.txt','w')
    #                 ###########Key files
    #                 key_detail_list=open('Api_Keys.txt','r').read().split('\n')
    #                 key_id=0
    #                 key=str(key_detail_list[key_id])
                    
    #                 # print ff 
    #                 result=[]
    #                 keyList=[]
    #                 res =location(ff.encode('utf-8'),key)
                     
    #                 # print res , "???"
    #                 if res[0]['status'] == 'OK':
    #                     for ii in range(len(res[1])): 
    #                         if res[1][ii][ u'long_name']== ff or res[1][ii][u'short_name'] == ff:
    #                             flag = 0;
    #                             # print ff , "LGLGLLG"

    #                             for j in range(len(res[1][ii][u'types'])):
    #                                 if res[1][ii][u'types'][j] == u'sublocality_level_1':
    #                                     flag = 1;
    #                                 elif res[1][ii][u'types'][j] == u'sublocality':
    #                                     flag = 1;
    #                                 elif res[1][ii][u'types'][j] == u'political':
    #                                     flag = 1;

    #                             if (flag == 1):
    #                                 # print "Location:" ,ff 
    #                                 dic_location[ff] = 1;
    #                                 fout = open('location_dictionary.py', 'w')
    #                                 fout.write('dic_location = '+str(dic_location))
    #                                 a.append(ff)

    #                 elif res[0]['status']=='OVER_QUERY_LIMIT':
    #                     key_id+=1
    #                     key=str(key_detail_list[key_id])
    #                     # print key
    #                     res=location(ff.encode('utf-8'),key)


    for i,each in enumerate(list_dictionary):
        for j in range(len(list_dictionary[i])):
            ff = list_dictionary[i][j]['NounPhrase']

        
            if ( len(ff) > 1):
                if ff not in done :
                    try :
                        ff = City_name_changes[ff]
                    except:
                        ff = ff
                    
                    try :

                        if ( dic_location[ff]  == 1):
                            a.append(ff)
                    
                    except :
                    ###Output Files Address
                        APi_Result=open('OutputV07.txt','w')
                        ###########Key files
                        key_detail_list=open('/media/inno/01D0425114146710/Saurabh/Coreference/Ner/Api_Keys.txt','r').read().split('\n')
                        key_id=0
                        key=str(key_detail_list[key_id])
                        

                        result=[]
                        keyList=[]
                        res =location(ff.encode('utf-8'),key)
                        
                        if res[0]['status'] == 'OK':
                            for ii in range(len(res[1])): 
                                if res[1][ii][ u'long_name']== ff or res[1][ii][u'short_name'] == ff:
                                    flag = 0;
                                    for j in range(len(res[1][ii][u'types'])):
                                        if res[1][ii][u'types'][j] == u'sublocality_level_1':
                                            flag = 1;
                                        elif res[1][ii][u'types'][j] == u'sublocality':
                                            flag = 1;
                                        elif res[1][ii][u'types'][j] == u'political':
                                            flag = 1;

                                    if (flag == 1):
                                        # print "Location:" ,ff 
                                        dic_location[ff] = 1;
                                        fout = open('location_dictionary.py', 'w')
                                        fout.write('dic_location = '+str(dic_location))
                                        a.append(ff)

                        elif res[0]['status']=='OVER_QUERY_LIMIT':
                            key_id+=1
                            key=str(key_detail_list[key_id])
                            # print key
                            res=location(ff.encode('utf-8'),key)

    

    return a



def  NER_company(input_sen,done,list_dictionary):

    suffix_dic = {}

    company = []
    bad_char = open('/media/inno/01D0425114146710/Saurabh/Coreference/Ner/bad chars.txt' ,'r').read().strip().split('\n')
    bad_char = [x.replace('\r','') for x in bad_char]
    suffix = open('/media/inno/01D0425114146710/Saurabh/Coreference/Ner/suffix.txt' ,'r').read().split('\n')

    for each in suffix :
        each1 = each.lower()
        each2 = each1.strip()
        # print (each2)
        suffix_dic[each2] = 1;
  

    for i,each in enumerate(list_dictionary[0]):
        token =  (list_dictionary[0][i]['NounPhrase'])

        if token not in done :
            token1 = token.lower()
            
            for each in bad_char:
                token1 = token1.replace(each," ")

            split_token = token1.split(" ")
            temp = []
            length = len(split_token)
            for each in reversed(split_token):
                temp.append(each)
                temp2 = reversed(temp)
                ss = ""
                for each in temp2:
                    ss = ss+" "+each
                ss = ss.strip()
                if ss in suffix_dic:
                    if ( suffix_dic[ss] == 1 and length != 1):
                        company.append(token) 
                        break

            # token = s
            # if token not in done :
            #     token1 = token.lower()
                

            #     split_token = token1.split(" ")
            #     temp = []
            #     length = len(split_token)
            #     for each in reversed(split_token):
            #         temp.append(each)
            #         temp2 = reversed(temp)
            #         ss = ""
            #         for each in temp2:
            #             ss = ss+" "+each
            #         ss = ss.strip()
            #         if ss in suffix_dic:
            #             if ( suffix_dic[ss] == 1 and length != 1):
            #                 company.append(token) 
            #                 break 


    output1 = list(set(company))

    return  output1

def NER_currency(input_sen,done):
    ########Finding Currency##########
    curr_list = []
    a = extract_curr(input_sen)
    if (len(a)>0) and a not in done:
        curr_list.append(a)

    # print "Currency :" ,curr_list
    temp = []
    for i in range(len(curr_list)):
        for j,each in enumerate(curr_list[i]):
            temp.append(each)

    return temp


def NER_date(input_sen,done):
    ########Finding Date###########
    date_list = []
    
    a = extract (input_sen)

    if (len(a) >0) and a not in done:
        date_list.append(a)

    

    temp = []
    for i in range(len(date_list)):
        for j,each in enumerate(date_list[i]):
            temp.append(each)
        
    return temp

def NER_location (input_sen,done,list_dictionary):
    return list(set(find_location (list_dictionary,done)))


def NER_lastname(input_sen, done,list_dictionary):

    last_name = open('/media/inno/01D0425114146710/Saurabh/Coreference/Ner/NameListV02.txt' ,'r').read().split('\n')
    output = []
    last_name_dic = {}
    for each in last_name:
        each1 = each.lower().strip()
        last_name_dic[each1]= 1; 

    for i,each in enumerate(list_dictionary[0]):
        token =  (list_dictionary[0][i]['NounPhrase'])
        if token not in done and list_dictionary[0][i]['POS']!= "NN":
            token1 = token.lower()
            # print token1

            split_token = token1.split(" ")
            temp = []
            length = len(split_token)
            if length > 1 :
                if split_token[length-1] in last_name_dic:
                    if last_name_dic[split_token[length-1]]== 1:
                        output.append(token)
    
    output1 = list(set(output))
    
    return  output1 

def merge ( done , output):
    for each in output:
        done.append(each)

    return done

def first_cap(alist):
    if alist[0].isupper() :
        return True
    else:
        return False  

def fun_prep(tree, origtree ,a,list_dictionary):
    for subTree_dic in tree :
        inside_trees = subTree_dic['subTree']
        orig_node = subTree_dic['node']
        if get_pos_rel(orig_node)['pos'] == "NNP" :
            if get_pos_rel(orig_node)['rel'] == 'nsubj' or get_pos_rel(orig_node)['rel'] == 'conj' or get_pos_rel(orig_node)['rel'] == 'dobj' or get_pos_rel(orig_node)['rel'] == 'pobj':
                s = ""
                if  len(subTree_dic['subTree']) > 0 :
                # s = ""
                    s+= cleannode(subTree_dic['subTree'][0][u'node']).lstrip().rsplit('-')[0]
                    s+= " "
                s+= get_pos_rel(orig_node)['word'].encode('utf-8')
                name_list.append(s)
            # # print cleannode(subTree_dic['subTree'][0][u'node']).lstrip().rsplit('-')[0] , get_pos_rel(orig_node)['word']
            # # print get_pos_rel(orig_node)['word'] ,  ( cleannode( subTree_dic['subTree'])).lstrip().rsplit('-')[0]

        node = get_pos_rel(orig_node)['word']
        # print node 
        

        if get_pos_rel(orig_node)['rel'] == 'pobj':
            inside_trees = subTree_dic['subTree']
            if get_pos_rel(get_node_parent(orig_node, inside_trees, origtree))['rel'] == 'prep':
                if get_pos_rel(get_node_parent(orig_node , inside_trees, origtree))['word'] == 'to' :
                    # print get_pos_rel(orig_node) , list_dictionary
                    # print get_pos_rel(orig_node)['word'] , list_dictionary[0][1]['NounPhrase']
                    for k,each in enumerate(list_dictionary[0]):
                        if get_pos_rel(orig_node)['word'] in list_dictionary[0][k]['NounPhrase']:
                            if first_cap (list_dictionary[0][k]['NounPhrase']):
                                location_list.append(list_dictionary[0][k]['NounPhrase'])


        if node.lower().strip() ==  'said' or node.lower().strip() ==  'says': 
            for subTree_dic2 in inside_trees:
                orig_node2 = subTree_dic2['node']
                node2 = get_pos_rel(orig_node2)['word']
                # print node2
                if get_pos_rel(orig_node2)['pos'] == 'NNP':
                    if node2 in list_dictionary[0][0]['NounPhrase']:
                        name_list.append(list_dictionary[0][0]['NounPhrase'])
              
            
        
        fun_prep (inside_trees, origtree,a,list_dictionary)

def pdf (remaining):
    prob_remaining = {}
    unique_company_dic = {}
    unique_company = open('/media/inno/01D0425114146710/Saurabh/Coreference/Ner/companyunique.txt' ,'r').read().split('\n')
    for each in unique_company:
        each1 = each.lower().strip()
        unique_company_dic[each1]= 1; 


    for i,each in enumerate(remaining):
        split_remaining = remaining[i].split()
        l = len(split_remaining)
        if l > 1:
            s = 0
            for j , every in enumerate(split_remaining):
                every1 = every.lower().strip()
              
                if every1 in unique_company_dic:
                    if unique_company_dic[every1] >= 1:
                        # print every1, "??"
                        s += 1;

            # print s , l 
            (aa) = float(s)/float(l)
            prob_remaining[remaining[i]] = aa


    return prob_remaining




def fullNER ( text_list , done , list_dictionary):
    result = {}

    output_company = NER_company(text_list,done , list_dictionary)
    done = merge (done , output_company)
    result["Company"] = output_company

    output_date = NER_date(text_list,done )
    done = merge (done , output_date)
    result["Date"] = output_date

    output_curr = NER_currency(text_list,done)
    done = merge (done , output_curr)
    result ["Currency"] = output_curr


    output_location =  NER_location(text_list,done,list_dictionary)
    # print output_location
    # output_location1 =  first_cap(output_location)
    done = merge (done , output_location)

    result["Location"] = output_location

    output_lastname  = NER_lastname(text_list,done,list_dictionary)
    done = merge (done , output_lastname)
    result["Name"] = output_lastname

   
    

    return result



################Main Function####################

def final_NER ( text):
    text_list=[]
    text_list.append(text)
    final_dic = {}
    dic = build_dictionary(text_list) 
    dic1 = insert_dictionary(final_dic, dic, text_list)
    list_dictionary = print_dictionary(dic1)

    tree = make_tree(text)


    r1 = fullNER ( text , done ,list_dictionary)

    # print r1 

    for i,each in enumerate(list_dictionary[0]):
        token =  (list_dictionary[0][i]['NounPhrase'])
        if token not in done:
            remaining.append(token)

    # print remaining , "OOOOOOOOOOOOOOO"
    # remaining.append(s)
    # print '>>', pdf(remaining)

    fun_prep(tree[0], tree[0] ,a,list_dictionary)

    r3 =  (r1["Location"])
    for each in location_list:
        if each  in remaining:
            r3.append(each)
            remaining.remove(each)
    r1["Location"] = r3


    r2 =  (r1["Name"])
    for each in name_list:
        if each in remaining:
            # print each 
            r2.append(each)

    r1["Name"] = r2

    # print r1["Lastname"] , "??"

    

    return  r1 
    

# if __name__=="__main__":
    # a = []
    # done = []
    # location_list = []
    # name_list = []
    # output_location = []
    # output_lastname = []
    # remaining = []
    # list_dictionary = []
    # input_file = open('ner_dataset.txt','r').read().split('\n')
    
    # print "location :" , location_list
    # print "name :" , name_list

    # print output_lastname

    # print final_NER("Barack Obama, Narendra Modi and Salman Khan are the person who are standing in the queue.")
