# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# Author     ：hu_cl
# Date       ：2022/4/20 16:55
# File       : app_sqlalchemy.py
# Description：
"""
from flask import Flask, render_template
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/user.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    age = db.Column(db.Integer)

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return '<User %r>' % self.name


class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course = db.Column(db.String(50))
    assess_date = db.Column(db.DateTime)
    score = db.Column(db.Float)
    is_pass = db.Column(db.Boolean)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('scores', lazy='dynamic'))

    def __init__(self, course, score, user, assess_date=None):
        self.course = course
        self.score = score
        self.is_pass = (score >= 60)
        if assess_date is None:
            assess_date = datetime.now()
        self.assess_date = assess_date
        self.user = user

    def __repr__(self):
        return '<Course %r of User %r>' % (self.course, self.user.name)


@app.route('/init')
def init():
    db.create_all()
    return 'Init Successful'


@app.route('/drop')
def drop():
    db.drop_all()
    return 'Drop Successful'


@app.route('/add')
def add():
    db.session.add(User('Michael', 18))
    db.session.add(User('Tom', 21))
    db.session.add(User('Jane', 17))
    db.session.commit()
    users = User.query.all()
    return render_template('users.html', users=users)


@app.route('/addscore')
def add_score():
    user = User.query.filter_by(name='Tom').first()
    if user is not None:
        db.session.add(Score('Math', 80.5, user))
        db.session.add(Score('Politics', 58, user))
    user = User.query.filter_by(name='Jane').first()
    if user is not None:
        db.session.add(Score('Math', 88, user))
    db.session.commit()
    return 'Add Score Successful'


@app.route('/scores/<string:name>')
def scores(name):
    user = User.query.filter_by(name=name).first()
    if user is not None:
        return render_template('scores.html', name=name, scores=user.scores)
    else:
        return 'No user found!'


@app.route('/user')
@app.route('/user/<string:name>')
def user(name=None):
    if name is None:
        from sqlalchemy import desc

        # SELECT * FROM user WHERE age < 30 ORDER BY age DESC LIMIT 5 OFFSET 0
        users = User.query.filter(User.age < 30).order_by(desc(User.age), User.name).limit(5).offset(0).all()
        # WHERE name LIKE 'J%' AND age < 30
        # users = User.query.filter(User.name.startswith('J'), User.age<20)
        # LIMIT 2 OFFSET 1
        # users = User.query.slice(1,3)
        return render_template('users.html', users=users)
    else:
        user = User.query.filter_by(name=name).first()
        if user is not None:
            return render_template('users.html', users=[user])
        else:
            return 'No user found!'


@app.route('/update')
def update():
    user = User.query.filter_by(name='Tom').first()
    if user is not None:
        user.age += 1
        db.session.add(user)
        db.session.commit()
    users = User.query.all()
    return render_template('users.html', users=users)


@app.route('/update-batch')
def update_batch():
    User.query.filter(User.age < 20).update({'age': User.age + 1})
    db.session.commit()
    users = User.query.all()
    return render_template('users.html', users=users)


@app.route('/del')
def delete():
    user = User.query.filter_by(name='Michael').first()
    if user is not None:
        db.session.delete(user)
        db.session.commit()
    users = User.query.all()
    return render_template('users.html', users=users)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
