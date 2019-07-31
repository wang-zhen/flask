#!/usr/bin/python
# -*- coding: UTF-8 -*-
from objects import objects_page  
from flask_restful import Resource, Api
from views import ObjectsList, ObjectsDetail 

api = Api(objects_page)

api.add_resource(ObjectsList, '/objects')
api.add_resource(ObjectsDetail, '/objects/<_id>')
