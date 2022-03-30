import motor.motor_asyncio
import conf

class DbOperation:
    def __init__(self):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(
                conf.LINK, 
                serverSelectionTimeoutMS=conf.TIMEOUT)
        self._db = self._client[conf.DBNAME]
    
    async def get_server_info(self):
        try:
            print(await self._client.server_info())
        except Exception:
            print("Unable to connect to the server.")

    async def do_insert_one(self, key, value):
        document = {str(key): str(value)}
        print(document)
        result = await self._db.test_database.insert_one(document)
        print('result %s' % repr(result.inserted_id))
        return result

    async def do_find_one(self, key, value):
        document = await self._db.test_database.find_one({str(key): str(value)})
        print('{} {}'.format(__name__, document))
        return document

    async def do_find_all(self):
        i = 0
        async for doc in self._db.test_database.find({}):
            # print('result {}: {}'.format(i, doc))
            i += 1
        return i

    async def do_delete_many(self, key):
        coll = self._db.test_database
        before = await coll.count_documents({})
        print('%s documents before calling delete_many()' % before)
        await self._db.test_database.delete_many({str(key): {'$gt': '0'}})
        after = await coll.count_documents({})
        print('%s documents after calling delete_many()' % after)
        return before - after
