from gevent import monkey; monkey.patch_all()
from gevent.pywsgi import WSGIServer
from pymongo import MongoClient
import conf

def db_init():
    conn = MongoClient(conf.LINK)
    db = conn[conf.DBNAME]
    docs = db.test_database
    return docs

def db_operation(args_str):
    args_list = args_str.split('/')
    
    if args_list[0] == 'read':
        results = docs.find()
        # result_str = ''
        # for result in results:
        #     result_str += str(result) + '\n'
        # print(result_str)
        return str(results.count())

    elif args_list[0] == 'write':
        doc = {str(args_list[1]): str(args_list[2])}
        return str(docs.insert_one(doc).inserted_id)
    
    elif args_list[0] == 'deleteall':
        before = docs.count_documents({})
        docs.delete_many({str(args_list[1]): {'$gt': '0'}})
        after = docs.count_documents({})
        return '{} docs was deleted'.format(before - after)
    
    else:
        return 'invaild args'

def application(environ, start_response):
    result = db_operation(environ['PATH_INFO'][1:])
    start_response("200 OK", [('Content-Type', 'text/html')])
    return [result.encode()]

if __name__ == '__main__':
    docs = db_init()
    server = WSGIServer(('0.0.0.0', conf.PORT), application)
    server.serve_forever()
