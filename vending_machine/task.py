import redis

rs = redis.StrictRedis(host='192.168.19.129',port=6379, db=1)
print(rs.set('ss', '33', 10))