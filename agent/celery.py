from __future__ import absolute_import, unicode_literals
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from celery import Celery, platforms
from agent.comm_path import redis_server_ip, redis_server_port


REDIS_BROKER = 'redis://%s:%d/0' % (redis_server_ip, redis_server_port)
REDIS_BACKEND = 'redis://%s:%d/1' % (redis_server_ip, redis_server_port)

ALL_AGENT_TASKS = [
    'agent.common',
    'agent.cephrgw_users',
    'agent.cephrgw_buckets',
    'agent.cephrgw_objects'
    ]

app = Celery('agent',
             broker = REDIS_BROKER,
             backend = REDIS_BACKEND,
             include = ALL_AGENT_TASKS)

platforms.C_FORCE_ROOT = True

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires = 3600, #task result survival time
)

if __name__ == '__main__':
    app.start()

