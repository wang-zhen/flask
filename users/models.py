from __future__ import absolute_import, unicode_literals
#!/usr/bin/python
# -*- coding: UTF-8 -*-
from common.db import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    displayname = db.Column(db.String(64))
    email = db.Column(db.String(64))
    #opmask = db.Column(db.String(32))
    #caps = db.Column(db.String(64))
    subusers = db.relationship('SubUser', backref='user', lazy=True)
    userkeys = db.relationship('UserKey', backref='user', lazy=True)

    def __init__(self,username):
        self.username = username

    def __repr__(self):
        return '<User: %r>' % self.username

class SubUser(db.Model):
    __tablename__ = 'subusers'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    secretkey = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return '<SubUser: %r>' % self.username

class UserKey(db.Model):
    __tablename__ = 'userkeys'
    id = db.Column(db.Integer, primary_key=True)
    accesskey = db.Column(db.String(64), unique=True)
    secretkey = db.Column(db.String(64), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, akey, skey):
        self.accesskey = akey
        self.secretkey = skey
