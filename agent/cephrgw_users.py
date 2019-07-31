from __future__ import absolute_import, unicode_literals
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from subprocess import Popen, PIPE, check_call
from agent.celery import app

import os
import time
import traceback
from agent.common import *
from agent.comm_path import *
from common.fclog import *

@app.task(bind=True)
def agent_cephrgw_user_list(self, arg):

    cmd = 'radosgw-admin  user list --format json'

    fclog.info(cmd)

    status, output = agent_run_command(cmd)
    if(status):
        fclog.error(output)

    return (status, output)

@app.task(bind=True)
def agent_cephrgw_user_info(self, arg):
    """
    arg = { 
        "username":"admin"
    }
    """

    cmd = 'radosgw-admin  user info --uid=%s --format json' % (arg['username'])

    fclog.info(cmd)

    status, output = agent_run_command(cmd)
    if(status):
        fclog.error(output)

    return (status, output)

@app.task(bind=True)
def agent_cephrgw_create_user(self, arg):
    """
    arg = {
        "username":"admin"
    }
    do not support "display-name" and "email"
    """
    
    cmd = 'radosgw-admin user create --uid=%s --display-name=%s --email=%s --format json' % (
        arg['username'], arg['username'], arg['username'])
    print "1111111111"
    fclog.info(cmd)

    status, output = agent_run_command(cmd)
    if(status):
        fclog.error(output)

    return (status, output)

@app.task(bind=True)
def agent_cephrgw_create_subuser(self, arg):
    """
    arg = {
        "username":"admin",
        "subusername":"johndoe"
    }
    """
    
    cmd = 'radosgw-admin subuser create --uid=%s --subuser=%s --access=full --format json' % (
        arg['username'], arg['subusername'])

    fclog.info(cmd)

    status, output = agent_run_command(cmd)
    if(status):
        fclog.error(output)

    return (status, output)

@app.task(bind=True)
def agent_cephrgw_remove_subuser(self, arg):
    """
    arg = {
        "username":"admin",
        "subusername":"johndoe"
    }
    """
    
    cmd = 'radosgw-admin subuser rm --subuser=%s:%s' % (
        arg['username'], arg['subusername'])

    fclog.info(cmd)

    status, output = agent_run_command(cmd)
    if(status):
        fclog.error(output)

    return (status, output)

@app.task(bind=True)
def agent_cephrgw_remove_user(self, arg):
    """
    arg = {
        "username":"admin"
    }
    """

    cmd = 'radosgw-admin user rm --uid=%s' % (arg['username'])

    fclog.info(cmd)

    status, output = agent_run_command(cmd)
    if(status):
        fclog.error(output)

    return (status, output)

@app.task(bind=True)
def agent_cephrgw_create_s3key(self, arg):
    """
    arg = {
        "username":"admin"
    }
    """
    
    cmd = 'radosgw-admin key create --uid=%s --key-type=s3 --gen-access-key --gen-secret --format json' % (
        arg['username'])

    fclog.info(cmd)

    status, output = agent_run_command(cmd)
    if(status):
        fclog.error(output)

    return (status, output)

@app.task(bind=True)
def agent_cephrgw_create_swiftkey(self, arg):
    """
    arg = {
        "username":"admin",
        "subusername":"johndoe"
    }
    """
    
    cmd = 'radosgw-admin key create --subuser=%s:%s --key-type=swift --gen-secret --format json' % (
        arg['username'], arg['subusername'])

    fclog.info(cmd)

    status, output = agent_run_command(cmd)
    if(status):
        fclog.error(output)

    return (status, output)

@app.task(bind=True)
def agent_cephrgw_remove_s3key(self, arg):
    """
    arg = {
        "username":"admin",
        "accesskey":"G6SZ2E7DGQM41146WXII"
    }
    """
    
    cmd = 'radosgw-admin key rm --uid=%s --access_key=%s' % (
        arg['username'], arg['accesskey'])

    fclog.info(cmd)

    status, output = agent_run_command(cmd)
    if(status):
        fclog.error(output)

    return (status, output)

@app.task(bind=True)
def agent_cephrgw_remove_swiftkey(self, arg):
    """
    arg = {
        "username":"admin",
        "subusername":"subuser"
    }
    """
    
    cmd = 'radosgw-admin key rm --subuser=%s:%s' % (
        arg['username'], arg['subusername'])

    fclog.info(cmd)

    status, output = agent_run_command(cmd)
    if(status):
        fclog.error(output)

    return (status, output)
