from sets import Set
def f_count(filename):
    fi=open(filename,'r')
    w={} #count the frequency of word in order to find rare words 
    d=Set([]) #word dictionary, determine whether a word is new ornot
    rarewords=[] #the rare words 
    states=[] #all the states in HMM 
    e={} #frequency of a state emite a word 
    t1={} #frequency of a state 
    t2={} #frequency of two states occur together 
    t3={} #frequency of three states occur togethor 
    for line in fi:
        word=line.strip().split() 
        if word[1]=='WORDTAG':
            d.add(word[3])
            w[word[3]]=w.get(word[3],0)+int(word[0])
            e[(word[2],word[3])]=e.get((word[2],word[3]),0)+int(word[0])
            if word[2] not in states:
                states.append(word[2])
        elif word[1]=="3-GRAM":
            t3[(word[2],word[3],word[4])]=t3.get((word[2],word[3],word[4]),0)+int(word[0])
        elif word[1]=="2-GRAM":
            t2[(word[2],word[3])]=t2.get((word[2],word[3]),0)+int(word[0])
        elif word[1]=="1-GRAM":
            t1[word[2]]=t1.get(word[2],0)+int(word[0])
    for word in w.iterkeys():
        if w[word]<5:
            rarewords.append(word)
    for word in rarewords:
        for state in states:
            if (state,word) in e:
                e[(state,"_RARE_")]=e.get((state,"_RARE"),0)+e[(state,word)]
                del e[(state,word)]
        d.discard(word) #diacard the rare words in word dictionary 
    d.add("_RARE_")

    fi.close()
    states.remove("*") 
    states.remove("STOP") 
    return d,states,e,t1,t2,t3

def calculate_prob(e,t1,t2,t3):
    ep={} #emission probability 
    tp={} #transfer probability 
    for word1,word2 in e.iterkeys():
        ep[(word1,word2)]=e.get((word1,word2))/(1.0*t1.get(word1))
    for word1,word2,word3 in t3.iterkeys():
        tp[(word1,word2,word3)]=t2.get((word1,word2,word3))/(1.0*t2.get((word1,word2)))

def viterbi(d,s,ep,tp,filename):
    sn=len(s) #number of states exclude "*' and "STOP" 
    states1=[] #latest score list 
    states2=[] #new score list 
    b1=[] #whole back table 
    b2=[] #current back list

    for i in range(sn):
        for j in range(sn):
            states1.append(tp(("*","*",s[i])))
            b2.append(-1) #initial b2 
    states2=states1 #initial states2 

    fi=open(filename,"r")
    wordnum=0
    for word in fi:
        #treat the new word as "_RARE_"
        if word not in d:
            word="_RARE_"

        wordnum+=1
        states1=states2 #update latest score list 
        for i in range(sn): #Yi 
            for j in range(sn): #Y(i-1) 
                states2[i*sn+j]=-1 #make sure the smallest 
                for t in range(sn): #Y(i-2) 
                    score=states1[j*sn+t]*tp((s[t],s[j],s[i]))*ep((s[j],word))
                    if states2[i*sn+j]<score:
                        states2[i*sn+j]=score
                        b2[i*sn+j]=j*sn+t
        b1.append(b2)
        lastword=word
    for j in range(sn):
        states2[j]=-1
        for t in range(sn):
            score=states1[j*sn+t]*tp((s[t],s[j],"STOP"))*ep((s[j],word))
            if states2[j]<score:
                states2[j]=score
                b2[j]=j*sn+t
    b1.append(b2)
    m=0
    for j in range(sn):
        if states2[j]>states2[m]:
            m=j
    
    fi.close()
    return m,b1,wordnum

def decode(m,b,wordnum,sn):
    sequence=[]
    backnum=m
    for i in range(wordnum):
        sequence.append(m)
        backnum=b[wordnum-i-1][backnum]
        m=backnum/sn
    mid=wordnum/2
    l=wordnum-1
    for i in range(mid):
        sequence[i],sequence[l-i] = sequence[l-i],sequence[i]
    return sequence



import pdb
pdb.set_trace()
d,s,e,t1,t2,t3=f_count("gene.counts")
calculate_prob(e,t1,t2,t3)
