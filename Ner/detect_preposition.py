import json, requests, ast ,re
from sentimentanalysis import  cleaner, sentiment
import sentimentanalysis.FullNNP as fullname
from scriptV02 import *
    

def getData1(text, delimiter, bd, sentiment):
    url = 'http://localhost:8080/sae-1.0.0-BUILD-SNAPSHOT/analytics/analyse'
    json_data = {"sentence":text, "bd":bd, "sentiment":sentiment, "delimiter":delimiter}
    headers = {"Content-type": "application/json","Accept": "application/json"}
    jsonData = json.dumps(json_data)
    response = requests.post(url, headers=headers, data=jsonData)
    return response.json()
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
def make_tree(line):
    bd = getData1(line, bd=True, sentiment=False, delimiter="-")
    bd = "["+str(bd)+"]"
    bd = ast.literal_eval(bd)
    return bd
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

def filter_node(word):
    word = word.strip().replace("-> ","")
    word = str(word.rsplit("-",1)[0])
    return word

def get_pos_rel(node):
    res = {}
    word = sentiment.filter_node(node)
    rel = sentiment.get_reln(node)
    pos = sentiment.get_pos(node)
    res['word'] = word
    res['rel'] = rel
    res['pos'] = pos
    return res

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

    
def get_node_parent(orig_node, inside_trees, origtree):
    di = {}
    di['node'] = orig_node
    di['subTree'] = inside_trees
    di1 = []
    di1.append(di)  
    orig_parent = sentiment.get_its_parent(origtree, di1)
    
    return orig_parent[0]

def all_nnps(tree):
    all_nnp=[]
    keyword_pos=['NNP','NNS']
    for key in keyword_pos:
        actor_list=breakmultilist(recursive_dict(tree[0],key))
        # print actor_list
        clean_name=clean_actor(actor_list)
        all_nnp.append(clean_name)
    return all_nnp

def get_next_parallel_nodes(node, tree):
    flag = 0
    parallel_nodes = []
    words = []
    for i, subTree_dic in enumerate(tree):
        orig_node = subTree_dic['node']
        inside_trees = subTree_dic['subTree'] 
        new_node = sentiment.filter_node(orig_node)
        if flag == 1:
            parallel_nodes.append(get_pos_rel(orig_node))
            words.append(new_node)
        if new_node == node:
            flag = 1

    return words, parallel_nodes

def fun_prep(tree, origtree ,a):
    for subTree_dic in tree :
        inside_trees = subTree_dic['subTree']
        orig_node = subTree_dic['node']
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

                            location_list.append(list_dictionary[0][k]['NounPhrase'])


        # temp = get_pos_rel(orig_node)['word'] 
        # temp1 = temp.strip()
        # print orig_node

        if node.lower().strip() ==  'said' or node.lower().strip() ==  'says': 
            for subTree_dic2 in inside_trees:
                orig_node2 = subTree_dic2['node']
                node2 = get_pos_rel(orig_node2)['word']
                # print node2
                if get_pos_rel(orig_node2)['pos'] == 'NNP':
                    if node2 in list_dictionary[0][0]['NounPhrase']:
                        name_list.append(list_dictionary[0][0]['NounPhrase'])
                # if get_pos_rel (subTree_dic[u'subTree'][0][u'node'])['pos'] == 'NNP':
                #     print "hi"
                # orig_node = subTree_dic['node']
                # node = get_pos_rel(orig_node)['word']
                # print node,"???" 
                
     
          

            
        
        fun_prep (inside_trees, origtree,a)

        # node = filter_node(orig_node)
        # # print node 
        # # inside_trees = subTree_dic['subTree']
        # # print get_pos_rel(get_node_parent(orig_node, inside_trees, origtree))['rel']
        # # print get_pos_rel(get_node_parent(orig_node, inside_trees, origtree)['rel'])
        # # # if get_pos_rel(get_node_parent(orig_node, inside_trees, origtree))['rel'] == 'pobj' and get_pos_rel(get_node_parent(orig_node, inside_trees, origtree)['rel']) == 'prep':
        # # #     print "hii"
        # # # # if (get_next_parallel_nodes(node, tree)[1][0]['pos']) =='NNP':
        # # #     a.append(get_next_parallel_nodes(node, tree)[1][0]['word'])


        # # # else :
        #

if __name__ == '__main__':

    text = "Mahatma Gandhi says he is going to Dandi,Gujarat"
    text_list = []
    text_list.append(text)
    
    # sentiment.tree_parse(tree[0])

    a = []
    dic = []
    dic1 = []
    final_dic = {}
    location_list = []
    name_list = []
    tree = make_tree(text)
    dic = build_dictionary(text_list) 
    dic1 = insert_dictionary(final_dic, dic, text_list)
    list_dictionary = print_dictionary(dic1)

    # print list_dictionary, "????"
    fun_prep(tree[0], tree[0] ,a)

    print "location :" , location_list
    print "name :" , name_list


        