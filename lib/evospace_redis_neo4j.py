__author__ = 'mario'
__author__ = 'chris'

LOGGING = False
LOG_INTERVAL = 10

import ConfigParser
import json
from py2neo import rel, node
from store import redis

from userGraph import Nodo, Graph_Individual, Relations

# Por que 5 iteraciones
# co = ConfigParser.ConfigParser()
# co.read(["config/evospace.cfg", "../config/evospace.cfg"])

# HOST = co.get('redis', 'HOST')
# PORT = co.getint('redis', 'PORT')
# DB = co.getint('redis', 'DB')

# r = redis.Redis(host=HOST, port=PORT, db=DB)
r = redis

class Individual:
    def __init__(self, **kwargs):
        ## Se puede inicializar desde un diccionario
        self.id = kwargs['id']
        self.fitness = kwargs.get('fitness', {})
        self.chromosome = kwargs.get('chromosome', [])
        self.__dict__.update(kwargs)

    def put(self, population):
        pipe = r.pipeline()
        if pipe.sadd(population, self.id):
            pipe.set(self.id, self.__dict__)
            pipe.execute()
            return True
        else:
            return False

    def get(self, as_dict=False):
    #Se evalua el diccionario almacenado en Redis
    #Esto crea el tipo de dato correspondiente en python
    #normalmente fitness es un diccionario y chromosome una lista
        if r.get(self.id):
            dict = eval(r.get(self.id))
            self.__dict__.update(dict)
        else:
            raise LookupError("Key Not Found")

        if as_dict:
            return self.__dict__
        else:
            return self

    def __repr__(self):
        return self.id + ":" + str(self.fitness) + ":" + str(self.chromosome)

    def as_dict(self):
        return self.__dict__


class Population:
    def __init__(self, name="pop"):
        self.name = name
        self.sample_counter = self.name + ':sample_count'
        self.individual_counter = self.name + ':individual_count'
        self.sample_queue = self.name + ":sample_queue"
        self.returned_counter = self.name + ":returned_count"
        self.log_queue = self.name + ":log_queue"
        #Esta es una propiedad del EvoSpaceServer NO de la poblacion
        self.is_active = False

    ##NOOO Aqui
    def deactivate(self):
        self.is_active = False

    def get_returned_counter(self):
        return int(r.get(self.returned_counter))

    def individual_next_key(self):
        key = r.incr(self.individual_counter)
        return self.name + ":individual:%s" % key

    def size(self):
        return r.scard(self.name)

    def initialize(self):
        r.flushall()
        r.setnx(self.sample_counter, 0)
        r.setnx(self.individual_counter, 0)
        r.setnx(self.returned_counter, 0)

        ##NOOO Aqui
        self.is_active = True

    def get_sample(self, size):
        sample_id = r.incr(self.sample_counter)

        #Get keys
        sample = [r.spop(self.name) for i in range(size)]
        #If there is a None
        if None in sample:
            sample = [s for s in sample if s]
            if not sample:
                return None
        r.sadd(self.name + ":sample:%s" % sample_id, *sample)
        r.rpush(self.sample_queue, self.name + ":sample:%s" % sample_id)
        try:
            result = {'sample_id': self.name + ":sample:%s" % sample_id,
                      'sample': [Individual(id=key).get(as_dict=True) for key in sample]}
        except:
            return None
        return result

    def read_sample_queue(self):
        result = r.lrange(self.sample_queue, 0, -1)
        return result

    def read_sample_queue_len(self):
        return r.llen(self.sample_queue)

    #####
    ##### Read Sample es ReadALL Pop
    #####
    #    def read_sample(self, size):
    #        sample_id = r.incr(self.sample_counter)
    #        sample = [r.spop(self.name) for i in range(size)]
    #        result =  {'sample_id': self.name+":sample:%s" % sample_id ,
    #                   'sample':   [Individual(key).get(as_dict=True) for key in sample]}
    #        return json.dumps(result)

    def read_pop_keys(self):
        sample = r.smembers(self.name)
        sample = list(sample)
        result = {'sample': sample}
        return result

    def read_sample(self):
        sample = r.smembers(self.name)
        result = {'sample': [Individual(id=key).get(as_dict=True) for key in sample]}
        return result

    def put_individual(self, **kwargs):

        #Esto debe hacerse fueran, recibe un diccionario y punto.
        #if isinstance(from_dict,str):
        #    from_dict = json.loads(from_dict)

        if kwargs['id'] is None:
            kwargs['id'] = self.name + ":individual:%s" % r.incr(self.individual_counter)
        ind = Individual(**kwargs)
        ind.put(self.name)

    def put_sample(self, sample, **kwargs):
        print "77777777777777"
        print type(sample)
        if not isinstance(sample, dict):
            sample = json.loads(sample)

        #if r.exists(sample['sample_id']):
        #    if LOGGING:

        r.incr(self.returned_counter)

        #        if count % LOG_INTERVAL == 0 :
        #            r.sunionstore("log:"+str(count),"pop")

        print "hola"
        for member in sample['sample']:
            print "for member"
            if member['id'] is None:
                print "*********MEMBER**********"
                member['id'] = self.name + ":individual:%s" % r.incr(self.individual_counter)

                new_individual_node = Nodo()
                new_individual_node.create_nodo(element_type="individual",
                                                id=member["id"],
                                                chromosome=member["chromosome"],
                                                views=member["views"])

                print "*********MEMBER**********"
                print member

                # Verificar si el nodo individual existe
                id = member['id']
                individual_node_child = Graph_Individual()
                individual_node_child_result = individual_node_child.get_node(id)

                if individual_node_child_result:
                    nodo1 = node(individual_node_child_result[0][0])


                    if member['papa']:
                        print "====PAPA==="
                        id_dad = member['papa']
                        individual_node_dad = Graph_Individual()
                        individual_node_dad_result = individual_node_dad.get_node(id_dad)
                        nodo2 = node(individual_node_dad_result[0][0])

                        relation = Relations()
                        relation.parent(nodo1, nodo2)

                    if member['mama']:
                        print "++++MAMA++++"
                        id_mom = member['mama']
                        individual_node_mom = Graph_Individual()
                        individual_node_mom_result = individual_node_mom.get_node(id_mom)
                        nodo2 = node(individual_node_mom_result[0][0])

                        relation = Relations()
                        relation.parent(nodo1, nodo2)
            else:
                id = member['id']
                views = member['views']
                individual_node = Graph_Individual()
                individual_node_result = individual_node.get_node(id)
                individual_node_result[0][0]["views"] = views
                print "Node views updated"


            self.put_individual(**member)
            # self.put_individual( member['id'], fitness = member['fitness'] , chromosome  = member['chromosome'])

        r.delete(sample['sample_id'])
        r.lrem(self.sample_queue, sample['sample_id'])


    def respawn_sample(self, sample):
        if r.exists(sample):
            members = r.smembers(sample)
            r.sadd(self.name, *members)
            r.delete(sample)
            r.lrem(self.sample_queue, sample, 1)


    def respawn_ratio(self, ratio=.2):
        until_sample = int(r.llen(self.sample_queue) * ratio)
        for i in range(until_sample):
            self.respawn_sample(r.lpop(self.sample_queue))


    def respawn(self, n=1):
        current_size = r.llen(self.sample_queue)
        if n > current_size:
            for i in range(current_size):
                self.respawn_sample(r.lpop(self.sample_queue))
        else:
            for i in range(n):
                self.respawn_sample(r.lpop(self.sample_queue))


if __name__ == "__main__":
    pass


