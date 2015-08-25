from collections import defaultdict
import math

##working?

def parse_word(s):
    word_list = []
    s = s.lower()
    buffer = ""
    for c in s:
        if (c >= 'a' and c <= 'z'):
            buffer = buffer + c
        elif (len(buffer) > 1 ):
            word_list.append(buffer)
            buffer = ""
        else:
            buffer = ""
    if(len(buffer) > 1):
        word_list.append(buffer)
    buffer = ""
    return word_list

def Frequency_dict(list):
    frequencies = defaultdict(str)
    for word in list:
        if (word not in frequencies):
            frequencies[word] = 1
        else:
            frequencies[word] += 1
    return frequencies
    
def WTF(freq):
    if(freq == 0):
        return 0
    return 1+math.log10(freq)

def score(freq, kind):
    if(kind == "title"):
        return 0.6*freq
    elif(kind == "body"):
        return 0.3*freq
    else:
        return 0.1*freq
def idf(corpus,df):
    return math.log10(float(corpus)/float(df))
    

if __name__ == '__main__':
    result = []
    
    result = parse_word('testing parser!ohoh zz z!!z xc aaa')
    for i in result:
        print(i)


