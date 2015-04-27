# test
from __future__ import division
from bs4 import BeautifulSoup
import nltk, re, pprint, os, math, operator

path="C:\\Users\\spyros\\Downloads\\diplomatiki\\work\\s\\"

lst=os.listdir(path)

#frequency of term in document
def freq(term, doc):
    return doc.count(term)

def word_count(doc):
    return len(doc)

#normalized freq. Raw freq devided by #of terms in doc
def tf(word, doc):
    return (freq(word, doc) / float(word_count(doc)))

#number of documents containing term
def ndc(word):
    return len(test_dictionary[word])

#calculate idf = log(N/dFt) N=number of documents, dFt=number of documents containing the term 
def idf(word):
    return (math.log(len(lst)/float(ndc(word))))

#term - [list of document names containing term] 
test_dictionary={}

#document: [list of words with the highest tfidf]
keywords={}

#for every file
for doc in lst:
    print(doc)
    p=path+'\\'+doc
    
    #open file
    f=open(p, encoding='utf8')
    #read file
    rtext=f.read()

    #remove \n
    text=rtext.replace('\n','')

    #clean html
    soup= BeautifulSoup(text)
    texts= soup.findAll(text=True)
    v_texts = []
    for text in texts:
        if text.parent.name not in ['style', 'script', '[document]', 'head', 'title']:
            if len(text) > 30:
                v_texts.append(text)

    f_text=''.join(v_texts)

    #tokenize
    tokens=nltk.word_tokenize(f_text)

    #get lemmas
    wnl=nltk.WordNetLemmatizer()
    lemmas=[wnl.lemmatize(t) for t in tokens]

    lemmas = [lem.lower() for lem in lemmas if len(lem) > 2]

    #number of terms in the document(lemmas)
    doc_len=len(lemmas)

    #dictionary holding tfidf of doc's terms
    l_dict={}

    #for each term
    for word in lemmas:
    
        #if the word has been added to the dict, add the doc name only once
        if word in test_dictionary:
            if doc not in test_dictionary[word]:
                test_dictionary[word].append(doc)
        #else add the word and the name of the doc
        else:
            test_dictionary[word]=[doc]
            
        #calculate (normalized) tf
        tfa=tf(word, lemmas)

        #calculate idf
        idfaa=idf(word)

        #tfidf
        tfidfa=tfa*idfaa

        if word not in l_dict:
            l_dict[word]=tfidfa

    #keywords of document
    keys=[]

    #sorted list of (term, tfidf) 
    s_list=sorted(l_dict.items(), key=operator.itemgetter(1), reverse=True)

    #take the 10 keywords with the highest tfidf
    keys=[x for x in s_list][:15]

    #save it
    keywords[doc]=keys

    print("done")

print("all done\n")
