import socket
import asyncio
from asyncio_demo import DbOperation
from aiohttp import web
import sys
import conf
import uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

async def handle(request):
    op    = request.match_info.get('op', 'UnknownArgs')
    key   = request.match_info.get('key', 'UnknownArgs')
    value = request.match_info.get('value', 'UnknownArgs')
    
    # print('cmd: op={}, key={}, value={}'.format(op, key, value))
    
    if op == 'UnknownArgs':
        web.Response(text='invald op args')
        return
    
    if op == 'write':
        if key == 'UnknownArgs' or value == 'UnknownArgs':
            web.Response(text='invald key/value args')
            return
        result = await db_operation.do_insert_one(key, value)
        return web.Response(text=str(result.inserted_id))
    
    elif op == 'read':
        if key == 'UnknownArgs' or value == 'UnknownArgs':
            web.Response(text='invald key/value args')
            return
        result = await db_operation.do_find_one(key, value)
        return web.Response(text=str(result))
    
    elif op == 'readall':
        result = await db_operation.do_find_all()
        print('{} results found'.format(result))
        return web.Response(text=str(result))
        
    elif op == 'deleteall':
        result = await db_operation.do_delete_many(key)
        return web.Response(text=str(str(result) + ' doc was deleted'))

def http_server():
    app = web.Application()
    app.add_routes([web.get('/{op}', handle),
                    web.get('/{op}/{key}/{value}', handle)])
    # avoid conflict event loop
    web.run_app(app, loop=asyncio.get_event_loop(), port=conf.PORT)

async def tcp_server(port):
    s = socket.socket()
    s.bind(('0.0.0.0', port))
    s.listen(500)
    while True:
        cli, addr = s.accept()
        await asyncio.gather(db_operation.do_find_one())

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('python3 {} tcp/http'.format(sys.argv[0]))
        
    elif sys.argv[1] == 'tcp':
        loop = asyncio.get_event_loop()
        main_coroutine = tcp_server(conf.PORT)
        task = loop.create_task(main_coroutine)
        loop.run_until_complete(task)
        
    elif sys.argv[1] == 'http':
        db_operation = DbOperation()
        http_server()
        
    else:
        print('python3 {} tcp/http'.format(sys.argv[0]))
