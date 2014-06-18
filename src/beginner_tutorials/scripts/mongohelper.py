
import pymongo
from pymongo import MongoClient
import datetime
import sys
from wit import Wit

def startDatabase(database, collection):
    client = MongoClient()
    db = client.database
    collectionName = db.collection
    return collectionName

def addSonarData(collection, data1, data2, data3, data4, data5, data6, data7
    , data8, data9, data10, data11, data12, data13, data14, data15,
     data16, data17, data18, data19, data20, data21, data22, data23, data24):

    data = {"__topic" : "/sonar",
            "__recorded": datetime.datetime.utcnow(),
            "Sonardata": [data1, data2, data3, data4, data5, data6, data7
    , data8, data9, data10, data11, data12, data13, data14, data15,
     data16, data17, data18, data19, data20, data21, data22, data23, data24],
            }
    sonar_id = collection.insert(data)

    return sonar_id

def addBumpData(collection, data):
    output = {"__topic" : "/MotorState",
            "__recorded": datetime.datetime.utcnow(),
            "MotorState": data,
            }

    MotorID = collection.insert(output)
    return MotorID

def addSpeechData(collection, data):
    output = {"__topic": "/audio",
               "__recorded": datetime.datetime.utcnow(), 
               "Raw Text": data["msg_body"],
               "Entity": data["outcome"]["entities"],
               "Intent": data["outcome"]["intent"],
               "Confidence": data["outcome"]["confidence"],
            }
    try:
        SpeechID = collection.insert(output)
    except:
        print "Error in Speech data add"
    return SpeechID

def addMotionData(collection, data):
    output = {"__topic" : "/Motion",
        "__recorded": datetime.datetime.utcnow(),
        "Event": "Motion Detected",
        "Filaname": data,
        }

    try:
        MotionID = collection.insert(output)
        return MotionID
    except:
        print "Error in Motion data add"
    

def topicQuery(collection, topicname):
    for x in collection.find({"__topic": topicname}):
        print x

def speechQuery(collection, intentName):
    for x in collection.find({"Intent": intentName}):
        print x["Intentbg"]

def dateQuery(collection, date, option, topic):
        if option == "<":
            option = "$lt"
        if option == ">":
            option = "$gt"
        if option == "<=" or option == "=<":
            option = "$lte"
        if option == ">=" or option == "=>":
            option = "$gte"   
        if option == "!=":
            option = "$ne"                                  

        for x in collection.find({"__topic": topic,"__recorded": {option: date}}):
            print x

def speechConfidenceQuery(collection, confidence, option):
    if option == "<":
        option = "$lt"
    if option == ">":
        option = "$gt"

    for x in collection.find({"Confidence": {option: confidence}}):
        print x


if __name__ == '__main__':
    #Test Code to ensure functions are working
    collection_name = startDatabase("test_database", "sonarTest")
    sonar_id = addSonarData(collection_name, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
                        12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23 ,24)
    print sonar_id
    print collection_name.find_one(sonar_id)

    bumpCollection = startDatabase("test_database", "bumpTest")
    
    bump_id = addBumpData(bumpCollection, 0)
    print bump_id    
    print bumpCollection.find_one(bump_id)
    
    bump_id = addBumpData(bumpCollection, 1)
    print bump_id
    print bumpCollection.find_one(bump_id)

    witData = {'msg_body': 'right', 'msg_id': '36972b53-8506-4163-9142-f581aa0b1100', 'outcome': {'entities': {'Direction': {'body': 'right', 'start': 0, 'end': 5, 'value': 'right'}}, 'confidence': 0.602, 'intent': 'Right'}}
    witCollection = startDatabase("test_database", "AudioTest")

    wit_id = addSpeechData(witCollection, witData)
    print witCollection.find_one(wit_id)


    for x in witCollection.find({"__topic": "/audio"}):
        print x["Raw Text"]    
        print x["__recorded"]

    MotionCollection = startDatabase("test_database", "MotionTest")
    #motionId = addMotionData(witCollection, "FILENAME.JPG")
    
    #print MotionCollection.find_one(motionId)

    for x in MotionCollection.find({"__topic": "/Motion"}):
        print x
    topicQuery(witCollection, "/MotorState")

    date = datetime.datetime(2014, 6, 3, 23)

    dateQuery(witCollection, date, "<")    

    speechQuery(witCollection, "Right")

    speechConfidenceQuery(witCollection, 0.5, "<")

    sys.exit(0)