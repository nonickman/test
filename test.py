# test
from __future__ import division
from bs4 import BeautifulSoup
import nltk, re, pprint, os, math, operator

#path to folder with the html files
path="C:\\Users\\spyros\\Downloads\\diplomatiki\\work\\s\\"

#stopwords
stopwords = nltk.corpus.stopwords.words('english')

lst=os.listdir(path)

wnl=nltk.WordNetLemmatizer()

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

#clean file from html tags and comments
def clean_html(rtext):
    #remove html comments
    text = re.sub("<!.*?>", "", rtext)
    
    #clean html tags
    soup= BeautifulSoup(text)
    texts= soup.findAll(text=True)
    v_texts = []
    for text in texts:
        if text.parent.name not in ['style', 'script', '[document]', 'head', 'title']:
            if len(text) > 30:
                v_texts.append(text)

    f_text=''.join(v_texts)
    return f_text

#tokenize cleaned html, lemmatize, ignore stopwords
def get_lemmas(f_text):
    #tokenize
    tokens=nltk.word_tokenize(f_text)

    #lemmatize
    lemmas=[wnl.lemmatize(t) for t in tokens]

    #ignore words with 2 or less letters
    lemmas=[lem.lower() for lem in lemmas if len(lem) > 2]

    #ignore stopwords
    lemmas=[word for word in lemmas if word not in stopwords]

    return lemmas

def get_keywords(lemmas):
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

    #sorted list of (term, tfidf) 
    s_list=sorted(l_dict.items(), key=operator.itemgetter(1), reverse=True)

    #take the terms with the highest tfidf
    keys=[x[0] for x in s_list][:30]
    
    return keys

#save the cleaned html to txt
def savecleaned(cleaned):
    t="%s.txt"%doc
    txt_file=open(t, "w")
    txt_file.write(cleaned)
    txt_file.close()

#print keywords and save them to txt
def prnt_keywords():
    t="keywords.txt"
    txt_file=open(t, "w")
    for key, val in keywords.items():
        m="\n"+key+"\n"
        txt_file.write(m)
        n=' '.join(str(x) for x in val)
        p=n+"\n"
        txt_file.write(p)
        print("\n[Article]: ", key, "\n[Keywords]: ", val)
    txt_file.close()


#term - [list of document names containing term] 
test_dictionary={}

#document: [list of words with the highest tfidf]
keywords={}

#for every file
for doc in lst:
    print("File: ", doc)
    p=path+'\\'+doc
    
    #open file
    f=open(p, encoding='utf8')
    #read file
    rtext=f.read()
    #close file
    f.close()
    
    #clean
    f_text=clean_html(rtext)
    
    #testing!!!! save cleaned html to txt
    savecleaned(f_text)

    #tokenize-lemmatize-remove stopwords
    lemmas=get_lemmas(f_text)

    #get keywords by calculating tfidf of each term. return dictionary
    keywords[doc]=get_keywords(lemmas)

prnt_keywords()
