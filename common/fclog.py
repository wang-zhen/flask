from __future__ import absolute_import, unicode_literals
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import logging
import logging.config

#*****************************************************************
# _____   _____       ___  ___       ___  ___   _____   __   _   *
#/  ___| /  _  \     /   |/   |     /   |/   | /  _  \ |  \ | |  *
#| |     | | | |    / /|   /| |    / /|   /| | | | | | |   \| |  *
#| |     | | | |   / / |__/ | |   / / |__/ | | | | | | | |\   |  *
#| |___  | |_| |  / /       | |  / /       | | | |_| | | | \  |  *
#\_____| \_____/ /_/        |_| /_/        |_| \_____/ |_|  \_|  *
#                                                                *
#*****************************************************************
slave_log_level = 'DEBUG'
slave_cli_log_level = 'DEBUG'


#********************
#For fclog's log.   *
#********************

#---------------------------------------------------------------------
AGENT_LOG_FILE = '/var/log/xinnet/fc.log'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s]:%(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
    },
    'handlers': {
        'console':{
            'level': slave_cli_log_level,
            #'level': 'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'level': slave_log_level,
            #'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': AGENT_LOG_FILE,
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'fc.log': {
            'handlers': ['console', 'file'],
            #'level': slave_log_level,
            'level': 'DEBUG',
            #'filters': ['special']
        }
    }
}

logging.config.dictConfig(LOGGING)

fclog = logging.getLogger('fc.log')
