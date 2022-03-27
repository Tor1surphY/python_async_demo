from pymongo import MongoClient

import conf

conn = MongoClient(conf.LINK)
db = conn[conf.DBNAME]

data = {'pymongo_test': '2022-03-27'}
id = db.datas.insert_one(data).inserted_id
print(id)

result = db.datas.find()
for doc in result:
    print(doc)

print('{} docs before delete'.format(db.datas.count_documents({})))
db.datas.delete_many({'pymongo_test': {'$gt': '0'}})
print('{} docs after delete'.format(db.datas.count_documents({})))
