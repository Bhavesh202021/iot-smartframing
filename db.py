from pymongo import MongoClient
from datetime import datetime as dt
conn = MongoClient('mongodb+srv://bhavesh:bhau2021@cluster0.1mj5o.mongodb.net/test')

db = conn['test']

collName = db['realtimedata']
collName = db['charts']

def insertNewRecord(data):
    temperature= data['temperature']
    light= data['light']
    humidity=data['humidity']
    moistureLevel=data['moistureLevel']
    timeStamp = dt.now()
    k = collName.insert_one({"temperature":temperature,
                            "humidity":humidity,"light":light,
                            "moistureLevel":moistureLevel,"timeStamp":timeStamp})
    return k


def insertsoilRecord(select):
    soilmoisture = select
    timeStamp = dt.now()
    s = collName.insert_one({'moistureLevel':soilmoisture,"timeStamp":timeStamp})
    
    return s
    
    
    
