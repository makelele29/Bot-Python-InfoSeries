# -*- coding: utf-8 -*-
__author__ = 'Javier Castillo'
from pymongo import MongoClient
import themoviedb
import json
import sensamoviedb

client = MongoClient()
db = client.info
coll = db.series

def insertar(id,serie):
    num=coll.find({'id':id.chat_id}).count()
    moviedb=themoviedb.seriesdb(serie)
    if num==0:
        coll.insert({'id':id.chat_id,'message':id.message_id,"image":moviedb.image(),"overview":moviedb.overview(),"status":moviedb.status(),'duracion':moviedb.duracion(),"temporadas":moviedb.temporadas(),"enlace":moviedb.enlace()})
    else:
        coll.update_one({'id':id.chat_id},{'$set':{'message':id.message_id,"image":moviedb.image(),"overview":moviedb.overview(),"status":moviedb.status(),'duracion':moviedb.duracion(),"temporadas":moviedb.temporadas(),"enlace":moviedb.enlace()}})
def show(id):
    return coll.find_one({'id':id},{'_id':0,})
def update(id,message):
    coll.update_one({'id':id},{'$set':{'message':message}})
