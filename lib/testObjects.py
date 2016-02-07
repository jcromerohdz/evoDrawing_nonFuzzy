__author__ = 'chris'
from py2neo import rel, node, neo4j, cypher
#import redis

graph_db = neo4j.GraphDatabaseService()

class Person(object):
    def __init__(self, name=None):
        self.name = name

    def get_person(self):

        try:
            query = "match (n) where n.username='" + self.name+ "' return n"
            #print query
            result, metadata = cypher.execute(graph_db, query)
            r = result[0][0]["username"]
        except:
            r ="error"
            #print r

        return r


person = "jakip30"
p = Person(person)
r = p.get_person()
print r