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
    for j in range(2,5):
        f1="SUFF:"+word[(-1*j):-1]+":"+s
        score+=v.get(f1,0)
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

def getbesttags(words,v):
    pi=multi_dimensions(4,float)
    bk=multi_dimensions(4,str)
    tags={}
    pi[0]["*"]["*"]=0
    for index in range(1,len(words)+1):
        for u in gettagset(index-1):
            for s in gettagset(index):
                pi[index][u][s]=-10000000
                for t in gettagset(index-2):
                    score=pi[index-1][t][u]+getscore(t,u,words[index],s,v)
                    if(score>pi[index][u][s]):
                        pi[index][u][s]=score
                        bk[index][u][s]=t
    max_score = -100000000 
    index=len(words)
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

    return tags


def train(filename_train):
    v={} 
    fi=open(filename_train,"r")
    words={}
    tags={}
    index=0
    for line in fi:
        line=line.strip()
        if line!="":
            index+=1
            ss=line.split()
            words[index]=ss[0]
            tags[index]=ss[1]
        else:
            p_tags=getbesttags(words,v) 
            for i in range(1,index-1):
               f1="TRIGRAM:"+p_tags[i]+":"+p_tags[i+1]+":"+p_tags[i+2]
               v[f1]=v.get(f1,0)-1
               f1="TRIGRAM:"+tags[i]+":"+tags[i+1]+":"+tags[i+2]
               v[f1]=v.get(f1,0)+1
            for i in range(1,index+1):
               f1="TAG:"+words[i]+":"+p_tags[i]
               v[f1]=v.get(f1,0)-1
               f1="TAG:"+words[i]+":"+tags[i]
               v[f1]=v.get(f1,0)+1
               for j in range(2,5):
                   f1="SUFF:"+words[i][-1*j:-1]+":"+p_tags[i]
                   v[f1]=v.get(f1,0)-1
                   f1="SUFF:"+words[i][-1*j:-1]+":"+tags[i]
                   v[f1]=v.get(f1,0)+1
            
            index=0
    fi.close()
    fo=open("tag.model.out","w")
    for line in v.iterkeys():
        fo.write(line+" "+str(v[line])+"\n")
    fo.close()
    return v



           



v=train("gene.train")
# v=initial("tag.model.out")
decode("gene.dev","gene.out.1",v)
    
