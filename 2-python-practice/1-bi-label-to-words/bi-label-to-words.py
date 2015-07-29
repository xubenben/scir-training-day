#!/usr/bin/env python
import sys

def read_instance(fp):
    sentence = []
    while True:
        line = fp.readline()
        if not line:
            yield sentence
            break

        line = line.strip()

        if len(line) == 0:
            yield sentence
            sentence = []
        else:
            sentence.append( line.split() )


def bi2words(chars):
    # insert your code here
    sentence=[]
    is_first=True
    for char in chars:
        if char[1] == 'B':
            if is_first==False:
                sentence.append(" ")
                sentence.append(char[0])
            else:
                sentence.append(char[0])
                is_first=False
        else:
            sentence.append(char[0])
    return sentence


if __name__=="__main__":
    try:
        fpi = open(sys.argv[1], "r")
    except IOError:
        print >> sys.stderr, "failed to open file."
        sys.exit(1)

    try:
        fpo = open(sys.argv[2], "w")
    except IOError:
        print >> sys.stderr, "failed to open file."
        sys.exit(1)

    for sentence in read_instance(fpi):
        print sentence
        print bi2words(sentence)
        fpo.write(''.join(bi2words(sentence))+"\n")
    
    

    fpi.close()
    fpo.close()
