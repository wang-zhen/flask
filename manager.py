from __future__ import absolute_import, unicode_literals
#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
from flask import Flask

from users import urls
from buckets import urls
from objects import urls

from users import users_page
from buckets import buckets_page
from objects import objects_page

from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate,MigrateCommand

from common.db import db
from users import models

app = Flask(__name__)

#ceph radosgw url
app.register_blueprint(users_page, url_prefix='/v1/storage')
app.register_blueprint(buckets_page, url_prefix='/v1/storage')
app.register_blueprint(objects_page, url_prefix='/v1/storage')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/cephradosgw'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)
migrate = Migrate(app,db)

manager = Manager(app)
manager.add_command('db',MigrateCommand)

if __name__ == '__main__':
    commands = sys.argv
    if 'runserver' == commands[1]:
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        manager.run()
