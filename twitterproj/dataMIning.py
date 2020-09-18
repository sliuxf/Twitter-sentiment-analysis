# CS562 Project Step 3
# Created by Xuefei Liu
# Creates new text files to store the tweets.
# One text file per state
import os
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient()
cs562 = client['cs562']

statesDict = {
    'Alabama': 'AL',
    'Montana': 'MT',
    'Alaska': 'AK',
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
    'Missouri': 'MO',
    'Wyoming': 'WY'
}



def getTextFromTweets():
    for x in statesDict.values():
        statedb = cs562['tweets_'+str(x)].find() #collections
        twts = []
        for item in statedb:     # item = object
            text = item['text']  # twitter text
            temp = ""
            for line in text.split("\n"):
                temp += line + " "
            twts.append(temp+"\n")
        f = open("analyzeFile/" + str(x)+".txt","w+")
        for i in range(len(twts)):
            f.write(twts[i])
        f.close()        

if __name__ == '__main__':
    getTextFromTweets()
