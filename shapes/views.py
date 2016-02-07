# Python
import urllib
import urlparse
import sys, traceback
import ast

import cgi, json
import datetime
import ast
import itertools
from py2neo import node
import datetime

from lib.store import redis
#import redis

# Django
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

# Project
from shapes import models
from shapes.models import Collection, User_Collection, Collection_Individual, FacebookSession
#from lib.evospace import Population, Individual
from lib.evospace_redis_neo4j import Population, Individual
from lib.colors import init_pop, evolve_Tournament
from lib.userGraph import Nodo, Person, WebDesign, Relations, Graph_Individual, WebDev, GraphCollection
from lib.user_activity import Activity_stream
from lib.scaleRanking import get_level
from lib.usr_last_date import usr_last_date



# Create your views here.
# def home(request):

# 	# form = SignUpForm(request.POST or None)

# 	# if form.is_valid():
# 	# 	save_it = form.save(commit=False)
# 	# 	save_it.save()
# 	m="Hola Sr. Christian, como esta!"

# 	return render(request, "test.html", {"mensaje":m})

EVOLUTION_INTERVAL = 8
REINSERT_THRESHOLD = 20
popName = 'pop'


@csrf_exempt
def evospace(request):
    if request.method == 'POST':
        population = Population(popName)
        #print 'Raw Data___: "%s"' % request.body
        #print type(request.body)
        json_data = json.loads(request.body)
        method = json_data["method"]
        params = json_data["params"]
        id = json_data["id"]



        if method == "initialize":
            result = population.initialize()
            data = json.dumps({"result": result, "error": None, "id": id})
            print data
            return HttpResponse(data, mimetype='application/javascript')
        elif method == "getSample":
            #Auto ReInsert
            if population.read_sample_queue_len() >= REINSERT_THRESHOLD:
                population.respawn(5)
            result = population.get_sample(params[0])
            if result:
                data = json.dumps({"result": result, "error": None, "id": id})
            else:
                data = json.dumps({"result": None, "error":
                    {"code": -32601, "message": "EvoSpace empty"}, "id": id})
            return HttpResponse(data, mimetype='application/json')
        elif method == "read_pop_keys":
            result = population.read_pop_keys()
            if result:
                data = json.dumps({"result": result, "error": None, "id": id})
            else:
                data = json.dumps({"result": None, "error":
                    {"code": -32601, "message": "EvoSpace empty"}, "id": id})
            return HttpResponse(data, mimetype='application/json')
        elif method == "read_sample_queue":
            result = population.read_sample_queue()
            if result:
                data = json.dumps({"result": result, "error": None, "id": id})
            else:
                data = json.dumps({"result": None, "error":
                    {"code": -32601, "message": "EvoSpace empty"}, "id": id})
            return HttpResponse(data, mimetype='application/json')

        elif method == "putSample":
            #Cada EVOLUTION_INTERVAL evoluciona
            print "##################"
            if not population.get_returned_counter() % EVOLUTION_INTERVAL:
                try:
                    print "Evolucionando"
                    evolve_Tournament()
                except Exception as e:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    print e.message
                    traceback.print_tb(exc_traceback, limit=20, file=sys.stdout)

                pass
            population.put_sample(params[0])

            #Aqui se va armar la machaca del individuo
            if request.user.is_authenticated():
                usr = request.user.username
                first_name = request.user.first_name
                last_name = request.user.last_name
                name = first_name + " " + last_name
                nodo = Nodo()
                person = Person()
                person_result = person.get_person(name)
                activity_stream = Activity_stream()

                #print u
                print "=========Parametros==========="
                print params[0]
                usrLastDate=str(usr_last_date(params[0]['sample'][0]['fitness']))
                print usrLastDate
                usr_date_key = usr + ":" + usrLastDate
                print usr_date_key
                print params[0]['sample'][0]['fitness'][usr_date_key]
                rate = params[0]['sample'][0]['fitness'][usr_date_key]

                if params[0]["individuals_with_like"]:
                    for item in params[0]["individuals_with_like"]:
                        id = item
                        print id
                        individual_node = Graph_Individual()

                        print "prueba ", params[0]["individuals_with_like"]

                        # Verificar si el nodo individual existe con status last
                        individual_node_exist = individual_node.get_node(id)

                        if person_result:
                            nodo1 = node(person_result[0][0])

                        if individual_node_exist: # si la lista esta vacia quiere decir que no existe
                            nodo2 = node(individual_node_exist[0][0])

                        relation = Relations()
                        relation.likes(nodo1,nodo2,rate)

                        #request.user.username in k

                        #Agreagando Activity stream para el verbo like
                        activity_stream.activity("person", "like", "evaluate", usr)

                print "=========Parametros==========="
            else:
                print "Usuario anonimo"


            return HttpResponse(json.dumps("Success"), mimetype='application/json')
        elif method == "init_pop":
            data = init_pop(populationSize=params[0])
            return HttpResponse(json.dumps("Success"), mimetype='application/javascript')
        elif method == "respawn":
            data = population.respawn(n=params[0])
            return HttpResponse(json.dumps("Success"), mimetype='application/javascript')
        elif method == "put_individual":
            print  "params", params[0]
            population.put_individual(**params[0])
            data = json.dumps({"result": None, "error": None, "id": id})
            return HttpResponse(data, mimetype='application/json')


    else:
        return HttpResponse("ajax & post please", mimetype='text')

#@ensure_csrf_cookie            
def home(request):
    #print request
    if request.user.is_authenticated():
        #REFACTOR GET_FRIENDS
        print request.user.username
        face = FacebookSession.objects.get(uid=request.user.username)
        friends = None
        
        friends = face.query("me", connection_type="friends", fields='name,installed')
       
        print friends
       
        
        #print "Amigos"
        #print friends



            #print "Hola, mundo!!"


        #Condultar nodo usuario
        u = request.user.username
        e = request.user.email
        fn = request.user.first_name
        ln = request.user.last_name
        na = fn + " " + ln
        n = Nodo()
        p = Person()
        print na
        person_result = p.get_person(na)
        print "if resultado igual a error"
        print person_result
        print "2323232323232323"
        print u

        # if not r:
        #     print "creando nodo"
        #     n.create_nodo(element_type="person", id=u, email=e, name=na)
        #     print "creo nodo"
        #     print n

        print "+++++++++++++++++"
        #print na, r[0][0]["name"]
        #n = Person()
        # participation = p.get_participation(u)
        # participation = participation[0][0]
        # print participation
        # ranking=get_level(participation)
        # print ranking



        if request.method == 'POST':
            if request.POST.has_key("webDesing"):
                web_design = request.POST["webDesing"]
                if web_design == "on":
                    nodo_web_design = Nodo()
                    nodo_web_design_exist = WebDesign() # creando objeto WebDesig
                    web_design_result = nodo_web_design_exist.get_node("web design") # Verificar si hay resultado

                    print "estoy en el if"
                    if not web_design_result: # si lista esta vacia quiere decir que el nodo web design no exist hay que crearlo
                        nodo_web_design.create_nodo(element_type="web_des", name="web design")
                        print "Nodo Web design creado"

                    #nodo_web_design_exist = WebDesign() # creando objeto WebDesig
                    #result = nodo_web_design_exist.get_node("web design") # Verificar si hay resultado

                    nodo1 = node(person_result[0][0])
                    nodo2 = node(web_design_result[0][0])
                    print "Making a relition LIKE between nodes"
                    relation = Relations()
                    relation.likes(nodo1,nodo2)
                    print "You like web design"

            if request.POST.has_key("webDevelopment"):
                web_dev = request.POST["webDevelopment"]
                if web_dev == "on":
                    nodo_web_dev = Nodo()
                    nodo_web_dev_exist = WebDev()
                    web_develoment_result = nodo_web_dev_exist.get_node("web develoment")

                    if not web_develoment_result:
                        nodo_web_dev.create_node(element_type="web_dev", name="web design")

                    web_develoment_result = nodo_web_dev_exist.get_node("web develoment")

                    nodo1 = node(person_result[0][0])
                    nodo2 = node(web_develoment_result[0][0])
                    relation = Relations()
                    relation.likes(nodo1,nodo2)
                    print "You like web develoment"

            if request.POST.has_key("internet"):
                internet = request.POST["internet"]

                if internet == "on":
                    nodo_internet = Nodo()
                    nodo_internet_exist = WebDev
                    web_develoment_result = nodo_web_dev_exist.get_node("web develoment")

                    if not web_develoment_result:
                        nodo_web_dev.create_node(element_type="web_dev", name="web design")

                    web_develoment_result = nodo_web_dev_exist.get_node("web develoment")

                    nodo1 = node(person_result[0][0])
                    nodo2 = node(web_develoment_result[0][0])
                    relation = Relations()
                    relation.likes(nodo1,nodo2)

                    print "You like internet"
                    
            #internet = request.POST["internet"]
            #elementary = request.POST["elementary"]
            #phd = request.POST['PhD']

        if friends:
        # Mejor con FQL
            app_friends = [f for f in friends['data'] if f.has_key('installed')]

            if app_friends:
                for i in range(len(app_friends)):
                    person_relation_knows = p.get_relation_knows(na, app_friends[i]["name"])
                    if person_relation_knows:
                        print "Existe relacion entre ambos"
                        pass
                    else:
                        print "crea relacion knows"
                        friend_result = p.get_person(app_friends[i]["name"])
                        if friend_result:
                            nodo_user = node(person_result[0][0])
                            nodo_friend = node(friend_result[0][0])
                            relation_knows = Relations()
                            relation_knows.knows(nodo_user, nodo_friend)

        else:
            app_friends = None
    else:
        app_friends = None



    return render_to_response('django_index.html', {'static_server': 'https://s3.amazonaws.com/evospace/prototype/',
                                                    'api_server': 'http://app.evospace.org', 'friends': app_friends,
                                                    },
                              context_instance=RequestContext(request))


def individual_view(request, individual_id):
    key = "pop:individual:%s" % (individual_id)
    individual = Individual(id=key).get(as_dict=True)
    mama = None
    papa = None
    if "mama" in individual:
        mama = Individual(id=individual["mama"]).get(as_dict=True)

    if "papa" in individual:
        papa = Individual(id=individual["papa"]).get(as_dict=True)

    individual_json = json.dumps(individual)

    return render_to_response('individual.html', {'static_server': 'http://evospace.org/prototype/',
                                                  'api_server': 'http://app.evospace.org', 'individual': individual,
                                                  'individual_json': individual_json, 'mama': mama, 'papa': papa},
                              context_instance=RequestContext(request))


def facebook_get_login(request):
    state = request.session.session_key
    scope = "user_friends, email"
    url = """https://www.facebook.com/dialog/oauth?client_id=%s&redirect_uri=%s&state=%s&scope=%s""" % \
          (settings.FACEBOOK_APP_ID, settings.FACEBOOK_REDIRECT_URL,
           state,
           scope,
          )

    return HttpResponseRedirect(url)


def facebook_login(request):
    if 'error' in request.GET:
        return HttpResponseRedirect('/')

    code = request.GET['code']
    UID = request.GET['state']

    args = {"client_id": settings.FACEBOOK_APP_ID,
            "redirect_uri": settings.FACEBOOK_REDIRECT_URL,
            "client_secret": settings.FACEBOOK_APP_SECRET,
            "code": code}

    response = urllib.urlopen("https://graph.facebook.com/oauth/access_token?" + urllib.urlencode(args))
    response = urlparse.parse_qs(response.read())
    access_token = response["access_token"][-1]
    profile = json.load(urllib.urlopen(
        "https://graph.facebook.com/me?" +
        urllib.urlencode(dict(access_token=access_token))))
    expires = response['expires'][0]

    facebook_session = models.FacebookSession.objects.get_or_create(
        access_token=access_token)[0]

    facebook_session.expires = expires
    facebook_session.save()
    user = authenticate(token=access_token)
    
    if user:
        print user
        u = str(user)
        #r = redis.StrictRedis(host='localhost', port=6379, db=0)
        r = redis
        login_time = datetime.datetime.now()
        r.set("time_login:"+u, login_time)

        if user.is_active:
            
            login(request, user)
            
            return HttpResponseRedirect('/')
        else:
            error = 'AUTH_DISABLED'

    if 'error_reason' in request.GET:
        error = 'AUTH_DENIED'
        ### TO DO Log Error
    return HttpResponseRedirect('/')


@login_required
def logout_view(request):
    #r = redis.StrictRedis(host='localhost', port=6379, db=0)
    r = redis
    # Log a user out using Django's logout function and redirect them
    # back to the homepage.
    u = request.user.username
    #print u
    logout_time = datetime.datetime.now()
    r.set("time_logout:"+u, logout_time)
    #print logout_time
    logout(request)
    # logout time
   

    return HttpResponseRedirect('/')


@csrf_exempt
def add_collection(request, username):
    global message
    errors = []
    if request.method == 'POST':
        #print "Estas en add collections"
        #users=User.objects.all();
        #u1=User.objects.get(username=username)
        #u=users[0]
        #print request.POST
        json_data = json.loads(request.body)

        n = json_data["name"]
        d = json_data["description"]
        v = json_data["option"]

        print n

        c = Collection(name=n,
                       description=d,
                       creation_date=datetime.datetime.now(),
                       visibility=v)
        c.save()


        #Agregar nodo Coleccion a la red de grafos
        nodo_collection = Nodo()
        nodo_collection.create_nodo(element_type="Collection", name=n, description=d, visibility=v)


        print "Salvaste colleccion"
        #c_id=Collection.objects.latest('id')
        #c_id=c_id.id
        #u_id=u1.id

        #if User.objects.get(id=u_id) and Collection.objects.get(id=c_id):
        #u=User.objects.get(id=u_id)
        #c=Collection.objects.get(id=c_id)

        u=request.user.last_name
        #print u

        uc = User_Collection(user=request.user,
                             collection=c,
                             role="O",
                             status="PU")
        uc.save()

        #Activity stream
        activity_stream = Activity_stream()
        usr = request.user.username
        activity_stream.activity("person", "save", "new collection", usr)


        #Relacionar coleccion con el usuario
        firstName = request.user.first_name
        lastName = request.user.last_name
        name = firstName +" "+lastName
        person = Person()
        person_result = person.get_person(name)
        collection = GraphCollection()
        collection_result = collection.get_collection(n)
        nodo1 = node(person_result[0][0])
        nodo2 = node(collection_result[0][0])
        relation = Relations()
        relation.has(nodo1, nodo2)


        message = "You are now linked to this collection!"
        #else:
        #    message= "Sorry there is no collection or user"
        #add_user_collection(id,c_id)
        #col= Collection.objects.all()

        data = ({'name': n, 'description': d, 'visibility': v, 'message': message})
        datar = json.dumps(data)
        print datar

    return HttpResponse(datar, mimetype='application/json')


def get_user_collections(request, username):
    if User.objects.get(username=username):
        u1 = User.objects.get(username=username)
        u_id = u1.id
        uc = Collection.objects.all().filter(user_collection__user_id__exact=u_id)
        jd = {'collections': [{'id': col.id, 'name': col.name} for col in uc]}
        j = json.dumps(jd)

        #Agreagar activity stream
        activity_stream = Activity_stream()
        usr = request.user.username
        activity_stream.activity("person", "open", "open a collection", usr)

    return HttpResponse(j, mimetype='application/json')


def get_collection(request, username, collection=None):
    if request.user.is_authenticated():

        #REFACTOR GET_FRIENDS
        face = FacebookSession.objects.get(uid=request.user.username)
        friends = face.query("me", connection_type="friends", fields='name,installed')
        # Mejor con FQL
        app_friends = [f for f in friends['data'] if f.has_key('installed')]

        face_owner = FacebookSession.objects.get(uid=username)

        url = 'https://graph.facebook.com/%s?fields=name' % username
        owner = face_owner.query("me", fields='name')
        #owner = json.load(urllib.urlopen(url))
        print username, owner

        #r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
        r = redis
        if collection:
            inds_psql = Collection.objects.get(user_collection__user__username=username,
                                               id=collection).individuals.all()
            collection_obj = Collection.objects.get(id=collection)

        else:
            collections = Collection.objects.filter(user_collection__user__username=username, visibility='PU')
            lists_of_inds = [ind for ind in [col.individuals.all() for col in collections]]
            inds_psql = list(itertools.chain.from_iterable(lists_of_inds))

            collection_obj = None

        inds = [{"id": r["id"], "chromosome": r["chromosome"]} for r in
                [ast.literal_eval(i) for i in
                 [r.get(ind_.individual_id) for ind_ in inds_psql] if i
                ]
        ]
        print "Individuals"
        print inds

        #Agreagar activity stream
        activity_stream = Activity_stream()
        usr = request.user.username
        activity_stream.activity("person", "open", "open a collection", usr)

        #inds = [ (i["id"], i["chromosome"]) for i in [ r.get(ind_.individual_id) for ind_ in inds_psql ] if i ]
        j = json.dumps(inds)
        return render_to_response('collection.html', {'static_server': 'http://evospace.org/prototype/',
                                                      'api_server': 'http://app.evospace.org',
                                                      'individualsjs': j, 'individuals': inds,
                                                      'collection_obj': collection_obj, "friends": app_friends,
                                                      'owner': owner
        },
                                  context_instance=RequestContext(request))
    else:
        return HttpResponse('noup')


@csrf_exempt
def add_ind_to_col(request, username):
    global message
    if request.method == 'POST':

        if request.user.is_authenticated():

            u1 = User.objects.get(username=username)
            u = User.objects.get(id=u1.id)

            json_data = json.loads(request.body)

            col = json_data['userCollection']
            ind = json_data['id']

            c = Collection.objects.get(id=col)
            collection_name = c.name
            #print collection_name

            itc = Collection_Individual(collection=c,
                                        individual_id=ind,
                                        added_from=c,
                                        from_user=u,
                                        date_added=datetime.datetime.now())

            itc.save()

            #Agregar activity stream
            activity_stream = Activity_stream()
            usr = request.user.username
            activity_stream.activity("person", "save", "individual to collection", usr)

            #Agregar relacion entre individuo y coleccion en la red de grafos
            collection = GraphCollection()
            collection_result = collection.get_collection(collection_name)
            individual = Graph_Individual()
            individual_result = individual.get_node(ind)
            nodo1 = node(collection_result[0][0])
            nodo2 = node(individual_result[0][0])
            relation = Relations()
            relation.has(nodo1, nodo2)





            message = "Individual is now added to this collection!"
        else:
            message = "No username in evoart!"

        data = ({'collection': col, 'individual': ind, 'message': message})
        datar = json.dumps(data)

    return HttpResponse(datar, mimetype='application/json')


def dashboard(request):
    return render_to_response('dashboard.html', {'static_server': 'http://evospace.org/prototype/',
                                                 'api_server': 'http://app.evospace.org'},
                              context_instance=RequestContext(request))


def home2(request):
    if request.method == 'POST':
        phd = request.POST['PhD']
        if phd:
            print "You have a PhD degree"
        print phd
        print "Hola, mundo!!"
    return render_to_response('base.html', context_instance=RequestContext(request))

def user_experience(request):
    #r = redis.StrictRedis(host='localhost', port=6379, db=0)

    experience = 0

    if request.user.is_authenticated():
        user_activity = r.lrange("user:"+request.user.username, 0, -1)

        #json_string = json.dumps(user_activity[0])
        #j=json_string.replace("'", "\"")
        #s=l[0].replace("'", "\"")
        #d = ast.literal_eval(s)


        for activity in user_activity:
            s = activity.replace("'", "\"")
            d = ast.literal_eval(s)
            fk = d.keys()

            if d[fk[0]]['verb'] == 'like':
                experience = experience + 3

            if d[fk[0]]['verb'] == 'join':
                experience = experience + 5

            if d[fk[0]]['verb'] == 'save':
                experience = experience + 8

            if d[fk[0]]['verb'] == 'open':
                experience = experience + 2

            #print d[fk[0]]['verb']

def get_user_level(request, username):
    print "^^^^^^^^^^^^^^"
    if username:

        p = Person()
        score = p.get_participation(username)
        score = score[0][0]

        print score

        if score == 0 or username=='anonymous':
            print "Hola, mundo!!"
            jd = {"user_level": {"score":0, "level":0}}
            j = json.dumps(jd)
            print j

        else:
            ranking=get_level(score)
            print score
            print ranking
        

            jd = {"user_level": {"score":score, "level":ranking}}


            j = json.dumps(jd)

        
        
    return HttpResponse(j, content_type='application/json')


def get_liders(request):
    print "T_T"
    
    jd = {"leaders":[]}
    p = Person()
    lider_board = p.get_lider_board()
    #ldier_board = score[0][0]

    print lider_board
   
    if lider_board:
        #   c = 0
        for lider in lider_board:
            
            # if c < len(lider_board):
            #     c = c + 1
            #     print c

            user = lider[0]
            score = lider[1]
            ranking=get_level(score)
            

            de = {"user":user, "score":score, "ranking":ranking}
            print de
            jd["leaders"].append(de)
            

        
        j = json.dumps(jd) 
        print "101010101001010101010101001"
        print lider_board
        print jd
        print j   
    else:
        print "No lider board"
        
        
    return HttpResponse(j, content_type='application/json')






