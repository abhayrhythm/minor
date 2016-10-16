from django.shortcuts import render
from nltk.corpus import stopwords
from nltk import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import sent_tokenize
import json
import numpy as np
import os.path

list=[]
cachedStopWords = stopwords.words("english")
list=cachedStopWords

docs_len={}
d1hash={}
count=0


def removestop(s):
    text =s
    text = ' '.join([word for word in text if word not in cachedStopWords])
    return text


def stem(s):
    text=""
    for word in s.split():
        text=text+PorterStemmer().stem_word(word)+" "

    return text


def sentencemaker(s,var):
    tokenizer = RegexpTokenizer(r'\w+')
    sent_tokenize_list = sent_tokenize(s)
    l=len(sent_tokenize_list)
    fo = open("preprocess/Files2/"+str(var)+".txt", "w", encoding="utf-8")
    for sentence in sent_tokenize_list:
        v = tokenizer.tokenize(sentence)
        v=removestop(v)
        v=stem(v)
        fo.write(v+"\n")
    fo.close()


def applynlp(var):
    fo = open("preprocess/Files/"+str(var)+".txt", "r", encoding="utf-8")
    str2 = fo.read()
    str2 = str2.strip()
    str2 = str2.lower()
    fo.close()
    sentencemaker(str2,var)


def makestructd1hash(var):
    global docs_len
    global d1hash
    fo=open("preprocess/Files2/"+str(var)+".txt","r",encoding="utf-8")
    str2=fo.read()
    fo.close()
    list=str2.strip().split()
    for i in list:
        if d1hash.get(i,"null")!="null":
            wordcounthash=d1hash.get(i)
            if d1hash.get(i).get(var,"not")!="not":
                d1hash.get(i)[var]=d1hash.get(i).get(var)+1

            else:

                wordcount=1
                wordcounthash[var]=wordcount
                d1hash[i] = wordcounthash

        else:
            d1hash[i]={}
            wordcount=1
            d1hash[i][var]=wordcount
    docs_len[var]=len(list)


def makestruct():
    global count
    path = 'preprocess/Files'
    count=len([f for f in os.listdir(path)
                     if os.path.isfile(os.path.join(path, f))])

    for i in range(1, count + 1):
        print("processing nlp of document :" + str(i))
        applynlp(i)
    for i in range(1, count + 1):
        print("processing document for d1hash :" + str(i))
        makestructd1hash(i)

def process(request):
    global d1hash
    makestruct()
    print("successfully created d1hash")
    print(count)
    np.save("preprocess/results/d1hash.npy", d1hash)
    np.save("preprocess/results/docslenhash.npy", docs_len)
    values = [{"words": k, "document reference": v} for k, v in d1hash.items()]
    fo = open("preprocess/results/d1hash.json", "w")
    fo.write(json.dumps(values, indent=4))
    fo.close()
    return render(request, 'preprocess/preprocessedsuccess.html', {})
