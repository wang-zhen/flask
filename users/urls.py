from __future__ import absolute_import, unicode_literals
#!/usr/bin/python
# -*- coding: UTF-8 -*-
from users import users_page  
from flask_restful import Resource, Api
from users.views import * 

api = Api(users_page)

api.add_resource(UsersList, '/users')
api.add_resource(UsersDetail, '/users/<int:pk>')
api.add_resource(UserKeysList, '/userkeys')
api.add_resource(UserKeysDetail, '/userkeys/<int:pk>')
api.add_resource(SubUsersList, '/subusers')
api.add_resource(SubUsersDetail, '/subusers/<int:pk>')
