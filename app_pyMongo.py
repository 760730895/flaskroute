# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# Author     ：hu_cl
# Date       ：2022/4/21 9:41
# File       : app_pyMongo.py
# Description：
"""
import pymongo
from flask import Flask, render_template
from flask_pymongo import PyMongo, DESCENDING
from datetime import datetime

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    MONGO_USERNAME='root',
    MONGO_PASSWORD='123456',
    MONGO_URI='mongodb://172.16.30.252:27017/flask'
)

mongo = PyMongo(app)


# mongo_test = PyMongo(app, config_prefix='MONGO_TEST')

@app.route('/init')
def init():
    pymongo.collection.Collection('flask', 'users', create=True)
    return 'Init Successful'


@app.route('/drop')
def drop():
    mongo.db.users.drop()
    return 'Drop Successful'


@app.route('/user')
@app.route('/user/<string:name>')
def user(name=None):
    if name is None:
        users = mongo.db.users.find({'age': {'$lt': 20}}).sort('age', DESCENDING)
        ages = mongo.db.users.find().distinct('age')
        print(type(ages))
        return render_template('users.html', users=users, count=users.count())
    else:
        user = mongo.db.users.find_one({'name': name})
        if user is not None:
            return render_template('users.html', users=[user], count=1)
        else:
            return 'No user found!'


@app.route('/article')
def article():
    articles = mongo_test.db.articles.find().limit(5).skip(2)
    print(articles.count())
    return render_template('articles.html', articles=articles)


@app.route('/add')
def add():
    user = {'name': 'Michael', 'age': 18, 'scores': [{'course': 'Math', 'score': 76}]}
    user_id = mongo.db.users.insert_one(user).inserted_id
    print('Add user with id: %s' % user_id)

    user = {'name': 'Tom', 'age': 21, 'scores': [{'course': 'Math', 'score': 85.5},
                                                 {'course': 'Politics', 'score': 58}]}
    user_id = mongo.db.users.insert_one(user).inserted_id
    print('Add user with id: %s' % user_id)

    user = {'name': 'Jane', 'age': 17, 'scores': [{'course': 'Politics',
                                                   'score': 82,
                                                   'date': datetime.now()}]}
    user_id = mongo.db.users.insert_one(user).inserted_id
    print('Add user with id: %s' % user_id)

    users = mongo.db.users.find()
    return render_template('users.html', users=users, count=users.count())


@app.route('/add-batch')
def add_batch():
    result = mongo.db.tests.insert_many([{'num': i} for i in range(3)])
    print(result.inserted_ids)
    return 'Add batch Successful'


@app.route('/add-article')
def add_article():
    article = {'title': 'How to use Flask', 'summary': 'An article to demostrate Flask usage.'}
    article_id = mongo_test.db.articles.insert_one(article).inserted_id
    print('Add article with id: %s' % article_id)

    articles = mongo_test.db.articles.find()
    return render_template('articles.html', articles=articles)


@app.route('/update')
def update():
    result = mongo.db.users.update_one({'name': 'Tom'}, {'$inc': {'age': 3}})
    # result = mongo.db.users.update_many({'age':{'$lt':20}}, {'$set': {'age': 20}})
    print('%d records modified' % result.modified_count)
    users = mongo.db.users.find()
    return render_template('users.html', users=users, count=users.count())


@app.route('/replace')
def replace():
    user = {'name': 'Lisa', 'age': 21, 'scores': [{'course': 'Politics', 'score': 95}]}
    result = mongo.db.users.replace_one({'name': 'Jane'}, user)
    print('%d records modified' % result.modified_count)
    users = mongo.db.users.find()
    return render_template('users.html', users=users, count=users.count())


@app.route('/delete')
def delete():
    result = mongo.db.users.delete_one({'name': 'Michael'})
    # result = mongo.db.users.delete_many({'age':{'$gt':20}})
    print('%d records deleted' % result.deleted_count)
    users = mongo.db.users.find()
    return render_template('users.html', users=users, count=users.count())


if __name__ == '__main__':
    app.run(host='0.0.0.0')
