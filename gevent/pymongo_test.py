from pymongo import MongoClient
import conf
import write_10
import write_100

conn = MongoClient(conf.LINK)
db = conn[conf.DBNAME]

data = {'1': str(write_100.msg)}
id = db.test_database.insert_one(data).inserted_id
print(id)

result = db.datas.find()
for doc in result:
    print(doc)
    
exit()

print('{} docs before delete'.format(db.datas.count_documents({})))
db.datas.delete_many({'pymongo_test': {'$gt': '0'}})
print('{} docs after delete'.format(db.datas.count_documents({})))
