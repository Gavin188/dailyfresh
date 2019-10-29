import os

import django
from django.core.cache import cache
from django_redis import get_redis_connection

os.environ['DJANGO_SETTINGS_MODULE'] = 'dailyfresh.settings'
django.setup()
# 给redis中加入了键为key1，值为value1缓存，过期时间20秒
# cache.set('key1', 'value1', 20)
# 参数：timeout=20, 过期时间20
# nx=True. 默认为False，重复命名时覆盖，True表示重复命名时不能再重新赋值

# # 获取cache值：
# val = cache.get('key1')
#
# print(val)
# # # # 获取key3的过期时间，返回值：0表示无此键或已过期，None表示未设置过期时间，有过期时间的返回秒数。
# time = cache.ttl('key1')
# # #
# print(time)
# # # 注意：在redis中存储的值并不是按照给定的键存储的，是根据键值又拼装的键(在你的key前面加上了个“:1:”)。
# # # # 删除redis中key1的值
# # # cache.delete('key1')
# '''-------------------------------------'''
# from django_reids import get_redis_connection
# get_redis_connection(‘default’)用法：
Conn = get_redis_connection('default')
# 表示网redis里面存入了数据，键key1，值val1，但是注意不能再redis中获取，只能用conn获取，
# 返回值是添加量，初始为1.0，如果再加一个一摸一样的，就是2.0，注意：可以往一个键中添加多个值，如
Conn.zincrby('key1', '333', 1)
# Conn.zincrby('key1', 'HELLO', 1)
# Conn.zincrby('key1', 'ooo', 1)
# Conn.zincrby('key1', 'world', 1)
Conn.zincrby('key2', '444', 1)
Conn.zincrby('key2', '444', 1)
Conn.zincrby('key2', '444', 1)  # 注意：这里val5添加了3次
# 如何获取刚才添加的呢？
li1 = Conn.zrevrange('key1', 0, 10, True)
print(li1)
# li1就是：[('444', 3.0), ('world', 1.0), ('ooo', 1.0), ('HELLO', 1.0), ('333', 1.0)]
# 得到的数据是一个列表，取其中0-10(前10)，按照刚才添加次数排序，val5添加了3次，所以权重值最大
# True表示，获得的值是个元组，False的话里面没有权重值，默认False
li2 = Conn.zrevrange('key1', 0, 10)
print(li2)
# li2就是：['444', 'world', 'ooo', 'HELLO', '333']
# 我统计热搜关键词排序用到了
#他们做watch项目的 星期天也可以加班