import math
import tweepy
import json
import sys
import os
import jsonpickle
import unicodedata

import pymongo
from pymongo import MongoClient

import config
import dataAnalyze


'''
First:

    pip install tweepy
    pip install jsonpickle
    pip install searchtweets
    
Install the tweepy, a Twitter Api Python Library

(May not using) Search Parameters:	
    q – the search query string
    lang – Restricts tweets to the given language, given by an ISO 639-1 code.
    locale – Specify the language of the query you are sending. This is intended for language-specific clients and the default should work in the majority of cases.
    rpp – The number of tweets to return per page, up to a max of 100.
    page – The page number (starting at 1) to return, up to a max of roughly 1500 results (based on rpp * page.
    since_id – Returns only statuses with an ID greater than (that is, more recent than) the specified ID.
    geocode – Returns tweets by users located within a given radius of the given latitude/longitude. The location is preferentially taking from the Geotagging API, but will fall back to their Twitter profile. The parameter value is specified by “latitide,longitude,radius”, where radius units must be specified as either “mi” (miles) or “km” (kilometers). Note that you cannot use the near operator via the API to geocode arbitrary locations; however you can use this geocode parameter to search near geocodes directly.
    show_user – When true, prepends “<user>:” to the beginning of the tweet. This is useful for readers that do not display Atom’s author field. The default is false.

'''


# MongoDB Setup with cs562 db
client = MongoClient()
cs562 = client['cs562']



# Auth with Tweepy
authT = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
authT.set_access_token(config.access_token, config.access_token_secret)

apiU = tweepy.API(authT)
if (not apiU):
    print ("Problem connecting to APIu")
print(apiU.rate_limit_status()['resources']['search'])

#Getting Geo ID for USA
# places = apiU.geo_search(query="USA", granularity="country")
#Copy USA id
# place_id = places[0].id
# print('USA id is: ',place_id)
# USA id is:  96683cc9126741d1



#Switching to application authentication
auth = tweepy.AppAuthHandler(config.consumer_key, config.consumer_secret)
#Setting up new api wrapper, using authentication only
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
if (not api):
    print ("Problem connecting to API")

print("Start: " + str(api.rate_limit_status()['resources']['search']))


''' 
Search with USA place code and key words
& TRY: without place id.
'''
searchQuery = '#nbafinals OR #nbaplayoffs'
searchQueryUSA = 'place:96683cc9126741d1 #nbafinals OR #nbaplayoffs'
#Maximum number of tweets we want to collect
maxTweets = 100000000
#The twitter Search API allows up to 100 tweets per query
tweetsPerQry = 100



def findTweets(start, end, db):
    tweetCount = 0
    newInsert = 0
    dbtweets = cs562[db]
    for tweet in tweepy.Cursor(apiU.search, q=searchQueryUSA,since=start,until=end).items(maxTweets):
        tweetCount += 1
        if tweet.place is not None:
            # Write the JSON format to the text file, and add one to the number of tweets we've collected
            j = tweet._json
            already = dbtweets.find({'id':tweet.id}).count()
            if already == 0:
                newInsert += 1
                dbtweets.insert_one(j)

    # Display how many tweets we have collected
    print(start + ", Downloaded "+str(tweetCount)+" tweets")
    print(start + ", New Insert "+str(newInsert)+" tweets")
    print(start + ", End: " + str(api.rate_limit_status()['resources']['search']))
    print('\n')


def findTweetsMoreTagsKeywords(start,end,db):
    tweetCount = 0
    newInsert = 0
    dbtweets = cs562[db]
    q = 'place:96683cc9126741d1 #nbaplayoffs OR #nbafinals'
    for tweet in tweepy.Cursor(api.search, q=q,since=start,until=end).items(maxTweets):
        tweetCount += 1
        if tweet.place is not None:
            # Write the JSON format to the text file, and add one to the number of tweets we've collected
            j = tweet._json
            already = dbtweets.find({'id':tweet.id}).count()
            if already == 0:
                newInsert += 1
                dbtweets.insert_one(j)

    # Display how many tweets we have collected
    print(start + ", Downloaded " + str(tweetCount) + " tweets")
    print(start + ", New Insert " + str(newInsert) + " tweets")
    print(start + ", End: " + str(api.rate_limit_status()['resources']['search']))
    print('')

    q = 'place:96683cc9126741d1 #teamlebron OR #CUsRise OR #PhilaUnite OR #HereTheyCome OR #StrengthInNumbers OR #DubNation OR #WarriorsGround'
    for tweet in tweepy.Cursor(api.search, q=q, since=start, until=end).items(maxTweets):
        tweetCount += 1
        if tweet.place is not None:
            # Write the JSON format to the text file, and add one to the number of tweets we've collected
            j = tweet._json
            already = dbtweets.find({'id': tweet.id}).count()
            if already == 0:
                newInsert += 1
                dbtweets.insert_one(j)

    # Display how many tweets we have collected
    print(start + ", Downloaded " + str(tweetCount) + " tweets")
    print(start + ", New Insert " + str(newInsert) + " tweets")
    print(start + ", End: " + str(apiU.rate_limit_status()['resources']['search']))
    print('\n')

    q = 'place:96683cc9126741d1 #RunAsOne OR #Rockets OR #WeTheNorth OR #WhateverItTakes OR #CavsPacers OR #Cavs OR #celtics OR #RTZ OR kingjames OR klow7 OR DeMar_DeRozan OR James Harden'
    for tweet in tweepy.Cursor(api.search, q=q, since=start, until=end).items(maxTweets):
        tweetCount += 1
        if tweet.place is not None:
            # Write the JSON format to the text file, and add one to the number of tweets we've collected
            j = tweet._json
            already = dbtweets.find({'id': tweet.id}).count()
            if already == 0:
                newInsert += 1
                dbtweets.insert_one(j)

    # Display how many tweets we have collected
    print(start + ", Downloaded " + str(tweetCount) + " tweets")
    print(start + ", New Insert " + str(newInsert) + " tweets")
    print(start + ", End: " + str(api.rate_limit_status()['resources']['search']))
    print('\n')



'''
Run the script.
'''

if __name__ == '__main__':
    print("get data from api by date")
    # findTweetsMoreTagsKeywords('2018-05-03','2018-05-04','moretags3')
    # findTweetsMoreTagsKeywords('2018-05-02','2018-05-03','moretags2')
    # findTweetsMoreTagsKeywords('2018-05-01','2018-05-02','moretags1')
    # findTweetsMoreTagsKeywords('2018-04-30','2018-05-01','moretags30')
    # findTweetsMoreTagsKeywords('2018-04-29','2018-04-30','moretags29')
    # findTweetsMoreTagsKeywords('2018-04-28','2018-04-29','moretags28')
    # findTweetsMoreTagsKeywords('2018-04-27','2018-04-28','moretags27')
    # findTweetsMoreTagsKeywords('2018-04-26','2018-04-27','moretags26')
    # findTweetsMoreTagsKeywords('2018-04-25','2018-04-26','moretags25')
    # findTweetsMoreTagsKeywords('2018-04-24','2018-04-25','moretags24')
    # findTweetsMoreTagsKeywords('2018-04-23','2018-04-24','moretags23')

    # findTweets('2018-05-02', '2018-05-03', 'tweets2')
    # findTweets('2018-05-01','2018-05-02','tweets1')
    # findTweets('2018-04-30','2018-05-01', 'tweets30')
    # findTweets('2018-04-29','2018-04-30', 'tweets29')
    # findTweets('2018-04-28','2018-04-29', 'tweets28')
    # findTweets('2018-04-27','2018-04-28', 'tweets27')
    # findTweets('2018-04-26','2018-04-27', 'tweets26')
    # findTweets('2018-04-25','2018-04-26', 'tweets25')
    # findTweets('2018-04-24','2018-04-25', 'tweets24')
    # findTweets('2018-04-23','2018-04-24', 'tweets23')
    # findTweets('2018-04-22','2018-04-23', 'tweets22')




# class MyStreamListener(tweepy.StreamListener):
#     # Overload the on_status method
#     def on_status(self, status):
#         try:
#             j = status._json
#             already = cs562['stream'].find({'id': status.id}).count()
#             if already == 0:
#                 cs562['stream'].insert_one(j)
#
#             # status.text = str(status.text.encode("utf-8"))
#             # print (status.text, "\n")
#             #
#             # data = {}
#             # data['text'] = status.text
#             # data['created_at'] = status.created_at
#             # data['geo'] = status.geo
#             # data['source'] = status.source
#             #
#             # cs562['stream'].insert(data)
#
#
#         # Error handling
#         except BaseException as e:
#             print("Error on_status: %s" % str(e))
#
#         return True
#
#     # Error handling
#     def on_error(self, status):
#         print("on_error "+str(status))
#         return True
#
#     # Timeout handling
#     def on_timeout(self):
#         return True
