
import pymongo
from pymongo import MongoClient
import datetime
import sys
from wit import Wit
import gridfs

# For Local Mongo DB databases
def startDatabase(database, collection):
    client = MongoClient()
    db = client.database
    collectionName = db.collection
    return collectionName

# All URI functions are for cloud based databases
def startBumpDatabaseURI(collection, uri):
    client = MongoClient(uri)
    db = client.get_default_database()
    collectionName = db.bumpCollection
    return collectionName

def startSonarDatabaseURI(collection, uri):
    client = MongoClient(uri)
    db = client.get_default_database()
    collectionName = db.SonarCollection
    return collectionName

def startSpeechDatabaseURI(collection, uri):
    client = MongoClient(uri)
    db = client.get_default_database()
    collectionName = db.SpeechCollection
    return collectionName

def startMotionDatabaseURI(collection, uri):
    client = MongoClient(uri)
    db = client.get_default_database()
    collectionName = db.MotionCollection
    return collectionName  

def startAlertDatabaseURI(collection, uri):
    client = MongoClient(uri)
    db = client.get_default_database()
    collectionName = db.AlertCollection
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
    sonar_id = collection.insert(data, True, True, True)

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

def addMotionData(collection, data, filename):
    client = MongoClient("URI")
    db = client.get_default_database()
    fs = gridfs.GridFS(db)
    data1 = open(filename, "rb")
    thedata = data1.read()
    stored = fs.put(thedata)

    output = {"__topic" : "/Motion",
        "__recorded": datetime.datetime.utcnow(),
        "Event": "Motion Detected",
        "Filename": data,
        "image": stored,
        }

    try:
        MotionID = collection.insert(output)
        return MotionID
    except:
        print "Error in Motion data add"

def addAlertData(collection, data):
    output = { "__topic": "/EVENT",
            "__recorded": datetime.datetime.utcnow(),
            "EVENT": data,
        }
    try:
        AlertID = collection.insert(output)
        return AlertID
    except:
        print "Error in Alert Data add"

def alertQuery(collection, date):
    for x in collection.find({"__recorded": {"$gt": date, "$lt": datetime.datetime.utcnow()},"__topic": "/EVENT"}):
        if(x is not None):
            return True
    return False


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
def ImageQuery(value, filename):
    client = MongoClient("URI")
    db = client.get_default_database()
    fs = gridfs.GridFS(db)
    out = fs.get(value["image"]).read()
    output = open(filename, "wb")
    output.write(out)
    output.close


def speechConfidenceQuery(collection, confidence, option):
    if option == "<":
        option = "$lt"
    if option == ">":
        option = "$gt"

    for x in collection.find({"Confidence": {option: confidence}}):
        print x


if __name__ == '__main__':
    date = datetime.datetime.utcnow()
    collection_name = startAlertDatabaseURI("AlertCollection", "URI")
    print collection_name
    
    alert_id = addAlertData(collection_name, "Some banterous alert data")
    
    print alertQuery(collection_name, date)
    # collection_name = startSonarDatabaseURI("SonarCollection", "URI")
    # print collection_name
    # sonar_id = addSonarData(collection_name, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23 ,24)
    # print sonar_id

    # print collection_name.find_one(sonar_id)

    # bumpCollection = startBumpDatabaseURI("bumpCollection", "URI")
    
    # print bumpCollection


    # bump_id = addBumpData(bumpCollection, 0)
    # print bump_id    
    # print bumpCollection.find_one(bump_id)
    
    # bump_id = addBumpData(bumpCollection, 1)
    # print bump_id
    # print bumpCollection.find_one(bump_id)

    # witData = {'msg_body': 'right', 'msg_id': '36972b53-8506-4163-9142-f581aa0b1100', 'outcome': {'entities': {'Direction': {'body': 'right', 'start': 0, 'end': 5, 'value': 'right'}}, 'confidence': 0.602, 'intent': 'Right'}}
    # witCollection = startSpeechDatabaseURI("SpeechCollection", "URI")
    # print witCollection
    # wit_id = addSpeechData(witCollection, witData)
    # print witCollection.find_one(wit_id)


    # for x in witCollection.find({"__topic": "/audio"}):
    #     print x["Raw Text"]    
    #     print x["__recorded"]

    # MotionCollection = startMotionDatabaseURI("MotionCollection", "URI")
    # #print MotionCollection
    # #motionId = addMotionData(MotionCollection, "FILENAME.JPG", "Filename.jpg")
    
    # for value in MotionCollection.find({"__recorded": {"$gt": datetime.datetime(2014, 6, 15, 19, 24)}}):
    #      temp = value     

    # #value = MotionCollection.find_one(temp)

    # ImageQuery(temp, "flyfly.jpg")


    

    # # y = bumpCollection.find({"__recorded": {"$gt": datetime.datetime(2014, 6, 8, 0), "$lt": datetime.datetime(2014, 6, 9, 0)}, "__topic": "/audio"}).count()
    # # print y




    #Write to Gridfs
    # client = MongoClient("URI")
    # db = client.get_default_database()
    # fs = gridfs.GridFS(db)
    # data = open("Banter.jpg", "rb")
    # thedata = data.read()
    # stored = fs.put(thedata)
    #Retrieve from Gridfs
    # out = fs.get(stored).read()
    # output = open("test.jpg", "wb")
    # output.write(out)
    # output.close

    # date = datetime.datetime(2014, 6, 3, 23)
    # dateQuery(witCollection, date, "<")    
    # speechQuery(witCollection, "Right")
    # speechConfidenceQuery(witCollection, 0.5, "<")
    sys.exit(0)