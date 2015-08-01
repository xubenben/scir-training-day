import sys,json
import math

rareword=[]
def get_rareword(filenme):
    fi=open(filenme,"r")
    worddict={}
    rareword=[]
    for line in fi:
        words=line.split()
        if words[1]=="UNARYRULE":
            worddict[words[3]]=worddict.get(words[3],0)+int(words[0])
    for word in worddict.iterkeys():
        if worddict[word]<5:
            rareword.append(word)
    fi.close()

def replace_rare_world_in_tree(tree):
    if len(tree)==3:
        tree[1]=replace_rare_world_in_tree(tree[1])
        tree[2]=replace_rare_world_in_tree(tree[2])
    elif tree[1] in rareword:
        tree[1]="_RARE_"
    return tree

def replace_rare_world_in_file(filename,filename1):
    get_rareword(filename1)
    fi=open(filename,"r")
    fo=open(filename+".new","w")
    for tree in fi:
        tree=json.loads(tree.strip())
        tree=replace_rare_world_in_tree(tree)
        json.dump(tree,fo) 
        fo.write("\n")
    fo.close()
    fi.close()

def gene_prob(filenam):
    fi=open(filenam,"r")
    count_X={}
    count_XYY={}
    count_XY={}
    prob_b={}
    prob_u={}
    for line in fi:
        words=line.strip().split()
        if words[1]=="NONTERMINAL":
            count_X[words[2]]=int(words[0])
        elif words[1]=="BINARYRULE":
            count_XYY[(words[2],words[3],words[4])]=int(words[0])
        else: 
            count_XY[(words[2],words[3])]=int(words[0])
    for w1,w2,w3 in count_XYY.iterkeys():
        prob_b[(w1,w2,w3)]=math.log(count_XYY[(w1,w2,w3)]/(1.0*count_X[w1]))
    for w1,w2 in count_XY.iterkeys():
        prob_u[(w1,w2)]=math.log(count_XY[(w1,w2)]/(1.0*count_X[w1]))

    fi.close()
    return prob_b,prob_u,count_X.keys()

def decode(i,j,s,words,b,nt):
    tree=[nt[s]]
    if j==1:
        tree.append(words[i-1])
    else:
       c1,c2,p=b[j][i][s] 
       p=int(p)
       tree.append(decode(i,p,c1,words,b,nt))
       tree.append(decode(i+p,j-p,c2,words,b,nt))
    return tree[:]
    

def parse_tree(line,prob_b,prob_u,nt):
    c=[' ']
    b=[' ']
    words=line.split()
    l=len(words)
    nt_l=len(nt)
    for j in range(1,1+l):
        list_j=[' ']
        b_j=[' ']
        for i in range(1,l+2-j):
            list_i_j=[' ']
            b_i_j=[' ']
            for x in range(1,1+nt_l):
                if j==1:
                    list_i_j.append(prob_u.get((nt[x-1],words[i-1]),-1000000))
                    b_i_j.append((x))
                else:
                    for p in range(1,j):
                        score=prob_b.get((nt[x-1],nt[0],nt[0]),-1000000)+c[p][i][1]+c[j-p][i+p][1]
                        list_i_j.append(score)
                        b_i_j.append((1,1,p))
                        for c1 in range(1,1+nt_l):
                            for c2 in range(1,1+nt_l):
                                score=prob_b.get((nt[x-1],nt[c1-1],nt[c2-1]),-1000000)+c[p][i][c1]+c[j-p][i+p][c2]
                                if list_i_j[x]<score:
                                    list_i_j[x]=score
                                    b_i_j[x]=(c1,c2,p)
                                
            list_j.append(list_i_j[:])
            b_j.append(b_i_j[:])
        c.append(list_j[:])
        b.append(b_j[:])

    return decode(1,l,"SBARQ",words,b,nt)


def parse(filename,nt,prob_b,prob_u):
    fi=open(filename,"r")
    fo=open("parse_dev.out","w")
    for line in fi:
        tree=parse_tree(line.strip(),prob_b,prob_u,nt)
        json.dump(tree,fo)
        fo.write("\n")
    fo.close()
    fi.close()
    

if __name__ == "__main__": 
    import pdb
    pdb.set_trace()
    if len(sys.argv) != 3:
        usage()
        sys.exit(1)
    # replace_rare_world_in_file(sys.argv[1],sys.argv[2])
    prob_b,prob_u,nt=gene_prob("parse_train.counts.out")
    parse("parse_dev.dat",nt,prob_b,prob_u)



