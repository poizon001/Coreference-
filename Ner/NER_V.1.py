import json, requests, ast ,re
from sentimentanalysis import  cleaner, sentiment
import sentimentanalysis.FullNNP as fullname


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

# actor_list=breakmultilist(recursive_dict(tre[0],'NNP'))

####All NNP and NNS
def all_nnps(tree):
    all_nnp=[]
    keyword_pos=['NNP','NNS']
    for key in keyword_pos:
        actor_list=breakmultilist(recursive_dict(tree[0],key))
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
def build_dictionary ():
    fo = open('ner_dataset.txt' ,'r').read().split('\n')

    ans = {}
    for i,each in enumerate(fo) :
        bb = []
        print i 
        tree = make_tree(each)
        list1 = all_nnps(tree)

        for ac in list1 :
            for li in ac:
                if ( li != "") :
                    s = re.findall ('nn', li )
                    if ( len(s) == 0):
                        # print li , "?"
                        relation  = li.split('(', 1)[1].split(')')[0]
                        # print relation  
                        ll = (fullname.fullnnp(tree[0],li))

                        bb.append(combine ( ll , relation))

        ans[each] = bb

    print ans 

build_dictionary() 


