__author__ = 'chris'
import redis, json
import time, datetime
import ast

class Activity_stream(object):
    #def __init__(self):
        #self.created = str(datetime.datetime.now())

    def activity(self, actor, verb, target, user_id):
        published = str(datetime.datetime.now())

        # Necesito inicializar una lista desde redis ????
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        #r.set("counter", 0)
        #activity_list=[]


        counter = int(r.get("counter")) + 1
        r.set("counter", counter)
        user_string = user_id +":"+ str(counter)
        d = {"user:"+user_string:{"published":published,
                                                    "actor":{"objectType":actor, "id":user_id},
                                            "verb":verb,
                                            "object":{"objectType":"evospaceApp",
                                                                    "displayName":"evospace interactive"},
                                            "target": {"objectType": target,
                                                          "displayName": target}}}
        r.lpush("activity_list", str(d))
        #print "$$$$$$$$$$$$$$$$$$$$$$"
        #print "activity list"
        r.lpush("user:"+user_id, str(d))


        #user_activity = r.lrange("activity_list", 0, -1)

        #print "################"
        #user_list = r.lrange("user:"+user_id, 0, -1)

        m = "user activity added!"

        #print m
        #print user_list
        #print user_activity
        #print len()

    def experience(self, user_id):
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        user_list = r.lrange("user:"+user_id, 0, -1)

        experience = 0

        for activity in user_list:
            s = activity.replace("'", "\"")
            d = ast.literal_eval(s)
            fk = d.keys()

            if d[fk[0]]['verb'] == 'like':
                experience = experience + 1

            if d[fk[0]]['verb'] == 'join':
                experience = experience + 2

            if d[fk[0]]['verb'] == 'save':
                experience = experience + 3

            if d[fk[0]]['verb'] == 'open':
                experience = experience + 2

        r.set("user_id", experience)
        total = int(r.get("user_id"))

        if total >= 100:
            exp_rate ='100'
        else:
            exp_rate =r.get("user_id")



        return exp_rate


