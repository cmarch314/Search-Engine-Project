
'''
@author:Ho Choi, choih4@uci.edu 
'''
import os
import json
import Utilities
import pickle

from collections import defaultdict
from _io import BufferedReader



## as a main , this class reads files 
## and parse the file into index


if(__name__ == '__main__'):
    ##to resume files
    corpus_log = 0
    ## word -> wordID
    word_hash = defaultdict(float)
    
    ## wordID -> {docID:freq ... }
    term_docID_freq = defaultdict(dict)
    
    ## wordID -> {docID:tf-idf ... }  
    term_tfidf = defaultdict(dict)
    
    
    path = "Core\\"
    save_path = "Indexes\\"
    
## 1) load saved term if it is possible
    try:
        print("loading stopwords.txt")
        stop_words_file = open("stopwords.txt")
        stop_words = Utilities.parse_word(stop_words_file.read())
    except:
        print("Can't find stopwords.txt")
    try:
        print("loading freq")
        loading = open(save_path + 'term_freq.pk','rb')
        term_docID_freq = pickle.load(loading)
    except:
        print("loading Freq failed")
    
    try:
        print("loading tf-idf")
        loading = open(save_path + 'term_tfidf.pk','rb')
        term_tfidf = pickle.load(loading)
    except:
        print("loading tfidf failed")
    
    try:
        print("loading word_hash")
        loading = open(save_path + 'word_hash.pk','rb')
        word_hash = pickle.load(loading)
    except:
        print("loading word_hash failed")
    try:
        print("loading file_log")
        loading = open(save_path + 'file_log.pk','rb')
        corpus_log = pickle.load(loading)
    except:
        print("loading corpus_log failed")
    
    
        
## 2) read directory and have iterator for parsing
    for filename in os.listdir(path)[corpus_log:]:
        corpus_log +=1
        
        if(filename.endswith(".txt")):
            file_in = open(path+"\\"+filename)
            temp = ""
            t_dict = defaultdict()
            exec ("temp = json.dumps("+file_in.read()+")")
            exec ("t_dict =" + temp)
            ##float doc_id 
            doc_id = t_dict.get('id')
            
            ##str url,str title, str text
            url = t_dict.get('_id')
            title = t_dict.get('title')
            text = t_dict.get('text')
            
            parsed_words = Utilities.parse_word(text)
            parsed_title = Utilities.parse_word(title)
            
            freq_title = Utilities.Frequency_dict(parsed_title)
            freq_words = Utilities.Frequency_dict(parsed_words)
            
            
            ## for texts, get hash codes and process indexing to Freq
            for word in freq_words.keys():
                ## check for word_ID
                if(word not in word_hash.keys()):
                    word_hash[word] = len(word_hash)
                term_id = word_hash[word]
                if( term_id in term_docID_freq.keys() ):
                    if doc_id in term_docID_freq[term_id].keys():
                        term_docID_freq[term_id][doc_id][1] += freq_words[word]
                term_docID_freq[term_id][doc_id] = [0,freq_words[word]]
            
                
            ## this is for title same as text
            for word in freq_title.keys():
                ## check for word_ID
                if(word not in word_hash.keys()):
                    word_hash[word] = len(word_hash)
                term_id = word_hash[word]
                if( term_id in term_docID_freq.keys() ):
                    if doc_id in term_docID_freq[term_id].keys():
                        term_docID_freq[term_id][doc_id][0] += freq_title[word]
                term_docID_freq[term_id][doc_id] = [freq_title[word],0]
    
    print("Removing Stop words")
    for stopword in stop_words:
        if(stopword in word_hash.keys()):
            term_docID_freq.pop(word_hash.get(stopword))
            word_hash.pop(stopword)
        if(stopword in word_hash.keys()):
            print("not removed")
            
    print("computing tf-idf")
    for t, doc_freq in term_docID_freq.items():
        for d, f in doc_freq.items():
            title_wtf = Utilities.WTF(int(f[0]))
            body_wtf = Utilities.WTF(int(f[1]))
            df = len(doc_freq) ##document frequency
            idf = Utilities.idf(corpus_log, df)
            tf_idf = Utilities.score(title_wtf, "title")*idf
            tf_idf += Utilities.score(body_wtf, "body")*idf
            term_tfidf[t][d] = tf_idf
    
    
## final) save terms into file
    print("saving all files")
    file_freq = open(save_path + "term_freq.pk",'wb')
    file_tfidf = open(save_path + "term_tfidf.pk",'wb')
    file_word_hash = open(save_path + "word_hash.pk",'wb')
    file_log = open(save_path +  "file_log.pk",'wb')
    
    pickle.dump(term_tfidf,file_tfidf)
    pickle.dump(word_hash,file_word_hash)
    pickle.dump(term_docID_freq,file_freq)
    pickle.dump(corpus_log,file_log)

    
    print("total word to term : " + str(len(word_hash)))
    print("total term to docID:freq : " + str(len(term_docID_freq)))
    print("total term to docID:tfidf : " + str(len(term_tfidf)))


