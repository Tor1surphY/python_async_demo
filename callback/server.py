from socket import AF_INET, SOCK_STREAM, socket
import threading
import conf
from pymongo import MongoClient

def db_init():
    conn = MongoClient(conf.LINK)
    db = conn[conf.DBNAME]
    docs = db.test_database
    return docs    
    
def do_find(sock, key):
    results = test_database.find()
    response = str(results.count())
    print('{} results found'.format(response))
    response += '\n\n'
    response_start_line = "HTTP/1.1 200 OK\r\n"
    response_headers = "Server: My server\r\n"
    response = response_start_line + response_headers + "\r\n" + response
    sock.send(response.encode())
    sock.close()
    
def func(sock):
    key = ''
    url = sock.recv(1024).decode()
    headers = url.split('\n')
    op = headers[0].split('/')[1].split(' ')[0]
    if op == 'readall':
        return do_find, key

def db_operation(sock, func):
    callback, key = func(sock)
    callback(sock, key)

def start_server():
    server_sock = socket(AF_INET, SOCK_STREAM)
    server_sock.bind(('127.0.0.1', 8080))
    server_sock.listen(5)
    while True:
        sock, addr = server_sock.accept()
        t = threading.Thread(target=db_operation, args=(sock, func))
        t.start()

if __name__ == '__main__':
    test_database = db_init()
    start_server()
