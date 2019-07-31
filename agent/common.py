from __future__ import absolute_import, unicode_literals
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from agent.celery import app
from agent.comm_path import *
from common.fclog import fclog

import os, os.path
import uuid
import json
import time
import platform
import subprocess
import signal
import paramiko, json

@app.task(bind=True)
def agent_run_command(self, cmd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(hostname=ceph_rgw_ip, port=ceph_rgw_port, username=ceph_rgw_user,password=ceph_rgw_pwd)

    chan = ssh.get_transport().open_session()
    chan.exec_command(cmd)

    stdout = chan.makefile('rb', -1) 
    stderr = chan.makefile_stderr('rb', -1) 

    status = chan.recv_exit_status()
    stdout = stdout.read().decode('utf-8')
    stderr = stderr.read().decode('utf-8')

    ssh.close()
    if 0 != status:
        return status, stderr
    return status, stdout

#AGENT_DB_BACKEND = False

def xn_wait_task_finished(task_handle):
    task_success = False
    wait_time_out = 300 # 30 * 1000 ms / 100 ms = 300
    count = 0
    #timeout is 30 seconds.
    while (False == task_handle.ready() and count <= wait_time_out):
        time.sleep(0.2)
        count = count + 1

    task_success = True

def xn_get_task_result(task_handle, timeout = 30):
    """
    1\ wait task ready. if timeout , return False.
       maybe a timeout arg is needed, and set a default value.
    2\ if ready, return task's result.

    IN: task handle.
    OUT: success -> task result  failure -> False
    """
    res = (False, 'Task failed.')
    wait_time_out = timeout # default 30 seconds
    count = 0

    while (False == task_handle.ready() and count <= wait_time_out):
        time.sleep(0.2)
        count = count + 0.2

    if (count > wait_time_out):
        fclog.error("task is timeout while task_handle = %s ." % task_handle)
        return (False, 'Task timeout.')

    res = task_handle.get()
    return (res)

def xn_get_task_result_by_ids(ids, timeout = 30):
    """
    ['68b9b191-b06d-413e-8ca0-251832ad67ce',
     'd5919f37-cea3-4a74-a4c1-7644459de60b',
     '74d59c05-f946-43d2-9e37-025b5488b3ec' ]

    """
    task_cnt = len(ids)
    success_cnt = 0
    t = 0

    print 'tsk list(%s), tsk cnt(%s)' % (ids, task_cnt)

    #init ret value.
    ret = []

    #is task returned.
    returned = []
    for tid in ids:
        ret.append([False, 'timeout'])
        returned.append(False)

    while (t < timeout):
        for i in range(task_cnt):
            if returned[i] == True:
                fclog.debug('Cur task(%s) is ready,check next.' % i)
                continue

            #if task ready, then save task result.
            task_handle = app.AsyncResult(ids[i])
            if True == task_handle.ready():
                success_cnt = success_cnt + 1
                res = task_handle.get()
                ret[i] = res
                print 'res=%s , ret=%s i=%s' % (res, ret, i)
                returned[i] = True

        if success_cnt == task_cnt:
            break

        time.sleep(0.2)
        t = t + 0.2

    return ret
