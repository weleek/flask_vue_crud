# -*- coding: utf-8 -*-
import os
from flask import Flask, Blueprint, request, jsonify, render_template
from flask_mongoengine import MongoEngine

url_prefix = '/'
app = Blueprint('base', __name__)


@app.route('/health_check')
def health_check():
    return jsonify({'status': 'check'})


@app.route('/check')
def check():
    return "check"