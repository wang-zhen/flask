from __future__ import absolute_import, unicode_literals
#!/usr/bin/python
# -*- coding: UTF-8 -*-
from common.db import db

class Bucket(db.Model):
    __tablename__ = 'buckets'
    id = db.Column(db.Integer, primary_key=True)
    bkname = db.Column(db.String(64), unique=True, nullable=False)
    permission = db.Column(db.String(64))
    subusers = db.relationship('SubUser', backref='user', lazy=True)
    userkeys = db.relationship('UserKey', backref='user', lazy=True)

    def __init__(self,username):
        self.username = username

    def __repr__(self):
        return '<User: %r>' % self.username
