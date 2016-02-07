import datetime
import redis

def participating_time(usr):
	r = redis.StrictRedis(host='localhost', port=6379, db=0)
	t1 = r.get("time_login:"+usr)
	t2 = r.get("time_logout:"+usr)
	dt1 = datetime.datetime.strptime(t1, "%Y-%m-%d %H:%M:%S.%f")
	dt2 = datetime.datetime.strptime(t2, "%Y-%m-%d %H:%M:%S.%f")
	pt = dt2 - dt1

	return pt

usr = '10204041785597745'
print participating_time(usr)