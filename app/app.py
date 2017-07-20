# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, jsonify, session, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from kftc_openplatform import KftcOpenAPI


# configuration
DEBUG = True
SECRET_KEY = "development-key"
SQLALCHEMY_DATABASE_URI = 'sqlite://database.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
KFTC_OPENPLATFORM_ENDPOINT = ''

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('KFTC_EXAMPLE_SETTINGS', silent=True)

db = SQLAlchemy(app)


api = KftcOpenAPI()


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True)
#     password = db.Column(db.String(255))


@app.route('/')
def index():
    return render_template('index.html',
                           authorize_url=api.build_authorize_url('login inquiry'))


@app.route('/logout')
def logout():
    flash('You have been successfully logged out.')
    session.pop('kftc_token', None)
    return redirect('index')


@app.route('/callback')
def callback():
    code = request.args.get('code', None)
    # scope = request.args.get('scope', None)

    res = api.get_token(code)
    session['kftc_token'] = res
    return redirect('index')
