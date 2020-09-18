# CS562 project step 4
# Created by Xuefei Liu

import nltk
import numpy as np
import math
from scipy.sparse import coo_matrix
import os
from sklearn.feature_extraction.text import TfidfVectorizer
import textmining
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, TweetTokenizer
from nltk.stem import *
from numpy.linalg import inv
from sklearn.metrics.pairwise import cosine_similarity

from pymongo import MongoClient


client = MongoClient()
cs562 = client['cs562']


statesDict = {
    'Alabama': 'AL',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Arizona': 'AZ',
    'Nevada': 'NV',
    'Arkansas': 'AR',
    'New Hampshire': 'NH',
    'California': 'CA',
    'New Jersey': 'NJ',
    'Colorado': 'CO',
    'New Mexico': 'NM',
    'Connecticut': 'CT',
    'New York': 'NY',
    'Delaware': 'DE',
    'North Carolina': 'NC',
    'Florida': 'FL',
    'North Dakota': 'ND',
    'Georgia': 'GA',
    'Ohio': 'OH',
    'Hawaii': 'HI',
    'Oklahoma': 'OK',
    'Idaho': 'ID',
    'Oregon': 'OR',
    'Illinois': 'IL',
    'Pennsylvania': 'PA',
    'Indiana': 'IN',
    'Rhode Island': 'RI',
    'Iowa': 'IA',
    'South Carolina': 'SC',
    'Kansas': 'KS',
    'South Dakota': 'SD',
    'Kentucky': 'KY',
    'Tennessee': 'TN',
    'Louisiana': 'LA',
    'Texas': 'TX',
    'Maine': 'ME',
    'Utah': 'UT',
    'Maryland': 'MD',
    'Vermont': 'VT',
    'Massachusetts': 'MA',
    'Virginia': 'VA',
    'Michigan': 'MI',
    'Washington': 'WA',
    'Minnesota': 'MN',
    'West Virginia': 'WV',
    'Mississippi': 'MS',
    'Wisconsin': 'WI',
    'Missouri': 'MO'
    
}



stopWords = ['a','able','about','across','after','all','almost','also','am',
             'among','an','and','any','are','as','at','be','because','been',
             'but','by','can','cannot','could','dear','did','do','does','either',
             'else','ever','every','for','from','get','got','had','has',
             'have','he','her','hers','him','his','how','however','i','if','in',
             'into','is','it','its','just','least','let','like','likely',
             'may','me','might','most','must','my','neither','no','nor','not',
             'of','off','often','on','only','or','other','our','own','rather',
             'said','say','says','she','should','since','so','some','than','that',
             'the','their','them','then','there','these','they','this','tis',
             'to','too','twas','us','wants','was','we','were','what','when',
             'where','which','while','who','whom','why','will','with','would',
             'yet','you','your']

def remove(lst,i):
    for twts in lst:
        for words in twts:
            if not words in stopWords:
                appendFile = open("analyzeFile/mod"+str(i)+".txt",'a')
                appendFile.write(" "+ words)
                appendFile.close()
                
        newLine = open("analyzeFile/mod"+str(i)+".txt",'a')
        newLine.write("\n")
        newLine.close()
    



def stems(x):
    word = []
    f = open(x)
    twts = f.readlines()
    for line in twts:
        lst = []
        tknzr = TweetTokenizer()
        twtstoken = tknzr.tokenize(line)
        for t in twtstoken:
            lst.append(SnowballStemmer("english").stem(t))
        word.append(lst)
    return word


def documentTermMatrix(x):       # count the frequencies of non-stop words
    temp=[]
    result=[]
    tdm = textmining.TermDocumentMatrix()
    #print("mod"+str(x)+".txt")
    with open("analyzeFile/mod"+str(x)+".txt") as f:
        for line in f:
            tdm.add_doc(line)
    # f = open("mod"+str(x)+".txt")
    # for line in f.read():
    #     tdm.add_doc(line)
    for row in tdm.rows(cutoff=1):
        temp.append(row)
    for i in range(1,len(temp)):
        result.append(temp[i])
    return result

def tf(matrix):                 # tf
    #print(x)
    col = len(matrix[0])
    leng = len(matrix)
    result = [[0 for x in range(col)] for y in range(leng)]
    for i in range(leng):
        count=0
        # print("\n\n\n")
        # print("i is: " + str(i))
        for j in range(col):
            count += matrix[i][j]
            # print("tf matrix[j][i]: " + str(matrix[i][j]))
        for k in range(col):
            # print("tf result matrix[i][k]: " + str(count))
            result[i][k]=matrix[i][k]/count
        # print("i is: " + str(i))
        print("\n")
    return result

def idf(matrix):                # idf
    col = len(matrix[0])
    leng = len(matrix)
    result = [[0 for x in range(col)] for y in range(leng)]
    for i in range(col):
        count=0
        for j in range(leng):
            if(matrix[j][i]>0):
                # print("idf matrix[j][i]: " + str(matrix[j][i]))
                count+=1
        for k in range(leng):
            result[k][i]=math.log(leng/count,10)
    return result

def tfidf(tf, idf):             # tf*idf
    col = len(tf[0])
    leng = len(tf)
    result = [[0 for x in range(col)] for y in range(leng)]
    for i in range(leng):
        for j in range(col):
            result[i][j]=tf[i][j]*idf[i][j]
    return result

def vectors(f,x):              # file's concept: 0 or 1 
    print("in vectors"+ str(x))
    lst = []
    q=open(f)
    line = q.read()
    words = word_tokenize(line)
    print(words)
    for w in words:
        lst.append(SnowballStemmer("english").stem(w))
    test = []
    tdm = textmining.TermDocumentMatrix()
    with open("analyzeFile/mod"+str(x)+".txt") as k:
        for line in k:
            tdm.add_doc(line)
    for row in tdm.rows(cutoff=1):
        test.append(row)
    #s = 1
    leng = len(test[0]);
    result = [[0 for x in range(1)] for y in range(leng)]
    for i in range(len(lst)):
        for j in range(leng):
            if(lst[i]==test[0][j]):
                result[j][0]=1
    return result

def construct():
    cs562.drop_collection('stateResult')
    for x in statesDict.values():
        remove(stems("analyzeFile/" + str(x)+".txt"),x)
    for name in statesDict.values():
        eastCount = 0
        westCount = 0
        sameCount = 0
        # name = "FL"
        a1=documentTermMatrix(name)
        #if x == "ME":
        # print(a1)
        l=tf(a1)
        #if x == "ME":
        #print("tf"+str(a1))
        k=idf(a1)
        #if x == "ME":
        #print("idf"+str(a1))
        a2=tfidf(l,k)
        a1=np.array(a1)
        a1=a1.transpose()
        a2=np.array(a2)
        a2=a2.transpose()
        #if x == "ME":
        #print(a2)

        u, s, vh = np.linalg.svd(a2, full_matrices=False)
        u = np.array(u)
        transpose_u = u.transpose()
        stateTweetCount = cs562['tweets_'+str(name)].find().count()
        intState = round(stateTweetCount*0.8)
        w, h = len(transpose_u[0]), intState;
        transpose_u_10 = [[0 for x in range(w)] for y in range(h)]
        for x in range(len(transpose_u_10)):
            for y in range(len(transpose_u_10[0])):
                transpose_u_10[x][y] = transpose_u[x][y]
        w, h = intState, intState;
        s_10 = [[0 for x in range(w)] for y in range(h)]
        for x in range(len(s_10)):
            s_10[x][x] = s[x]
        print(str(name) + " s_10 is: " + str(s_10))
        inverse_s_10 = inv(np.array(s_10))
        lsi_inter_2 = np.matmul(inverse_s_10, transpose_u_10)
        lsiF2 = np.matmul(lsi_inter_2, a1)
        
        print("before vectors"+ str(name))
        query1 = vectors("west.txt",name)
        print("q1 is \n"+str(query1))
        query1 = np.array(query1)
        q_1 = np.matmul(lsi_inter_2, query1)
        lsiF2_transpose = np.transpose(lsiF2)
        q_1_transpose = np.transpose(q_1)
        print("\nq_1_transpose\n\n"+str(q_1_transpose))
        print("\nlsiF2_transpose\n\n"+str(lsiF2_transpose))
        west = cosine_similarity(q_1_transpose, lsiF2_transpose)
        print("\ncosine similarity\n\n"+str(west))
        
        query2 = vectors("east.txt",name)
        #print("q1 is \n"+str(query2))
        query2 = np.array(query2)
        q_2 = np.matmul(lsi_inter_2, query2)
        lsiF2_transpose = np.transpose(lsiF2)
        q_2_transpose = np.transpose(q_2)
        #print("\nq_2_transpose\n\n"+str(q_2_transpose))
        #print("\nlsiF2_transpose\n\n"+str(lsiF2_transpose))
        east = cosine_similarity(q_2_transpose, lsiF2_transpose)
        #print("\ncosine similarity\n\n"+str(east))
        #print(east[0][0])
        index = 0
        for westItem in west[0]:
            eastItem = east[0][index]
            if westItem > eastItem:
                westCount += 1
            elif westItem < eastItem:
                eastCount += 1
            else:
                eastCount += 1
                westCount += 1
                sameCount += 1
            index += 1
        support = ""
        if westCount >= eastCount:
            support = "west"
        else:
            support = "east"

        dic = {'state':name,
               'support':support,
               'totalTweets':stateTweetCount,
                'westCount':westCount,
                'eastCount':eastCount,
               'sameCount':sameCount}
        cs562['stateResult'].insert_one(dic)


if __name__ == '__main__':
    construct()
    for x in statesDict.values():
        os.remove("analyzeFile/mod"+str(x)+".txt")
