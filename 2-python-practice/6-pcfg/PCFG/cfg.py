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
    for line in fi:
        words=line.strip().split()
        if words[1]=="NONTERMINAL":
            count_X[words[2]]=int(words[0])
        elif words[1]=="BINARYRULE":
            count_XYY[(words[2],words[3],words[4])]=int(words[0])
        else: 
            count_XY[(words[2],words[3])]=int(words[0])
    nt=count_X.keys()
    nt_l=len(count_X.keys())
    prob_b=make_3_array(nt_l,nt_l,nt_l)
    prob_u={}
    # for w1,w2,w3 in count_XYY.iterkeys():
        # prob_b[(w1,w2,w3)]=math.log(count_XYY[(w1,w2,w3)]/(1.0*count_X[w1]))
    for i in range(1,nt_l+1):
        for j in range(1,nt_l+1):
            for k in range(1,nt_l+1):
                if (nt[i-1],nt[j-1],nt[k-1]) in count_XYY.keys():
                    prob_b[i][j][k]=math.log(count_XYY[(nt[i-1],nt[j-1],nt[k-1])]/(1.0*count_X[nt[i-1]]))
                else:
                    prob_b[i][j][k]=-1000000

    for w1,w2 in count_XY.iterkeys():
        prob_u[(w1,w2)]=math.log(count_XY[(w1,w2)]/(1.0*count_X[w1]))

    fi.close()
    return prob_b,prob_u,count_X.keys()

def decode(i,j,s,words,b,nt):
    tree=[nt[s-1]]
    if j==1:
        tree.append(words[i-1])
    else:
       c1,c2,p=b[j][i][s] 
       p=int(p)
       tree.append(decode(i,p,c1,words,b,nt))
       tree.append(decode(i+p,j-p,c2,words,b,nt))
    return tree[:]
    
def make_3_array(x,y,z):
    array={}
    for i in range(x+1):
        yarray={}
        for j in range(y+1):
            zarray={}
            for k in range(z+1):
                zarray[k]=float("-inf")
            yarray[j]=zarray
        array[i]=yarray
    return array



def parse_tree(line,prob_b,prob_u,nt):
    words=line.split()
    l=len(words)
    nt_l=len(nt)
    c=make_3_array(l,l,nt_l)
    b=make_3_array(l,l,nt_l)
    for j in range(1,1+l):
        for i in range(1,l+2-j):
            for x in range(1,1+nt_l):
                if j==1:
                    c[j][i][x]=prob_u.get((nt[x-1],words[i-1]),-1000000)
                    b[j][i][x]=x 
                else:
                    for p in range(1,j):
                        score=prob_b[x][1][1]+c[p][i][1]+c[j-p][i+p][1]
                        for c1 in range(1,1+nt_l):
                            for c2 in range(1,1+nt_l):
                                score=prob_b[x][c1][c2]+c[p][i][c1]+c[j-p][i+p][c2]
                                if c[j][i][x]<score:
                                    c[j][i][x]=score
                                    b[j][i][x]=(c1,c2,p)
    return decode(1,l,nt.index("SBARQ")+1,words,b,nt)


def parse(filename,nt,prob_b,prob_u):
    fi=open(filename,"r")
    fo=open("parse_dev.out","w")
    count=0
    for line in fi:
        tree=parse_tree(line.strip(),prob_b,prob_u,nt)
        json.dump(tree,fo)
        fo.write("\n")
        count+=1
        if count%10==0:
            print str(count)+"\n"
    fo.close()
    fi.close()
    

if __name__ == "__main__": 
    # import pdb
    # pdb.set_trace()
    if len(sys.argv) != 3:
        usage()
        sys.exit(1)
    # replace_rare_world_in_file(sys.argv[1],sys.argv[2])
    prob_b,prob_u,nt=gene_prob("parse_train.counts.out")
    parse("parse_dev.dat",nt,prob_b,prob_u)



