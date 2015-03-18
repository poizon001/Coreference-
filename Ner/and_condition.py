import json, requests, ast ,re
from sentimentanalysis import  cleaner, sentiment
import sentimentanalysis.FullNNP as fullname

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

def get_pos_rel(node):
    res = {}
    word = sentiment.filter_node(node)
    rel = sentiment.get_reln(node)
    pos = sentiment.get_pos(node)
    res['word'] = word
    res['rel'] = rel
    res['pos'] = pos
    return res

def get_node_parent(orig_node, inside_trees, origtree):
    di = {}
    di['node'] = orig_node
    di['subTree'] = inside_trees
    di1 = []
    di1.append(di)  
    orig_parent = sentiment.get_its_parent(origtree, di1)
    
    return orig_parent[0]

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

def fun_and (tree, origtree ,a):
    for subTree_dic in tree :
        orig_node = subTree_dic['node']
        node = filter_node(orig_node)
        if node == '&':
            inside_trees = subTree_dic['subTree']
            if get_pos_rel(get_node_parent(orig_node, inside_trees, origtree))['pos'] == 'NNP':
                a.append(get_pos_rel(get_node_parent(orig_node, inside_trees, origtree))['word'])
                a.append(' and ')
            if (get_next_parallel_nodes(node, tree)[1][0]['pos']) =='NNP':
                a.append(get_next_parallel_nodes(node, tree)[1][0]['word'])


        else :
            inside_trees = subTree_dic['subTree']
            fun_and (inside_trees, origtree,a)

'''
if __name__ == '__main__':

each = "Bane & Company is a good firm."
tree = make_tree(each)
a = []

fun_and(tree[0], tree[0] ,a)

s  = ""
for each in a:
    s+= each

print s   
'''      