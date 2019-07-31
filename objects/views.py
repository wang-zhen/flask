from __future__ import absolute_import, unicode_literals
#!/usr/bin/python
# -*- coding: UTF-8 -*-
from flask import request
from flask_restful import Resource, Api

class ObjectsList(Resource):
   def get(self):
     return 'this is data list'
   def post(self):
     data = request.get_json()
     return 'add new data: %s'%data  

class ObjectsDetail(Resource):
   def get(self,_id):
     return 'this data is %s'%_id
   def delete(self,_id):
     return 'delete data: %s'%_id
   def put(self, _id):
     data = request.get_json()
     return 'put data %s: %s'%(_id, data)
