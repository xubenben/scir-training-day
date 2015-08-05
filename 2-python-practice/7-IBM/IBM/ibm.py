from itertools import izip
from collections import defaultdict
from collections import Counter

def multi_dimensions(n, type):
    if n<=1:
        return type()
    return defaultdict(lambda:multi_dimensions(n-1, type))

def initial(filename_e,filename_f):
    fi_e = open(filename_e,"r")
    fi_f = open(filename_f,"r")
    trans=multi_dimensions(3,float)
    for line_e,line_f in izip(fi_e,fi_f):
        words_e=line_e.strip().split()
        words_f=line_f.strip().split()
        for w1 in words_e:
            for w2 in words_f:
               trans[w1][w2]=0 
    for w1 in trans.iterkeys():
        l=len(trans[w1])
        for w2 in trans[w1].iterkeys():
            trans[w1][w2]=float(1)/l
    fi_e.close()
    fi_f.close()
    return trans
        

def train(filename_e,filename_f,trans):
    # fi_  e = open(filename_e,"r")
    # fi_f = open(filename_f,"r")
    for ind in range(5):
        cef=multi_dimensions(3,float)
        ce={}
        with open(filename_e,"r") as fi_e,open(filename_f,"r") as fi_f: 
            for line_e,line_f in izip(fi_e,fi_f):
                words_e=line_e.strip().split()
                words_f=line_f.strip().split()
                f={}
                g=multi_dimensions(3,float)
                for w2 in words_f:
                    for w1 in words_e:
                        f[w2]=f.get(w2,0)+trans[w1][w2]
                for w2 in words_f:
                    for w1 in words_e:
                        g[w1][w2]=float(trans[w1][w2])/f[w2]

                for w2 in words_f:
                    for w1 in words_e:
                        cef[w1][w2]+=g[w1][w2]
                        ce[w1]=ce.get(w1,0)+g[w1][w2]
        # import pdb
        # pdb.set_trace()
        for w1 in trans.iterkeys():
            for w2 in trans[w1].iterkeys():
                trans[w1][w2]=float(cef[w1][w2])/ce[w1]
    fi_e.close()
    fi_f.close()
    return trans

def decode(file_dev_e,file_dev_f,file_out,trans):
    fi_e=open(file_dev_e,"r")
    fi_f=open(file_dev_f,"r")
    fo=open(file_out,"w")
    index0=0
    for line_e,line_f in izip(fi_e,fi_f):
        index0+=1
        words_e=line_e.strip().split()
        words_f=line_f.strip().split()
        index2=0
        for w2 in words_f:
            index2+=1
            a=-1
            b=-1
            index1=0
            for w1 in words_e:
                index1+=1
                if a < trans[w1][w2]:
                    a=trans[w1][w2]
                    b=index1
            fo.write(str(index0)+" "+str(b)+" "+str(index2)+"\n")
    fo.close()
    fi_f.close()
    fi_e.close()


trans=initial("corpus.en","corpus.es")
trans=train("corpus.en","corpus.es",trans)
# import pdb
# pdb.set_trace()
decode("dev.en","dev.es","dev.out",trans)
