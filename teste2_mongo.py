import pymongo
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["customersdb"]
customers = db["customers"]
for x in customers.find():
    print(x)
