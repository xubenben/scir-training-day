#!/usr/bin/env python
#import pudb; pu.db
import cPickle as pickle
import sys


def find_word(words,dic):
    l=len(words)
    l_z=l
    for i in range(l_z): 
        if words[:(l_z-i)].encode('utf-8') in dic:
            return (l_z-i)
    return 1



def max_match_segment( line, dic ):
    # write your code here
    segment=[]
    l=len(line)
    index=0
    while index<=l-5:
        wordsize=find_word(line[index:index+5], dic)
        segment.append(line[index:index+wordsize])
        index+=wordsize
    while index<l:
        wordsize=find_word(line[index:], dic)
        segment.append(line[index:index+wordsize])
        index+=wordsize
        
    return segment


if __name__=="__main__":

    try:
        fpi=open(sys.argv[1], "r")
    except:
        print >> sys.stderr, "failed to open file"
        sys.exit(1)

    try:
        dic = pickle.load(open(sys.argv[2],'r'))
    except:
        print >> sys.stderr, "failed to load dict"
        sys.exit(1)
    #import pdb
    #pdb.set_trace()
    fo=open("output.dat","w")
    i=0
    for line in fpi:
        #print line[1]
        line=line.decode("utf-8")
        #print line[1]
        i+=1
        fo.write(u"\t".join( max_match_segment(line.strip(), dic)
            ).encode('utf-8')+"\n")
        print u"\t".join( max_match_segment(line.strip(), dic)
                ).encode('utf-8')+"\n"
    fo.close()
