from __future__ import absolute_import, unicode_literals
#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
from users.models import *
from agent.common import *
from agent.cephrgw_users import *

from common.fclog import *
from common.serializer import Serializer
from common.db import db

def create_user(arg):
    """
    {
        "username":"admin"
    }
    """

    uname = arg['username']

    ch_user = User.query.filter_by(username=uname).first()
    if ch_user != None:
        warning = 'the user:%s already  exists' % uname
        fclog.warning(warning)
        return (False, warning) 
    
    ret_create = agent_cephrgw_create_user.apply_async(args=[arg])
    (stat, res) = xn_get_task_result(ret_create, 60)
    if stat:
        fclog.error('create user:%s failed' % uname)
        return (False, res)

    fclog.debug(res)
    res = json.loads(res)

    user = User(username=uname)
    db.session.add(user)
    db.session.commit()    

    userkey = UserKey(akey=res['keys'][0]['access_key'], skey=res['keys'][0]['secret_key'])
    userkey.user_id = User.query.filter_by(username=uname).first().id
    db.session.add(userkey)
    db.session.commit()    

    fclog.info(arg)
    fclog.info('create user:%s successfully' % (arg['username']))
    return (True, res)

def remove_user(userid):
    ch_user = User.query.filter_by(id=userid).first()
    if ch_user == None:
        warning = 'the userid:%d do not exists' % userid
        fclog.warning(warning)
        return (False, warning) 

    arg = {}
    arg['username'] = ch_user.username

    ret_remove = agent_cephrgw_remove_user.apply_async(args=[arg])
    (stat, res) = xn_get_task_result(ret_remove, 60)
    if stat:
        fclog.error('remove user:%s failed' % (arg['username']))
        return (False, res)

    fclog.debug(res)

    ch_userkeys = UserKey.query.filter_by(id=userid).all()
    for keys in ch_userkeys:
        db.session.delete(keys)
        db.session.commit()    
        
    db.session.delete(ch_user)
    db.session.commit()    

    fclog.info('remove user:%s successfully' % (arg['username']))
    return (True, res)

def __get_s3key(res, user_id):
    newkeys = res['keys']
    
    for newkey in newkeys:
        akey = newkey['access_key']
        ch_userkey = UserKey.query.filter_by(accesskey=akey).first()
        if ch_userkey == None:
                break
     
    return (newkey['access_key'],newkey['secret_key'])

def create_s3key(arg):
    """
    {
        "user_id":1
    }
    """
    user_id = arg['user_id']

    ch_user = User.query.filter_by(id=user_id).first()
    if ch_user == None:
        warning = 'the userid:%d do not  exists' % user_id
        fclog.warning(warning)
        return (False, warning) 

    argv = {}
    argv['username'] = ch_user.username

    ret_create = agent_cephrgw_create_s3key.apply_async(args=[argv])
    (stat, res) = xn_get_task_result(ret_create, 60)
    if stat:
        fclog.error('create s3key failed')
        return (False, res)

    fclog.debug(res)

    res = json.loads(res)

    akey, skey = __get_s3key(res, user_id)
    userkey = UserKey(akey=akey, skey=skey)
    userkey.user_id = user_id
    db.session.add(userkey)
    db.session.commit()    

    return (True, res)

def remove_s3key(s3keyid):
    ch_userkey = UserKey.query.filter_by(id=s3keyid).first()
    if ch_userkey == None:
        warning = 'the userkey id:%d do not exists' % s3keyid
        fclog.warning(warning)
        return (False, warning) 

    userid = ch_userkey.user_id
    ch_user = User.query.filter_by(id=userid).first()
    if ch_user == None:
        warning = 'the user do not exists'
        fclog.warning(warning)
        return (False, warning) 

    arg = {}
    arg['username'] = ch_user.username
    arg['accesskey'] = ch_userkey.accesskey

    ret_remove = agent_cephrgw_remove_s3key.apply_async(args=[arg])
    (stat, res) = xn_get_task_result(ret_remove, 60)
    if stat:
        fclog.error('remove s3key %s:%s failed' % (arg['username'], arg['accesskey']))
        return (False, res)

    fclog.debug(res)

    db.session.delete(ch_userkey)
    db.session.commit()    

    fclog.info('remove s3key %s:%s failed' % (arg['username'], arg['accesskey']))
    return (True, res)

def gen_swiftkey(arg):
    """
    {
        "username":"admin"
    }
    """

def __get_secretkey(res, user, subuser):
    uname = "%s:%s" % (user,subuser)
    swift_keys = res['swift_keys']
    for swift_key in swift_keys:
        if uname == swift_key['user']:
            return swift_key['secret_key']

def create_subuser(arg):
    """
    {
        "user_id":1,
        "username":"admin"
    }
    """

    u_id = arg['user_id']
    uname = arg['username']

    ch_user = User.query.filter_by(id=u_id).first()
    if ch_user == None:
        warning = 'the user:%d do not  exists' % u_id
        fclog.warning(warning)
        return (False, warning) 
    
    ch_subuser = SubUser.query.filter_by(username=uname).first()
    if ch_subuser != None:
        warning = 'the subuser:%s already  exists' % uname
        fclog.warning(warning)
        return (False, warning) 

    argv = {}
    argv['username'] = ch_user.username
    argv['subusername'] = uname

    ret_create = agent_cephrgw_create_subuser.apply_async(args=[argv])
    (stat, res) = xn_get_task_result(ret_create, 60)
    if stat:
        fclog.error('create subuser:%s failed' % uname)
        return (False, res)

    fclog.debug(res)

    res = json.loads(res)

    subuser = SubUser(username=uname)
    subuser.user_id = u_id
    subuser.secretkey = __get_secretkey(res, ch_user.username, uname) 
    db.session.add(subuser)
    db.session.commit()    

    fclog.info('create subuser:%s successfully' % (uname))
    return (True, res)

def remove_subuser(subuserid):
    ch_subuser = SubUser.query.filter_by(id=subuserid).first()
    if ch_subuser == None:
        warning = 'the subuser:%s do not exists' % subuserid
        fclog.warning(warning)
        return (False, warning) 

    userid = ch_subuser.user_id
    ch_user = User.query.filter_by(id=userid).first()
    if ch_user == None:
        warning = 'the user do not exists'
        fclog.warning(warning)
        return (False, warning) 

    arg = {}
    arg['username'] = ch_user.username
    arg['subusername'] = ch_subuser.username

    ret_remove = agent_cephrgw_remove_subuser.apply_async(args=[arg])
    (stat, res) = xn_get_task_result(ret_remove, 60)
    if stat:
        fclog.error('remove %s:%s failed' % (arg['username'], arg['subusername']))
        return (False, res)

    fclog.debug(res)

    db.session.delete(ch_subuser)
    db.session.commit()    

    fclog.info('remove subuser:%s successfully' % (arg['subusername']))
    return (True, res)
