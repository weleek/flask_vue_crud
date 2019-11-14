# -*- coding: utf-8 -*-
import datetime

import mongoengine as me


class User(me.Document):
    _id = me.StringField(required=True, primary_key=True)
    name = me.StringField()
    password = me.StringField()
    insert_date = me.DateTimeField(defualt=datetime.datetime.utcnow)
    modified_date = me.DateTimeField(default=datetime.datetime.utcnow)


