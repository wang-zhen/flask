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

print 'eeiiie'
class UsersList(Resource):
    def get(self):
        users = User.query.all()
        serializer = Serializer(users, many=True)
        response = serializer.data
        fclog.info(response)
        return (response)

    def post(self):
        """
        {"username":"admin"}
        """
     
        data = request.get_json()
        fclog.info(data)
        (state, ret) = create_user(data)
        message = {"detail": ret}
        if(state != True):
            return (message, HTTP_400_BAD_REQUEST)
        return (message, HTTP_201_CREATED)
        
class UsersDetail(Resource):
    def get_object(self, pk):
        return User.query.filter_by(id=pk).first()
            
    def get(self, pk):
        user = self.get_object(pk)
        if user == None:
            message = {"detail": "NOT FOUND"}
            fclog.warning(message)
            return (message, HTTP_404_NOT_FOUND)

        serializer = Serializer(user, many=True)
        response = serializer.data
        return (response)

    def put(self, pk):
        """
        {
            "cmd":"suspend" or "cmd":"enable" 
        }
        {
            "cmd":"userquota"
            "arg":{
                "enable":True,
                "maxobjects":1024,
                "maxsize":1024
            }
        }
        {
            "cmd":"bucketquota"
            "arg":{
                "enable":True,
                "maxobjects":1024,
                "maxsize":1024
            }
        }
        """
 
        args = request.get_json()
        if (False == args.has_key('cmd')):
            message = {'detail': 'input error'}
            return (message, HTTP_400_BAD_REQUEST)

        logger.debug('UsersDetail: data=%s pk=%s.' % (args, pk))

        if ('suspend' == args['cmd']):
            suspend_user(True)
        elif ('enable' == args['cmd']):
            suspend_user(False)
        elif ('userquota' == args['cmd']):
            suspend_user(False)
        elif ('bucketquota' == args['cmd']):
            suspend_user(False)
        elif ('enable' == args['cmd']):
            suspend_user(False)
        else:
            pass

        user = self.get_object(pk)
        if user == None:
            message = {"detail": "NOT FOUND"}
            fclog.warning(message)
            return (message, HTTP_404_NOT_FOUND)

        serializer = Serializer(user, many=True)
        response = serializer.data
        fclog.info(response)
        return (response)

    def delete(self, pk):
        (state, ret) = remove_user(pk)
        message = {"detail": ret}
        if(state != True):
            return (message, HTTP_400_BAD_REQUEST)

        return (message, HTTP_204_NO_CONTENT)

class UserKeysList(Resource):
    def get(self):
        userkeys = UserKey.query.all()
        serializer = Serializer(userkeys, many=True)
        response = serializer.data
        fclog.info(response)
        return (response)

    def post(self):
        """
        {
            "user_id":1
        }
        """
     
        data = request.get_json()
        fclog.info(data)
        (state, ret) = create_s3key(data)
        message = {"detail": ret}
        if(state != True):
            return (message, HTTP_400_BAD_REQUEST)
        return (message, HTTP_201_CREATED)
        
class UserKeysDetail(Resource):
    def get_object(self, pk):
        return UserKey.query.filter_by(id=pk).first()
            
    def get(self, pk):
        userkey = self.get_object(pk)
        if userkey == None:
            message = {"detail": "NOT FOUND"}
            fclog.warning(message)
            return (message, HTTP_404_NOT_FOUND)

        serializer = Serializer(userkey, many=True)
        response = serializer.data
        return (response)

    def put(self, pk):
        pass

    def delete(self, pk):
        (state, ret) = remove_s3key(pk)
        message = {"detail": ret}
        if(state != True):
            return (message, HTTP_400_BAD_REQUEST)

        return (message, HTTP_204_NO_CONTENT)

class SubUsersList(Resource):
    def get(self):
        subusers = SubUser.query.all()
        serializer = Serializer(subusers, many=True)
        response = serializer.data
        fclog.info(response)
        return (response)

    def post(self):
        """
        {
            "user_id":1,
            "username":"admin"

        }
        """
     
        data = request.get_json()
        (state, ret) = create_subuser(data)
        message = {"detail": ret}
        if(state != True):
            return (message, HTTP_400_BAD_REQUEST)
        return (message, HTTP_201_CREATED)
        
class SubUsersDetail(Resource):
    def get_object(self, pk):
        return SubUser.query.filter_by(id=pk).first()
            
    def get(self, pk):
        subuser = self.get_object(pk)
        if subuser == None:
            message = {"detail": "NOT FOUND"}
            fclog.warning(message)
            return (message, HTTP_404_NOT_FOUND)

        serializer = Serializer(subuser, many=True)
        response = serializer.data
        return (response)

    def put(self, pk):
        """
        {
            "subcmd":"subuser",
            "arg":{
                "subusername":"subuser"
            }
        }
        """
        #user = self.get_object(pk)
        pass

    def delete(self, pk):
        (state, ret) = remove_subuser(pk)
        message = {"detail": ret}
        if(state != True):
            return (message, HTTP_400_BAD_REQUEST)

        return (message, HTTP_204_NO_CONTENT)
