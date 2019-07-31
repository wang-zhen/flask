from __future__ import absolute_import, unicode_literals
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from subprocess import Popen, PIPE, check_call
from agent.celery import app

#import os
#from agent.common import *
#from agent.comm_path import *

@app.task(bind=True)
def agent_test_buckets(self, arg):
    print "agent_test_buckets"
    return (False, '1')
