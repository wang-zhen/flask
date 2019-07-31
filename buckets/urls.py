#coding=utf-8
#!/usr/bin/python
# -*- coding: UTF-8 -*-
from buckets import buckets_page  
from flask_restful import Resource, Api
from views import BucketList, BucketDetail

api = Api(buckets_page)

api.add_resource(BucketList, '/bucket')
api.add_resource(BucketDetail, '/bucket/<_id>')
