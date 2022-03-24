import asyncio
import motor.motor_asyncio
from aiohttp import web


# motor连接mongo数据库
client = motor.motor_asyncio.AsyncIOMotorClient("*********", 27017)

db = client["findjob"]


# 继承web.View
class Index(web.View):


	# 由于是异步，所以所有方法前面都要加async 将该方法变成协程
	# 协程具有传染性
    async def get(self):
    	# 所有请求数据库的操作都是异步的，所以用await将该操作挂起，motor已经所有对数据库操作变为一个协程对象
        res = await db.chinahr.find_one()
        print(res)
        res.pop("_id")
        # 注意返回的结果，一定要是web.response的实例
        # 返回 html页面
        # 注意如果只返回文本可以用text 后面是字符串
        # 如果body 后面只能接字节，并且注意编码，要和后面charset保持一致
        # content_type="text/html" 如果访问路由出现直接下载文件问题需要加上这个
        return web.Response(body=bytes(html,encoding='utf-8'), content_type='text/html', charset="utf-8")
        # 返回json格式数据
        # return web.json_response(res)


# 开启事件循环
loop = asyncio.get_event_loop()
# 将上面的事件循环合app绑定
app = web.Application(loop=loop)

# 注册路由
app.add_routes([web.get("/", Index)])

if __name__ == '__main__':
	# 启动服务命令
    web.run_app(app, port=20008, host="127.0.0.1")
