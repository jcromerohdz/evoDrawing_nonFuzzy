__author__ = 'chris'

import time, datetime
from py2neo import rel, node, neo4j, cypher
from py2neo import packages

from py2neo import ServiceRoot
import os

graphenedb_url = os.environ.get("http://app47206011-hOD5pp:7MSXfHJkDqy4Gt28exdc@app47206011hod5pp.sb02.stations.graphenedb.com:24789", "http://localhost:7474/")
graph_db = ServiceRoot(graphenedb_url).graph


#import redis
# conectarse a graphene service
#import os
#from py2neo.packages.urimagic import URI
#GRAPHENEDB_URL = "http://app29381869:UsGfVXqOMl2AQAe2gW2Z@app29381869.sb02.stations.graphenedb.com:24789"
#graphenedb_url = os.environ.get("GRAPHENEDB_URL", "http://localhost:7474/")
#graph_db=service_root.graph_db

#local  ne4j
#graph_db = neo4j.GraphDatabaseService()



class Nodo(object):
    def __init__(self):
        self.created = str(datetime.datetime.now())

    def create_nodo(self, **kwargs):
        d={"created":self.created}
        for item in kwargs.items():
            d.update({item[0]:item[1]})

        print "$$$$$$$$$$Diccionario para creacion de nodo$$$$$$$"
        print d
        if d["element_type"] == "person":
            person = graph_db.create(node(d))
            person[0].add_labels("User", "Person")
            m = "Node Created!"
            print m
        elif d["element_type"] == "individual":
            #individual = graph_db.create(node(**d))
            individual = graph_db.create(node(element_type=d["element_type"],
                                              id=d["id"],
                                              chromosome=str(d["chromosome"]),
                                              views=d["views"]))
            individual[0].add_labels("Individuals", "Individual")
            m = "Node Created!"
            print m
        elif d["element_type"] == "Collection":
            collection = graph_db.create(node(d))
            collection[0].add_labels("Collections", "Collection")
            m = "Node Created!"
            print m
        return m

    def get_nodo(self, name=None):
        self.p = name
        query = "match (n) where n.name='" + self.p+ "' return n"
        result, metadata = cypher.execute(graph_db, query)
        r = result[0][0]["name"]
        return r




class Person(object):

    def get_person(self, name=None):
        self.p = name
        try:
            query = "match (n) where n.name='" + self.p + "' return n"
            #print query
            result, metadata = cypher.execute(graph_db, query)
            r = result
        except:
            r ="error"
            #print r

        return r

    def get_relation_knows(self, name_user=None, name_friend=None):
        self.p = name_user
        self.f = name_friend
        try:
            "Este es:"
            query = "MATCH n-[r]-b WHERE n.id='" + self.p+ "' RETURN count(b)"
            print query
            result, metadata = cypher.execute(graph_db, query)
            r = result
        except:
            r ="error"
            print r

        return r

    def get_participation(self, ide=None):
        self.p = ide
        
        try:
            #"Participaciones"
            query = "MATCH n-[r]-b WHERE n.id='" + self.p + "' RETURN count(b)"
            print query
            result, metadata = cypher.execute(graph_db, query)
            r = result
        except:
            r ="error"
            print r

        return r

    def get_lider_board(self):
        #self.p = ide
        
        try:
            #"Participaciones"
            query = "MATCH n-[r]-() where n.element_type='person' return n.name as user, count(r) as score order by count(r) DESC"
            print query
            result, metadata = cypher.execute(graph_db, query)
            r = result
        except:
            r ="error"
            print r

        return r


class GraphCollection(object):

    def get_collection(self, name=None):
        self.p = name
        try:
            query = "match (n) where n.name='" + self.p + "' return n"
            #print query
            result, metadata = cypher.execute(graph_db, query)
            r = result
        except:
            r ="error"
            #print r

        return r


class Person2(object):
    def __init__(self, element_type=None, ide=None, username=None, name=None, email=None):
        self.element_type = element_type
        self.ide = ide
        self.username = username
        self.name = name
        self.email = email
        self.created = str(datetime.datetime.now())

    def print_person(self):
        print self.element_type
        print self.ide
        print self.name
        print self.email
        print self.created

    def create_person(self):
        graph_db.create({"element_type": self.element_type,
                         "ide": self.ide,
                         "username": self.username,
                         "name": self.name,
                         "email": self.email,
                         "crated": self.created})

    def get_person(self, name=None):
        n = name
        query = "match (n) where n.name='" + n + "'return n"
        result, metadata = cypher.execute(graph_db, query)
        r = result[0][0]["name"]
        print r


class WebDev(object):

    def get_node(self, name=None):
        self.wd = name
        try:

            query = "match (n) where n.name='" + self.wd + "' return n"
            print query
            result, metadata = cypher.execute(graph_db, query)
            r = result
            print r

        except:
            r ="error"
            #print r

        return r

    

class WebDesign(object):


    def get_node(self, name=None):
        self.wd = name
        try:

            query = "match (n) where n.name='" + self.wd + "' return n"
            print query
            result, metadata = cypher.execute(graph_db, query)
            r = result
            print r
        except:
            r ="error"
            #print r

        return r
   

class Internet(object):


    def get_node(self, name=None):
        self.internet = name
        try:

            query = "match (n) where n.name='" + self.internet + "' return n"
            print query
            result, metadata = cypher.execute(graph_db, query)
            r = result
            print r
        except:
            r ="error"
            #print r

        return r
    


class Education(object):
    
    def get_node(self, name=None):
        self.education = name
        try:

            query = "match (n) where n.name='" + self.internet + "' return n"
            print query
            result, metadata = cypher.execute(graph_db, query)
            r = result
            print r
        except:
            r ="error"
            #print r

        return r


class Graph_Individual(object):

    def get_node(self, id=None):
        self.id = id
        #self.status = ind_status
        try:
            query = "MATCH (n) WHERE n.id='" + self.id + "'return n"
            print query
            result, metadata = cypher.execute(graph_db, query)
            r = result
            print r
        except:
            r ="error"
            #print r

        return r


class Relations(object):
    def likes(self, n1, n2, rate):
        r = graph_db.create(rel(n1, "LIKES", n2, createn=str(datetime.datetime.now()), rate=rate))
        print "Relation LIKES created"

    def has(self, n1, n2):
        r = graph_db.create(rel(n1, "HAS", n2, createn=str(datetime.datetime.now())))
        print "Relation HAS created"

    def knows(self, n1, n2):
        r = graph_db.create(rel(n1, "KNOWS", n2, createn=str(datetime.datetime.now())))
        print "Relation KNOWS created"

    def parent(self, n1, n2):
        r = graph_db.create(rel(n1, "PARENT", n2, createn=str(datetime.datetime.now())))
        print "Relation PARENT created"








# person = g_db.create({"elemnt_type": "person",
#                       "email": "crhdragon@gmail.com",
#                       "name": "Jose",
#                       "created": str(datetime.datetime.now())})
#
# webDev = g_db.create({"elemnt_type": "web_development",
#                       "name": "web develoment",
#                       "created": str(datetime.datetime.now())})
#
# education = g_db.create({"elemnt_type": "education",
#                          "name": "education",
#                          "eduType": "Elementary",
#                          "created": str(datetime.datetime.now())})
#
# individual = g_db.create({"elemnt_type": "individual",
#                           "ide": "education",
#                           "chro": "[1,2,3,4,5,6,7,8,9]",
#                           "cross": "chrossover",
#                           "views": "32",
#                           "created": str(datetime.datetime.now())})


# class Character(object):
#     def __init__(self, name):
#         self.name = name
#         self.health = 100
#
#     def printName(self):
#         print self.name
#
#
# class NPC(Character):
#     pass
#
#
# class PC(Character):
#     def __init__(self, name):
#         super(PC, self).__init__(name)


# q1 = "match (n) where n.name='iliana'return n"
# q1 = "match (n) where n.name='Jose'return n"
# q2 = "match (n) where n.ide='education'return n"
# result, metadata = cypher.execute(g_db, q1)
# result2, metadata2 = cypher.execute(g_db, q2)
# result, metadata = cypher.execute(g_db, q1)
# n1 = node(result[0][0])
# n2 = node(result2[0][0])
# r = g_db.create(rel(n1, "LIKES", n2, createn=str(datetime.datetime.now())))
# result[0][0]["name"]
# n1 = node(result[0][0])
# n2 = result[0][1]
# r = g_db.create(rel(n1, "LIKES", n2, createn=str(datetime.datetime.now())

# p = Person()
# part='10204041785597745'
# print type(p.get_participation(part))
# par = p.get_participation(part)
# print type(par[0][0])

