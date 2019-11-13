# -*- coding: utf-8 -*-
import mongoengine as me
import datetime


class User(me.Document):
    seq = me.IntField()
    user_id = me.StringField(required=True)
    name = me.StringField()
    password = me.StringField()
    insert_date = me.DateTimeField(defualt=datetime.datetime.utcnow)
    modified_date = me.DateTimeField(default=datetime.datetime.utcnow)

