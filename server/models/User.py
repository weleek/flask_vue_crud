# -*- coding: utf-8 -*-

import mongoengine as me

class User(me.Document):
    id = me.StringField(required=True)
    name = me.StringField()
    password = me.StringField()
