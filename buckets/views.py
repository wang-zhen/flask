from __future__ import absolute_import, unicode_literals
#!/usr/bin/python
# -*- coding: UTF-8 -*-
from flask import request
from flask_restful import Resource, Api 

from common.fclog import fclog
from common.serializer import Serializer
from common.status import *

from users.models import *
from users.control import *
#from buckets.models import *
#from buckets.control import *

class BucketList(Resource):
   def get(self):
     return 'this is data list'
   def post(self):
     data = request.get_json()
     return 'add new data: %s'%data  

class BucketDetail(Resource):
   def get(self,_id):
     return 'this data is %s'%_id
   def delete(self,_id):
     return 'delete data: %s'%_id
   def put(self, _id):
     data = request.get_json()
     return 'put data %s: %s'%(_id, data)
