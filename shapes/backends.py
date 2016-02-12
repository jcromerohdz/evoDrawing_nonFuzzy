# -*- coding: utf-8 -*-
__author__ = 'mariosky'
#Facebook backend basado en: http://djangosnippets.org/snippets/2065/
# 16 June 2010 Added missing imports. Cleaned up the template.
#Shouts out to @obeattie and @whalesalad
#Author: barnardo
#Posted: June 15, 2010
import datetime
from django.contrib.auth import models as auth_models
from shapes import models
from shapes.models import Collection, User_Collection
from lib.userGraph import Nodo, Person
from lib.user_activity import Activity_stream

class FacebookBackend:

    def authenticate(self, token=None):
        print token
        
        facebook_session = models.FacebookSession.objects.get(
            access_token=token,
        )

        profile = facebook_session.query('me')
        print "^^^^^^^^^PROFILE^^^^^^^^^^^^"

        try:
            user = auth_models.User.objects.get(username=profile['id'])
        except auth_models.User.DoesNotExist, e:
            user = auth_models.User(username=profile['id'])


        user.set_unusable_password()


        if 'username' in profile:
            user.email = profile['username']
        else:
            user.email = profile['id']

        user.first_name = profile['name']
        user.last_name = profile['name']
        user.save()

        #Agregando Activity_stream
        #activity_stream = Activity_stream()

        #Agregando nodo usuario, creado por Christian "Nuevo"
        usr = profile['id']
        email = profile['name']
        #first_name = profile['first_name']
        #last_name = profile['last_name']
        #full_name = first_name + " " + last_name
        full_name = profile['name']

        print '****************'
        nodo = Nodo()
        person = Person()
        person_result = person.get_person(full_name)

       

        #print usr, email, full_name
        print "if person_result es vacio, entonce hay que crearlo"
        print person_result

        if not person_result:
            print "creando nodo"
            nodo.create_nodo(element_type="person", id=usr, email=email, name=full_name)
            print "creo nodo"

        #Agregando Activity_stream
        activity_stream = Activity_stream()
        activity_stream.activity("person", "join", "log in", usr)


        try:
            models.FacebookSession.objects.get(uid=profile['id']).delete()
        except models.FacebookSession.DoesNotExist, e:
            pass

        facebook_session.uid = profile['id']
        facebook_session.user = user
        facebook_session.save()


        if User_Collection.objects.filter(user = user).exists():
            pass
        else:
            c = Collection(name="Public", description="Public Collection", creation_date=datetime.datetime.now(), visibility="PU" )
            c.save()
            uc= User_Collection(user=user, collection=c, role="O", status="PU" )
            uc.save()

        return user

    def get_user(self, user_id):

        try:
            return auth_models.User.objects.get(pk=user_id)
        except auth_models.User.DoesNotExist:
            return None