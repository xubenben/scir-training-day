from collections import defaultdict
from collections import Counter
import math 

def multi_dimensions(n, type):
    if n<=1:
        return type()
    return defaultdict(lambda:multi_dimensions(n-1, type))

def initial(filename):
    fi=open(filename,"r")
    v={}
    for line in fi:
        words=line.strip().split()
        v[words[0]]=float(words[1])
    fi.close()
    return v

def getscore(t,u,word,s,v):
    score =0
    f1="TAG:"+word+":"+s
    f2="TRIGRAM:"+t+":"+u+":"+s
    if f1 in v:
        score+=v[f1]
    if f2 in v:
        score+=v[f2]

    return score 

def gettagset(i):
    if i<=0:
        return ["*"]
    else:
        return ["O","I-GENE"]

def decode(input_filename,output_filename,v):
    fi=open(input_filename,"r")
    fo=open(output_filename,"w")
    index=0
    pi=multi_dimensions(4,float)
    bk=multi_dimensions(4,str)
    tags={}
    words={}
    pi[0]["*"]["*"]=0
    for word in fi:
        word=word.strip()
        if word!="":
            index+=1
            words[index]=word
            for u in gettagset(index-1):
                for s in gettagset(index):
                    pi[index][u][s]=-10000000
                    for t in gettagset(index-2):
                        score=pi[index-1][t][u]+getscore(t,u,word,s,v)
                        if(score>pi[index][u][s]):
                            pi[index][u][s]=score
                            bk[index][u][s]=t
        else:
            max_score = -100000000 
            for u in gettagset(index-1):
                for s in gettagset(index):
                    if max_score<pi[index][u][s]:
                        max_score=pi[index][u][s]
                        max_u=u
                        max_s=s
            tags[index]=max_s
            tags[index-1]=max_u
            for i in range(index-2,0,-1):
                tags[i]=bk[i+2][tags[i+1]][tags[i+2]]
            for i in range(1,index+1):
                fo.write(words[i]+" "+tags[i]+"\n")
            fo.write("\n")
            index=0

    fi.close()
    fo.close()



v=initial("tag.model")
decode("gene.dev","gene.out",v)





    
