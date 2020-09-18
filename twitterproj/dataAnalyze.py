
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

def dataCombine(start,end):
    dbtotal = cs562['alltweets']
    for day in range(start,end+1):
        tweetCount = 0
        newInsert = 0
        dbmoretags = cs562['moretags'+str(day)].find()
        dbtweets = cs562['tweets'+str(day)].find()
        for tag in dbmoretags:
            id = tag['id']
            already = dbtotal.find({'id': id}).count()
            tweetCount += 1
            if already == 0:
                newInsert += 1
                dbtotal.insert_one(tag)
        for tw in dbtweets:
            id = tw['id']
            already = dbtotal.find({'id': id}).count()
            tweetCount += 1
            if already == 0:
                newInsert += 1
                dbtotal.insert_one(tw)
        print(str(day) + ", Total " + str(tweetCount) + " tweets")
        print(str(day) + ", New Insert " + str(newInsert) + " tweets")
        print("\n")

def deleteSameUser():
    cs562.drop_collection('alltweets_norepeatuser')
    tweetCount = 0
    norepeat = 0
    dbtotalNoSameUser = cs562['alltweets_norepeatuser']
    dbtotal = cs562['alltweets'].find()
    for item in dbtotal:
        tweetCount += 1
        userid = item['user']['id']
        alreadyUser = dbtotalNoSameUser.find({'user.id':userid}).count()
        if alreadyUser == 0:
            norepeat += 1
            dbtotalNoSameUser.insert_one(item)
    print("Total " + str(tweetCount) + " tweets")
    print("No Repeat User Insert " + str(norepeat) + " tweets")
    print("\n")


def splitWithState():
    totalCount = cs562['alltweets_norepeatuser'].count()
    calculateCount = 0
    dbtotalNoSameUser = cs562['alltweets_norepeatuser'].find()
    for val in statesDict.values():
        cs562.drop_collection('tweets_' + str(val))
    for item in dbtotalNoSameUser:
        # print(item['place']['place_type'])
        item['_id'] = ObjectId()
        fullname = item['place']['full_name']
        l_fullname = fullname.split(', ')
        # print(l_fullname)
        if len(l_fullname) == 2:
            if l_fullname[1] == "USA":
                state = statesDict.get(l_fullname[0],None)
                if state != None:
                    # print(state)
                    # cs562.drop_collection('tweets_'+str(state))
                    already = cs562['tweets_'+str(state)].find({'id':item['id']}).count()
                    if already == 0:
                        calculateCount += 1
                        cs562['tweets_'+str(state)].insert_one(item)
            else:
                state = ""
                if l_fullname[1] in statesDict.values():
                    state = l_fullname[1]
                else:
                    state = statesDict.get(l_fullname[1],None)
                if state != None:
                    already = cs562['tweets_' + str(state)].find({'id': item['id']}).count()
                    if already == 0:
                        calculateCount += 1
                        cs562['tweets_' + str(state)].insert_one(item)
                    # print(state)
    print("Total " + str(totalCount) + " tweets")
    print("Added total " + str(calculateCount) + " tweets")
    print("\n")



def main():

    dataCombine(22, 30)
    dataCombine(1, 2)

    deleteSameUser()

    splitWithState()



if __name__ == '__main__':
    main()
