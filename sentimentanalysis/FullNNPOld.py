import csv
import re
import os
import ast
def posTag(x):
    pos=[]
    wordlist=[]
    totallist=[]

    result=nnpprepfromlist(x)
    for ele in result:
        if ele.find('-NNP')>0:
            pos.append('NNP')
        elif ele.find('-NNS')>0:
            pos.append('NNS')
        elif ele.find('-NN')>0:
            pos.append('NN')
    for elem in result:
        elelist=elem.split(' ')
        wor=[]
        for i in elelist:
            wor.append(i.split('-')[0])
        wordlist.append(' '.join(wor))
    totallist.append(wordlist)
    totallist.append(pos)
    return totallist
def singlePos(x):
    x=x.split('-')
    y=x[-1]
    return y

def cleannode(x):
    x = x[x.find('->')+2:]
    x = x.split('(')[0]
    return x

def nnpfromlist(dicttree):
    outnnp = []
    if dicttree['node'].find('(cc)')==-1 and dicttree['node'].find('(pobj)')==-1 and dicttree['node'].find('(prep)')==-1:   
        if dicttree['node'].find('(conj)')>=0:
            for smalldict in dicttree['subTree']:
                outnnp.append(cleannode(smalldict['node']).strip()) 
            node = cleannode(dicttree['node']).strip()
            outnnp.append(node)
        else:
            node = cleannode(dicttree['node']).strip()
            outnnp.append(node)
            for smalldict in dicttree['subTree']:
                outnnp.append(cleannode(smalldict['node']).strip())
    return ' '.join(outnnp)

def nnpprepfromlist(x):
    if x:
        masternode = cleannode(x[0]['node']).strip()
        x = x[0]['subTree']
    else:
        masternode = ""
        x = x

    # masternode = cleannode(x[0]['node']).strip()
    # x = x[0]['subTree']
    
    lenlist = len(x)
    i = 0
    j = 0
    outlistnnp = []
    outnnp = []
    while i<lenlist:
        if x[i]['node'].find('prep')>=0:
            if x[i]['node'].find('-IN')>=0:
                recursiveout = nnpprepfromlist(x[i]['subTree'])
                for each in recursiveout:
                    outlistnnp.append(each.strip())
            else:
                new = []
                new.append(x[i])
                recursiveout = nnpprepfromlist(new)
                for each in recursiveout:
                    outlistnnp.append(each.strip())
        else:
            lensub = len(x[i]['subTree'])
            if lensub>0:
                outnnp.append(nnpfromlist(x[i]).strip())
            else:
                outnnp.append(cleannode(x[i]['node']).strip())
        if i<lenlist-1 and (x[i+1]['node'].find('(cc)')>=0 or x[i+1]['node'].find('(prep)')>=0 or x[i+1]['node'].find('(conj)')>=0):
            if j==0:
                outnnp.append(masternode)
            outlistnnp.append(' '.join(outnnp))
            outnnp = []
            if x[i+1]['node'].find('(cc)')>=0:
                i = i + 1
            j = j + 1
        i += 1
    if j==0:
        outnnp.append(masternode)
    if len(outnnp)>0:
        outlistnnp.append(' '.join(outnnp))
    return outlistnnp
    



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



#Navigation dictionaries to find child dictionary of our NNP in question
def recursive_dict(dictum, nnp):
    # print dictum
    dictret = []
    if type(dictum) == dict:
        if dictum['node'].find(nnp)>0:
            dictret.append(dictum['subTree'])
            if len(recursive_dict(dictum['subTree'],nnp))>0:
                dictret.append(recursive_dict(dictum['subTree'],nnp))       
        else:
            if len(recursive_dict(dictum['subTree'],nnp))>0:
                dictret.append(recursive_dict(dictum['subTree'],nnp))
    else:
        for dictrow in dictum:
            if dictrow['node'].find(nnp)>0:
                dictret.append(dictrow['subTree'])
                if len(recursive_dict(dictrow['subTree'],nnp))>0:
                    dictret.append(recursive_dict(dictrow['subTree'],nnp))
                              
            else:
                if len(recursive_dict(dictrow['subTree'],nnp))>0:
                    dictret.append(recursive_dict(dictrow['subTree'],nnp))

    return dictret

def PosTagger(x):
    postagg=[]
    for words in x:
        if words.find('NNP')>-1:
            postagg.append('NNP')
        elif words.find('NNS')>-1:
            postagg.append('NNS')
        elif words.find('NN')>-1:
            postagg.append('NN')
        elif words.find('PRP')>-1:
            postagg.append('PRP')
        elif words.find('JJ')>-1:
            postagg.append('JJ')
        elif words.find('CD')>-1:
            postagg.append('CD')
        elif words.find('$')>-1:
            postagg.append('$')
        elif not words:
            pass
        else:
            postagg.append('Not Known')
    return postagg


#Extracting Full NNP Names from the dictionary
def fullnnp(dictum,nnp):
    smalllist = recursive_dict(dictum,nnp)
    # print smalllist
    smalllist = breakmultilist(smalllist)
    nnpoutput=[]
    nnpoutlist = []
    sublist=[]
    sublistPos=[]
    postypeoutput=[]
    prep_part=[]
    prep_part_pos=[]
    extra_result=-2
    if len(smalllist)==0:
        if nnp.find('-NNP')>0:
            master_nnp = nnp[:nnp.find('-NNP')]
            nnpoutput.append(master_nnp.strip('->'))
            postypeoutput.append('NNP')
        elif nnp.find('-NN')>0:
            master_nnp = nnp[:nnp.find('-NN')]
            nnpoutput.append(master_nnp.strip('->'))
            postypeoutput.append('NN')
        elif nnp.find('-PRP')>0:
            master_nnp = nnp[:nnp.find('-PRP')]
            nnpoutput.append(master_nnp.strip('->'))
            postypeoutput.append('PRP')
        elif nnp.find('-$')>-1:
            master_nnp = nnp[:nnp.find('-$')]
            nnpoutput.append(master_nnp.strip('->'))
            postypeoutput.append('$')
        elif nnp.find('-CD')>-1:
            master_nnp = nnp[:nnp.find('-CD')]
            nnpoutput.append(master_nnp.strip('->'))
            postypeoutput.append('CD')
        nnpoutlist.append(nnpoutput)
        nnpoutlist.append(postypeoutput)
    else:
        nnpout = []
        postype=[]
        postypeoutput=[]
        for lists in smalllist:
            if type(lists)==list:

                #Traversing each dictionary in list
                for pos in lists:
                    if type(pos)==dict:
                        if pos['node'].find('(nn)')>0:
                            if pos['node'].find('-NNP')>0:
                                temp = pos['node'][:pos['node'].find('-NNP')]
                                nnpout.append(temp.strip().strip('->').strip())
                                postype.append('NNP')
                            elif pos['node'].find('-NN')>0:
                                temp = pos['node'][:pos['node'].find('-NN')]
                                nnpout.append(temp.strip().strip('->').strip())
                                postype.append('NN')
                        if pos['node'].find('(amod)')>0:
                            if pos['node'].find('-JJ')>0:
                                temp = pos['node'][:pos['node'].find('-JJ')]
                                nnpout.append(temp.strip().strip('->').strip())
                                postype.append('JJ')
                        elif pos['node'].find('(det)')>0:
                            if pos['node'].find('-DT')>0:
                                temp = pos['node'][:pos['node'].find('-DT')]
                                nnpout.append(temp.strip().strip('->').strip())
                                postype.append('DT')

                        elif pos['node'].find('(poss)')>0:
                            if len(pos['subTree'])>0:
                                possess=pos['subTree']
                                if possess[0]['node'].find('DT')>0:
                                    words=possess[0]['node'][:possess[0]['node'].find('-DT')].strip().strip('->').strip()+" "+pos['node'][:pos['node'].find('-NN')].strip().strip('->').strip()
                                    nnpout.append(words.strip().strip('->').strip())
                                    postype.append(singlePos(pos['node'].strip().strip('->').strip()))
                                elif possess[0]['node'].find('NNP')>0:
                                    words=possess[0]['node'][:possess[0]['node'].find('-NNP')].strip().strip('->').strip()+" "+pos['node'][:pos['node'].find('-NN')].strip().strip('->').strip()
                                    nnpout.append(words.strip().strip('->').strip())
                                    postype.append(singlePos(pos['node'].strip().strip('->').strip()))
                                elif possess[0]['node'].find('NNS')>0:
                                    words=possess[0]['node'][:possess[0]['node'].find('-NNS')].strip().strip('->').strip()+" "+pos['node'][:pos['node'].find('-NN')].strip().strip('->').strip()
                                    nnpout.append(words.strip().strip('->').strip())
                                    postype.append(singlePos(pos['node'].strip().strip('->').strip()))

                                elif possess[0]['node'].find('NN')>0:
                                    words=possess[0]['node'][:possess[0]['node'].find('-NN')].strip().strip('->').strip()+" "+pos['node'][:pos['node'].find('-NN')].strip().strip('->').strip()
                                    nnpout.append(words.strip().strip('->').strip())
                                    postype.append(singlePos(pos['node'].strip().strip('->').strip()))
                                else:
                                    words=pos['node'][:pos['node'].find('-NN')].strip().strip('->').strip()
                                    npout.append(words.strip().strip('->').strip())
                                    postype.append(singlePos(pos['node'].strip().strip('->').strip()))

                            else:
                                if pos['node'].find('-NNP')>0:
                                    temp = pos['node'][:pos['node'].find('-NNP')]
                                    nnpout.append(temp.strip().strip('->').strip())
                                    postype.append('NNP')
                                elif pos['node'].find('-NNS')>0:
                                    temp = pos['node'][:pos['node'].find('-NNS')]
                                    nnpout.append(temp.strip().strip('->').strip())
                                    postype.append('NNS')
                                elif pos['node'].find('-NN')>0:
                                    temp = pos['node'][:pos['node'].find('-NN')]
                                    nnpout.append(temp.strip().strip('->').strip())
                                    postype.append('NN')
                                elif pos['node'].find('-PRP$')>0:
                                    temp = pos['node'][:pos['node'].find('-PRP$')]
                                    nnpout.append(temp.strip().strip('->').strip())
                                    postype.append('PRP$')
                                elif pos['node'].find('-CD')>0:
                                    temp = pos['node'][:pos['node'].find('-CD')]
                                    nnpout.append(temp.strip().strip('->').strip())
                                    postype.append('CD')
                        elif pos['node'].find('(pobj)')>0:
                            if pos['node'].find('-NNP')>0:
                                temp = pos['node'][:pos['node'].find('-NNP')]
                                nnpout.append(temp.strip().strip('->').strip())
                                postype.append('NNP')
                            elif pos['node'].find('-NNS')>0:
                                temp = pos['node'][:pos['node'].find('-NNS')]
                                nnpout.append(temp.strip().strip('->').strip())
                                postype.append('NNS')
                            elif pos['node'].find('-NN')>0:
                                temp = pos['node'][:pos['node'].find('-NN')]
                                nnpout.append(temp.strip().strip('->').strip())
                                postype.append('NN')

                        elif pos['node'].find('(appos)')>0:
                            if pos['node'].find('-NNP')>0:
                                temp = pos['node'][:pos['node'].find('-NNP')]
                                nnpout.append(temp.strip().strip('->').strip())
                                postype.append('NNP')
                            elif pos['node'].find('-NNS')>0:
                                temp = pos['node'][:pos['node'].find('-NNS')]
                                nnpout.append(temp.strip().strip('->').strip())
                                postype.append('NNS')
                            elif pos['node'].find('-NN')>0:
                                temp = pos['node'][:pos['node'].find('-NN')]
                                nnpout.append(temp.strip().strip('->').strip())
                                postype.append('NN')
                        
                        #########################PREP Section#################

                        elif pos['node'].find('(prep)')>0:
                            if len(pos['subTree'])>0:

                                if pos['node'].find('-IN')>0:
                                    temp = pos['node'][:pos['node'].find('-IN')]
                                    prep_part.append(temp.strip().strip('->').strip())
                                    prep_part_pos.append('IN')

                                result=posTag(pos['subTree'])
                                prep_part.append(result[0][0])
                                try:
                                    prep_part_pos.append(result[1][0])
                                except:
                                    prep_part_pos.append('CD')
                                
                            else:
                                if pos['node'].find('-NNP')>0:
                                    temp = pos['node'][:pos['node'].find('-NNP')]
                                    nnpout.append(temp.strip().strip('->').strip())
                                    postype.append('NNP')
                                elif pos['node'].find('-NNS')>0:
                                    temp = pos['node'][:pos['node'].find('-NNS')]
                                    nnpout.append(temp.strip().strip('->').strip())
                                    postype.append('NNP')
                                elif pos['node'].find('-NN')>0:
                                    temp = pos['node'][:pos['node'].find('-NN')]
                                    nnpout.append(temp.strip().strip('->').strip())
                                    postype.append('NNP')
                                elif pos['node'].find('-IN')>0:
                                    temp = pos['node'][:pos['node'].find('-IN')]
                                    nnpout.append(temp.strip().strip('->').strip())
                                    postype.append('IN')


                        elif pos['node'].find('(partmod)')>0:
                            if len(pos['subTree'])>0:
                                if pos['subTree'][0]['node'].find('-IN')>0:
                                    result=posTag(pos['subTree'][0]['subTree'])
                                    sublist.append(result[0])
                                    sublistPos.append(result[1])
                            else:
                                if pos['node'].find('-NNP')>0:
                                    temp = pos['node'][:pos['node'].find('-NNP')]
                                    nnpout.append(temp.strip().strip('->').strip())
                                    postype.append('NNP')
                                elif pos['node'].find('-NNS')>0:
                                    temp = pos['node'][:pos['node'].find('-NNS')]
                                    nnpout.append(temp.strip().strip('->').strip())
                                    postype.append('NNS')
                                elif pos['node'].find('-NN')>0:
                                    temp = pos['node'][:pos['node'].find('-NN')]
                                    nnpout.append(temp.strip().strip('->').strip())
                                    postype.append('NN')
                        elif pos['node'].find('(num)')>0:
                            if pos['node'].find('-CD')>0:
                                temp = pos['node'][:pos['node'].find('-CD')]
                                nnpout.append(temp.strip().strip('->').strip())
                                postype.append('CD')
                            elif pos['node'].find('(number)')>0:
                                if pos['node'].find('-CD')>0:
                                    temp = pos['node'][:pos['node'].find('-CD')]
                                    nnpout.append(temp.strip().strip('->').strip())
                                    postype.append('CD')

                        ########################New Section
                        elif pos['node'].find('(cc)')>0:
                            pass
                        elif pos['node'].find('(conj)')>0:
                            new_nnp=pos['node'][:pos['node'].find('(conj)')].strip().strip('->').strip()
                            extra_result=fullnnp(dictum, new_nnp)

                        else:
                            break
                    else:
                        for postt in pos:
                            if type(postt)==dict:
                                if postt['node'].find('(nn)')>0:
                                    if postt['node'].find('-NNP')>0:
                                        temp = postt['node'][:postt['node'].find('-NNP')]
                                        nnpout.append(temp.strip().strip('->').strip())
                                        postype.append('NNP')
                                    elif postt['node'].find('-NN')>0:
                                        temp = postt['node'][:postt['node'].find('-NN')]
                                        nnpout.append(temp.strip().strip('->').strip())
                                        postype.append('NN')
                                if postt['node'].find('(amod)')>0:
                                    if postt['node'].find('-JJ')>0:
                                        temp = postt['node'][:postt['node'].find('-JJ')]
                                        nnpout.append(temp.strip().strip('->').strip())
                                        postype.append('JJ')
                                elif postt['node'].find('(det)')>0:
                                    if postt['node'].find('-DT')>0:
                                        temp = postt['node'][:postt['node'].find('-DT')]
                                        nnpout.append(temp.strip().strip('->').strip())
                                        postype.append('DT')
                                elif postt['node'].find('(poss)')>0:
                                    if len(postt['subTree'])>0:
                                        possess=postt['subTree']
                                        if possess[0]['node'].find('DT')>0:
                                            words=possess[0]['node'][:possess[0]['node'].find('-DT')].strip().strip('->').strip()+" "+postt['node'][:postt['node'].find('-NN')].strip().strip('->').strip()
                                            nnpout.append(words.strip().strip('->').strip())
                                            postype.append(singlePos(postt['node'].strip().strip('->').strip()))

                                        elif possess[0]['node'].find('NNP')>0:
                                            words=possess[0]['node'][:possess[0]['node'].find('-NNP')].strip().strip('->').strip()+" "+postt['node'][:postt['node'].find('-NN')].strip().strip('->').strip()
                                            nnpout.append(words.strip().strip('->').strip())
                                            postype.append(singlePos(postt['node'].strip().strip('->').strip()))

                                        elif possess[0]['node'].find('NNS')>0:
                                            words=possess[0]['node'][:possess[0]['node'].find('-NNS')].strip().strip('->').strip()+" "+postt['node'][:postt['node'].find('-NN')].strip().strip('->').strip()
                                            nnpout.append(words.strip().strip('->').strip())
                                            postype.append(singlePos(postt['node'].strip().strip('->').strip()))
                                        elif possess[0]['node'].find('NN')>0:
                                            words=possess[0]['node'][:possess[0]['node'].find('-NN')].strip().strip('->').strip()+" "+postt['node'][:postt['node'].find('-NN')].strip().strip('->').strip()
                                            nnpout.append(words.strip().strip('->').strip())
                                            postype.append(singlePos(postt['node'].strip().strip('->').strip()))
                                        else:
                                            words=postt['node'][:postt['node'].find('-NN')].strip().strip('->').strip()
                                            npout.append(words.strip().strip('->').strip())
                                            postype.append(singlePos(postt['node'].strip().strip('->').strip()))

                                    else:
                                        if postt['node'].find('-NNP')>0:
                                            temp = postt['node'][:postt['node'].find('-NNP')]
                                            nnpout.append(temp.strip().strip('->').strip())
                                            postype.append('NNP')
                                        elif postt['node'].find('-NNS')>0:
                                            temp = postt['node'][:postt['node'].find('-NNS')]
                                            nnpout.append(temp.strip().strip('->').strip())
                                            postype.append('NNS')
                                        elif postt['node'].find('-NN')>0:
                                            temp = postt['node'][:postt['node'].find('-NN')]
                                            nnpout.append(temp.strip().strip('->').strip())
                                            postype.append('NN')
                                        elif postt['node'].find('-PRP$')>0:
                                            temp = postt['node'][:postt['node'].find('-PRP$')]
                                            nnpout.append(temp.strip().strip('->').strip())
                                            postype.append('PRP$')
                                        elif postt['node'].find('-CD')>0:
                                            temp = postt['node'][:postt['node'].find('-CD')]
                                            nnpout.append(temp.strip().strip('->').strip())
                                            postype.append('CD')
                                elif postt['node'].find('(pobj)')>0:
                                    if postt['node'].find('-NNP')>0:
                                        temp = postt['node'][:postt['node'].find('-NNP')]
                                        nnpout.append(temp.strip().strip('->').strip())
                                        postype.append('NNP')
                                    elif postt['node'].find('-NNS')>0:
                                        temp = postt['node'][:postt['node'].find('-NNS')]
                                        nnpout.append(temp.strip().strip('->').strip())
                                        postype.append('NNS')
                                    elif postt['node'].find('-NN')>0:
                                        temp = postt['node'][:postt['node'].find('-NN')]
                                        nnpout.append(temp.strip().strip('->').strip())
                                        postype.append('NN')
                                elif postt['node'].find('(appos)')>0:
                                    if postt['node'].find('-NNP')>0:
                                        temp = postt['node'][:postt['node'].find('-NNP')]
                                        nnpout.append(temp.strip().strip('->').strip())
                                        postype.append('NNP')
                                    elif postt['node'].find('-NNS')>0:
                                        temp = postt['node'][:postt['node'].find('-NNS')]
                                        nnpout.append(temp.strip().strip('->').strip())
                                        postype.append('NNS')
                                    elif postt['node'].find('-NN')>0:
                                        temp = postt['node'][:postt['node'].find('-NN')]
                                        nnpout.append(temp.strip().strip('->').strip())
                                        postype.append('NN')
                                    #########################PREP Section#################

                                elif postt['node'].find('(prep)')>0:
                                    if len(postt['subTree'])>0:

                                        if postt['node'].find('-IN')>0:
                                            temp = postt['node'][:postt['node'].find('-IN')]
                                            prep_part.append(temp.strip().strip('->').strip())
                                            prep_part_pos.append('IN')

                                        result=posTag(postt['subTree'])
                                        prep_part.append(result[0][0])
                                        try:
                                            prep_part_pos.append(result[1][0])
                                        except:
                                            prep_part_pos.append('CD')
                                        
                                    else:
                                        if postt['node'].find('-NNP')>0:
                                            temp = postt['node'][:postt['node'].find('-NNP')]
                                            nnpout.append(temp.strip().strip('->').strip())
                                            postype.append('NNP')
                                        elif postt['node'].find('-NNS')>0:
                                            temp = postt['node'][:postt['node'].find('-NNS')]
                                            nnpout.append(temp.strip().strip('->').strip())
                                            postype.append('NNP')
                                        elif postt['node'].find('-NN')>0:
                                            temp = postt['node'][:postt['node'].find('-NN')]
                                            nnpout.append(temp.strip().strip('->').strip())
                                            postype.append('NNP')
                                        elif postt['node'].find('-IN')>0:
                                            temp = postt['node'][:postt['node'].find('-IN')]
                                            nnpout.append(temp.strip().strip('->').strip())
                                            postype.append('IN')






                                elif postt['node'].find('(partmod)')>0:
                                    if len(postt['subTree'])>0:
                                        if postt['subTree'][0]['node'].find('-IN')>0:
                                            result=posTag(postt['subTree'][0]['subTree'])
                                            sublist.append(result[0])
                                            sublistPos.append(result[1])
                                    else:
                                        if postt['node'].find('-NNP')>0:
                                            temp = postt['node'][:postt['node'].find('-NNP')]
                                            nnpout.append(temp.strip().strip('->').strip())
                                            postype.append('NNP')
                                        elif postt['node'].find('-NNS')>0:
                                            temp = postt['node'][:postt['node'].find('-NNS')]
                                            nnpout.append(temp.strip().strip('->').strip())
                                            postype.append('NNS')
                                        elif postt['node'].find('-NN')>0:
                                            temp = postt['node'][:postt['node'].find('-NN')]
                                            nnpout.append(temp.strip().strip('->').strip())
                                            postype.append('NN')

                                elif postt['node'].find('(num)')>0:
                                    if postt['node'].find('-CD')>0:
                                        temp = postt['node'][:postt['node'].find('-CD')]
                                        nnpout.append(temp.strip().strip('->').strip())
                                        postype.append('CD')
                                    elif postt['node'].find('(number)')>0:
                                        if postt['node'].find('-CD')>0:
                                            temp = postt['node'][:postt['node'].find('-CD')]
                                            nnpout.append(temp.strip().strip('->').strip())
                                            postype.append('CD')
                                

                                ########################New Section
                                elif postt['node'].find('(cc)')>0:
                                    pass
                                elif postt['node'].find('(conj)')>0:
                                    new_nnp=postt['node'][:postt['node'].find('(conj)')].strip().strip('->').strip()
                                    extra_result=fullnnp(dictum, new_nnp)

                                else:
                                    break
                
                

            
            #List of Dictionaries
            else:
                # nnpoutput=[]
               
                if lists['node'].find('(nn)')>0:
                    if lists['node'].find('-NNP')>0:
                        temp = lists['node'][:lists['node'].find('-NNP')]
                        nnpout.append(temp.strip().strip('->').strip())
                        postype.append('NNP')
                    elif lists['node'].find('-NN')>0:
                        temp = lists['node'][:lists['node'].find('-NN')]
                        nnpout.append(temp.strip().strip('->').strip())
                        postype.append('NN')
                    elif lists['node'].find('-PRP')>0:
                        temp = lists['node'][:lists['node'].find('-PRP')]
                        nnpout.append(temp.strip().strip('->').strip())
                        postype.append('PRP')
                elif lists['node'].find('(amod)')>0:
                    if lists['node'].find('-JJ')>0:
                        temp = lists['node'][:lists['node'].find('-JJ')]
                        nnpout.append(temp.strip().strip('->').strip())
                        postype.append('JJ')
                elif lists['node'].find('(det)')>0:
                    if lists['node'].find('-DT')>0:
                        temp = lists['node'][:lists['node'].find('-DT')]
                        nnpout.append(temp.strip().strip('->').strip())
                        postype.append('DT')
                elif lists['node'].find('(poss)')>0:
                    if len(lists['subTree'])>0:
                        possess=lists['subTree']
                        if possess[0]['node'].find('DT')>0:
                            words=possess[0]['node'][:possess[0]['node'].find('-DT')].strip().strip('->').strip()+" "+lists['node'][:lists['node'].find('-NN')].strip().strip('->').strip()
                            nnpout.append(words.strip().strip('->').strip())
                            postype.append(singlePos(lists['node'].strip().strip('->').strip()))
                        elif possess[0]['node'].find('NNP')>0:
                            words=possess[0]['node'][:possess[0]['node'].find('-NNP')].strip().strip('->').strip()+" "+lists['node'][:lists['node'].find('-NN')].strip().strip('->').strip()
                            nnpout.append(words.strip().strip('->').strip())
                            postype.append(singlePos(lists['node'].strip().strip('->').strip()))
                        elif possess[0]['node'].find('NNS')>0:
                            words=possess[0]['node'][:possess[0]['node'].find('-NNS')].strip().strip('->').strip()+" "+lists['node'][:lists['node'].find('-NN')].strip().strip('->').strip()
                            nnpout.append(words.strip().strip('->').strip())
                            postype.append(singlePos(lists['node'].strip().strip('->').strip()))
                        elif possess[0]['node'].find('NN')>0:
                            words=possess[0]['node'][:possess[0]['node'].find('-NN')].strip().strip('->').strip()+" "+lists['node'][:lists['node'].find('-NN')].strip().strip('->').strip()
                            nnpout.append(words.strip().strip('->').strip())
                            postype.append(singlePos(lists['node'].strip().strip('->').strip()))

                        else:
                            words=lists['node'][:lists['node'].find('-NN')].strip().strip('->').strip()
                            nnpout.append(words.strip().strip('->').strip())
                            postype.append(singlePos(lists['node'].strip().strip('->').strip()))
                    else:
                        if lists['node'].find('-NNP')>0:
                            temp = lists['node'][:lists['node'].find('-NNP')]
                            nnpout.append(temp.strip().strip('->').strip())
                            postype.append('NNP')
                        elif lists['node'].find('-NNS')>0:
                            temp = lists['node'][:lists['node'].find('-NNS')]
                            nnpout.append(temp.strip().strip('->').strip())
                            postype.append('NNS')
                        elif lists['node'].find('-NN')>0:
                            temp = lists['node'][:lists['node'].find('-NN')]
                            nnpout.append(temp.strip().strip('->').strip())
                            postype.append('NN')
                        elif lists['node'].find('-PRP$')>0:
                            temp = lists['node'][:lists['node'].find('-PRP$')]
                            nnpout.append(temp.strip().strip('->').strip())
                            postype.append('PRP$')
                        elif lists['node'].find('-CD')>0:
                            temp = lists['node'][:lists['node'].find('-CD')]
                            nnpout.append(temp.strip().strip('->').strip())
                            postype.append('CD')
                elif lists['node'].find('(pobj)')>0:
                    if lists['node'].find('-NNP')>0:
                        temp = lists['node'][:lists['node'].find('-NNP')]
                        nnpout.append(temp.strip().strip('->').strip())
                        postype.append('NNP')
                    elif lists['node'].find('-NNS')>0:
                        temp = lists['node'][:lists['node'].find('-NNS')]
                        nnpout.append(temp.strip().strip('->').strip())
                        postype.append('NNS')
                    elif lists['node'].find('-NN')>0:
                        temp = lists['node'][:lists['node'].find('-NN')]
                        nnpout.append(temp.strip().strip('->').strip())
                        postype.append('NN')
                elif lists['node'].find('(appos)')>0:
                    if lists['node'].find('-NNP')>0:
                        temp = lists['node'][:lists['node'].find('-NNP')]
                        nnpout.append(temp.strip().strip('->').strip())
                        postype.append('NNP')
                    elif lists['node'].find('-NNS')>0:
                        temp = lists['node'][:lists['node'].find('-NNS')]
                        nnpout.append(temp.strip().strip('->').strip())
                        postype.append('NNS')
                    elif lists['node'].find('-NN')>0:
                        temp = lists['node'][:lists['node'].find('-NN')]
                        nnpout.append(temp.strip().strip('->').strip())
                        postype.append('NN')
                elif lists['node'].find('(prep)')>0:
                    if len(lists['subTree'])>0:

                        if lists['node'].find('-IN')>0:
                            temp = lists['node'][:lists['node'].find('-IN')]
                            prep_part.append(temp.strip().strip('->').strip())
                            prep_part_pos.append('IN')

                        result=posTag(lists['subTree'])
                        prep_part.append(result[0][0])
                        try:
                            prep_part_pos.append(result[1][0])
                        except:
                            prep_part_pos.append('CD')
                        
                    else:
                        if lists['node'].find('-NNP')>0:
                            temp = lists['node'][:lists['node'].find('-NNP')]
                            nnpout.append(temp.strip().strip('->').strip())
                            postype.append('NNP')
                        elif lists['node'].find('-NNS')>0:
                            temp = lists['node'][:lists['node'].find('-NNS')]
                            nnpout.append(temp.strip().strip('->').strip())
                            postype.append('NNP')
                        elif lists['node'].find('-NN')>0:
                            temp = lists['node'][:lists['node'].find('-NN')]
                            nnpout.append(temp.strip().strip('->').strip())
                            postype.append('NNP')
                        elif lists['node'].find('-IN')>0:
                            temp = lists['node'][:lists['node'].find('-IN')]
                            nnpout.append(temp.strip().strip('->').strip())
                            postype.append('IN')

                elif lists['node'].find('(partmod)')>0:
                    if len(lists['subTree'])>0:
                        if lists['subTree'][0]['node'].find('-IN')>0:
                            result=posTag(lists['subTree'][0]['subTree'])
                            sublist.append(result[0])
                            sublistPos.append(result[1])
                    else:
                        if lists['node'].find('-NNP')>0:
                            temp = lists['node'][:lists['node'].find('-NNP')]
                            nnpout.append(temp.strip().strip('->').strip())
                            postype.append('NNP')
                        elif lists['node'].find('-NNS')>0:
                            temp = lists['node'][:lists['node'].find('-NNS')]
                            nnpout.append(temp.strip().strip('->').strip())
                            postype.append('NNS')
                        elif lists['node'].find('-NN')>0:
                            temp = lists['node'][:lists['node'].find('-NN')]
                            nnpout.append(temp.strip().strip('->').strip())
                            postype.append('NN')
                elif lists['node'].find('(num)')>0:
                    if lists['node'].find('-CD')>0:
                        temp = lists['node'][:lists['node'].find('-CD')]
                        nnpout.append(temp.strip().strip('->').strip())
                        postype.append('CD')
                    elif lists['node'].find('(number)')>0:
                        if lists['node'].find('-CD')>0:
                            temp = lists['node'][:lists['node'].find('-CD')]
                            nnpout.append(temp.strip().strip('->').strip())
                            postype.append('CD')
                elif lists['node'].find('(cc)')>0:
                    pass
                elif lists['node'].find('(conj)')>0:
                    new_nnp=lists['node'][:lists['node'].find('(conj)')].strip().strip('->').strip()
                    extra_result=fullnnp(dictum, new_nnp)

                else:
                    break

         

        if nnp.find('-NNP')>0:
            master_nnp = nnp[:nnp.find('-NNP')]
            nnpout.append(master_nnp.strip('->'))
            postype.append('NNP')
        elif nnp.find('-NN')>0:
            master_nnp = nnp[:nnp.find('-NN')]
            nnpout.append(master_nnp.strip('->'))
            postype.append('NN')
        elif nnp.find('-PRP')>0:
            master_nnp = nnp[:nnp.find('-PRP')]
            nnpout.append(master_nnp.strip('->'))
            postype.append('PRP')
        elif nnp.find('-JJ')>0:
            master_nnp = nnp[:nnp.find('-JJ')]
            nnpout.append(master_nnp.strip('->'))
            postype.append('JJ')
        elif nnp.find('-CD')>0:
            master_nnp = nnp[:nnp.find('-CD')]
            nnpout.append(master_nnp.strip('->'))
            postype.append('CD')
        elif nnp.find('-$')>0:
            master_nnp = nnp[:nnp.find('-$')]
            nnpout.append(master_nnp.strip('->'))
            postype.append('$')

        if len(prep_part)>0:
            for ele in prep_part:
                nnpout.append(ele)
        nnpoutput.append(' '.join(nnpout))
        if len(prep_part_pos)>0:
            for elem in prep_part_pos:
                postype.append(elem)
        

        postypeoutput.append(' '.join(postype))
        if len(sublist)>0:
            for word in sublist[0]:
                nnpoutput.append(word)
        if len(sublistPos)>0:
            for wordpos in sublistPos[0]:
                postypeoutput.append(wordpos)
        if extra_result !=-2:
            if extra_result[0]:
                nnpoutput.append(extra_result[0][0])


        

        postaggerOutput=PosTagger(postypeoutput)
        if extra_result !=-2:
            if extra_result[1]:
                postaggerOutput.append(extra_result[1][0])
        nnpoutlist.append(nnpoutput)
        nnpoutlist.append(postaggerOutput)

    return nnpoutlist

# tre = [{u'node': u'-> presents-VBZ (root)', u'subTree': [{u'node': u'  -> Study-NNP (nsubj)', u'subTree': [{u'node': u'    -> The-DT (det)', u'subTree': []}]}, {u'node': u'  -> indicated-VBD (ccomp)', u'subTree': [{u'node': u'    -> Case-NN (nsubj)', u'subTree': [{u'node': u'      -> a-DT (det)', u'subTree': []}, {u'node': u'      -> Base-NN (nn)', u'subTree': []}, {u'node': u'      -> considers-VBZ (rcmod)', u'subTree': [{u'node': u'        -> which-WDT (nsubj)', u'subTree': []}, {u'node': u'        -> tonne-NN (dobj)', u'subTree': [{u'node': u'          -> a-DT (det)', u'subTree': []}, {u'node': u'          -> million-CD (num)', u'subTree': [{u'node': u'            -> 10-CD (number)', u'subTree': []}]}, {u'node': u'          -> per-IN (prep)', u'subTree': [{u'node': u'            -> operation-NN (pobj)', u'subTree': [{u'node': u'              -> annum-NN (nn)', u'subTree': []}, {u'node': u'              -> encompassing-VBG (partmod)', u'subTree': [{u'node': u'                -> existing-VBG (dobj)', u'subTree': [{u'node': u'                  -> measured-VBN (partmod)', u'subTree': [{u'node': u'                    -> and-CC (cc)', u'subTree': []}, {u'node': u'                    -> indicated-VBN (conj)', u'subTree': []}, {u'node': u'                    -> resources-NNS (dobj)', u'subTree': [{u'node': u'                      -> and-CC (cc)', u'subTree': []}, {u'node': u'                      -> Case-NN (conj)', u'subTree': [{u'node': u'                        -> an-DT (det)', u'subTree': []}, {u'node': u'                        -> Alternate-JJ (amod)', u'subTree': []}]}, {u'node': u'                      -> considers-VBZ (rcmod)', u'subTree': [{u'node': u'                        -> which-WDT (nsubj)', u'subTree': []}, {u'node': u'                        -> tonnes-NNS (dobj)', u'subTree': [{u'node': u'                          -> a-DT (det)', u'subTree': []}, {u'node': u'                          -> million-CD (num)', u'subTree': [{u'node': u'                            -> 10-CD (number)', u'subTree': []}]}, {u'node': u'                          -> per-IN (prep)', u'subTree': [{u'node': u'                            -> operation-NN (pobj)', u'subTree': [{u'node': u'                              -> annum-NN (nn)', u'subTree': []}]}]}]}]}]}, {u'node': u'                    -> incorporating-VBG (xcomp)', u'subTree': [{u'node': u'                      -> existing-VBG (dobj)', u'subTree': [{u'node': u'                        -> measured-VBN (partmod)', u'subTree': []}]}]}]}]}]}]}]}]}]}]}, {u'node': u'    -> and-CC (cc)', u'subTree': []}, {u'node': u'    -> inferred-VBD (conj)', u'subTree': [{u'node': u'      -> resources-NNS (dobj)', u'subTree': []}]}]}]}]
# sub = "which-WDT (nsubj)"

# print fullnnp(tre, sub)