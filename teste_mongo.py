import pymongo  # package for working with MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
#use robo3t to visualize the entire database. Please install Robo3t via synaptic on Ubuntu
db = client["customersdb"]
customers = db["customers"]
customers_list = [
    {"name": "Amy", "address": "Apple st 652"},
    {"name": "Hannah", "address": "Mountain 21"},
    {"name": "Michael", "address": "Valley 345"},
    {"name": "Sandy", "address": "Ocean blvd 2"},
    {"name": "Betty", "address": "Green Grass 1"},
    {"name": "Richard", "address": "Sky st 331"},
    {"name": "Susan", "address": "One way 98"},
    {"name": "Vicky", "address": "Yellow Garden 2"},
    {"name": "Ben", "address": "Park Lane 38"},
    {"name": "William", "address": "Central st 954"},
    {"name": "Chuck", "address": "Main Road 989"},
    {"name": "Viola", "address": "Sideway 1633"}
]
# print list of the _id values of the inserted documents:
x = customers.insert_many(customers_list)
print(x.inserted_ids)
