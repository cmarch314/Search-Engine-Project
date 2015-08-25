'''
Created on Jun 2, 2015

@author: Choi
'''
from tkinter import *
import os
import json
import Utilities
import pickle
from collections import defaultdict
from _io import BufferedReader
import webbrowser
from xml.dom import INVALID_ACCESS_ERR

class Searcher:
    SearchedResult =  [["",""],["",""],["",""],["",""],["",""]]
    docID_to_score = defaultdict(float)
    ## word -> wordID
    word_hash = defaultdict(float)
    ## wordID -> {docID:tf-idf ... }  
    term_tfidf = defaultdict(dict)
    
    ## FileDump path and index path(pre-computed by indexer) must be modified by user
    save_path = "C:\\Users\\Choi\\Documents\\CS121\\FileDump\\index_log\\"
    path = "C:\\Users\\Choi\\Documents\\CS121\\FileDump\\Core"    
    root = Tk()
    root.title("ICS Search Engine")
    searchBarFrame = Frame(root,height = 50, width = 100)
    searchBarFrame.pack(side = TOP)
    
    resultListFrame = Frame(root,height = 100, width = 100)
    resultListFrame.pack(side = BOTTOM)
    
    def __init__(self):
        '''
        as initialization, load pre-computed indexed file, word->termID, termID->{docID->tf_idf}
        having main frame as root
        consist with search frame on top , result frame on bottom
        search button runs __search__, which computes searching process and update result to result ListBox
        go button runs __navigate__, which takes selected item of ListBox and run OS default browser passing URL
        '''
        ##to resume files
        
        try:
            print("loading tf-idf")
            loading = open(self.save_path + 'term_tfidf.pk','rb')
            self.term_tfidf = pickle.load(loading)
        except:
            print("loading tfidf failed")
        
        try:
            print("loading word_hash")
            loading = open(self.save_path + 'word_hash.pk','rb')
            self.word_hash = pickle.load(loading)
        except:
            print("loading word_hash failed")

        MessageLabel = Label(self.resultListFrame,width = 60,height = 1,text="Welcome")
        MessageLabel.pack(side = TOP)
        
        searchBar = Entry(self.searchBarFrame,width = 50)
        searchBar.pack(side=LEFT)
        
        GoButton = Button(self.resultListFrame, text = "Go",width = 30,command = lambda: self.__navigate__(resultDisplay,MessageLabel))
        GoButton.pack(side=BOTTOM)
        
        resultDisplay = Listbox(self.resultListFrame,selectmode = SINGLE,width = 55,height = 5)
        resultDisplay.pack(side=BOTTOM)
        
        self.__refreash__(resultDisplay)
        
        searchButton = Button(self.searchBarFrame, text = "Search",command=lambda: self.__search__(searchBar,resultDisplay,MessageLabel))
        searchButton.pack(side=RIGHT)
        
        
        self.root.mainloop()
        
    def __search__(self,searchBar,resultDisplay,MessageLabel):
        '''
        taking string from searchBar, parse it using Utilities.parse(string)
        look for word_hash to find word->termID
        if exist, compute each term->docID,tf_idf to docID->tf_idf += additional tf_idf if exist.
        sort the result by tf_idf value
        load title, url from FileDump
        update result to SearchedResult=[title,url] by order
        '''
        searchFor = searchBar.get()
        query = Utilities.parse_word(searchFor)
        
        self.docID_to_score = defaultdict(float)
        
        for word in query:
            if word in self.word_hash:
                index = self.word_hash[word]
                for doc_id, doc_score in self.term_tfidf[index].items():
                    if doc_id in self.docID_to_score:
                        self.docID_to_score[doc_id]+=doc_score
                    else:
                        self.docID_to_score[doc_id] = doc_score
            else:
                query.remove(word)
        ##sort to get top five result                
        sorted_result = sorted(self.docID_to_score,key = self.docID_to_score.__getitem__ ,reverse = True)
        sorted_result = sorted_result[:5]
        ## empty global result
        self.SearchedResult=[]
        ##for each docID -> termID, load title and url from Filedump
        for docID in sorted_result:
            try:
                loading = open(self.path +"\\"+ str(int(docID)) + ".txt")
                data = json.load(loading)
                title = data.get('title')
                title = title.strip()
                url = data.get('_id')
                self.SearchedResult.append([title,url])
            except:
                pass
        MessageLabel.config(text = "Search result for:"+str(query))

        ##if result is not enough, fill with blank
        while(len(self.SearchedResult) < 5):
            self.SearchedResult.append(["",""])
        ##display result
        self.__refreash__(resultDisplay)

    def __refreash__(self,resultDisplay):
        '''
        will update resultDisplay elements
        based on Global variable SearchedResult
        '''
        for i in range(len(self.SearchedResult)):
            resultDisplay.delete(i)
            resultDisplay.insert(i, self.SearchedResult[i][0])
        resultDisplay.pack()
    
    def __navigate__(self,resultDisplay,MessageLabel):
        '''
        based on global variable SearchedResult = [title,url]
        this will take index of selected line on resultDisplay
        and run default browser
        '''
        try:
            selection = resultDisplay.curselection()
            url = self.SearchedResult[int(selection[0])][1]
            if url == "":
                MessageLabel.config(text = "Selection has no URL")
                return
            webbrowser.open_new(url)
        except:
            MessageLabel.config(text = "please select url's title first")
        
if(__name__ == '__main__'):
    print("running Searcher")
    s = Searcher()
    print("program terminated")
    