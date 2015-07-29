class NGram(object):

    uniGram={}
    biGram={}

    def __init__(self, n):
        # n is the order of n-gram language model
        self.n = n

    # scan a sentence, extract the ngram and update their
    # frequence.
    #
    # @param    sentence    list{str}
    # @return   none
    def scan(self, sentence):
        # file your code here

        first="START"
        second=""
        for word in sentence.split():
            second=word.lower()
            self.uniGram[second]=self.uniGram.get(second,0)+1
            self.biGram[(first,second)]=self.biGram.get((first,second),0)+1
            first=second
        second="END"
        self.biGram[(first,second)]=self.biGram.get((first,second),0)+1


    # caluclate the ngram of the words
    #
    # @param    words       list{str}
    # @return   int         count of the ngram
    def ngram(self, words):
        # file your code here
        first="START"
        score=1.0
        for word in words.split():
            second=word.lower()
            print second
            if second not in self.uniGram:
                return -1
            score=score*(self.biGram.get((first,second),0)/(1.0*self.uniGram.get(first,1)))
            first=second
        second="END"
        #score*=(self.biGram.get((first,second),0)/(1.0*self.uniGram.get(first)))
        return score

    def write2file(self):
        fo=open("data.uni","w")
        for word,count in self.uniGram.iteritems():
            fo.write(word+"\t"+str(count)+"\n")
        fo.close()
        fo=open("data.bi","w")
        for word1,word2 in self.biGram:
            fo.write(word1+" "+word2+"\t"+str(self.biGram[(word1,word2)])+"\n")
        fo.close()




if __name__=="__main__":
    import sys
    #print >> sys.stderr, "library is not runnable"
    gram = NGram(2)
    gram.scan("xu jun and jun xu is the xu and xu")
    gram.write2file()
    print gram.ngram("xu jun and")

