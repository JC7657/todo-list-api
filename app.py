import os
import json
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from models import db, User, Todo

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG'] = True
app.config['ENV'] = "development"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'dev.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)
db.init_app(app)
Migrate(app, db)
manager = Manager(app)
manager.add_command("db", MigrateCommand)

@app.route('/')
def root():
    return render_template("index.html")

@app.route('/todos/user/<username>', methods=['POST'])
def createList(username):
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    username = request.view_args['username']
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({"msg": "List already exists"}), 400
    
    new_user = User()
    new_user.username = username
    new_user.todos = []
    db.session.add(new_user)
    db.session.commit()

    userId = User.query.filter_by(username=username).first().id

    return jsonify({"result": "ok"}), 200

@app.route('/todos/user/<username>', methods=['DELETE'])
def deleteList(username):

    username = request.view_args['username']
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"msg": "User not found"})
    userTodos = Todo.query.filter_by(user_id=user.id).all()
    if userTodos:
        for todo in userTodos:
            db.session.delete(todo)
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({"result": "ok"}), 200

@app.route('/todos/user/<username>', methods=['PUT'])
def updateList(username):
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    label = request.json.get('label', None)
    if not label:
        return jsonify({"msg": "Missing label parameter"}), 400
    username = request.view_args['username']
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"msg": "User does not exists"}), 404

    new_todo = Todo()
    new_todo.label = label
    new_todo.user = user
    db.session.add(new_todo)
    db.session.commit()

@app.route('/todos/user/<username>', methods=['GET'])
def getList(username):
    username = request.view_args['username']
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"msg": "User not found"}), 404
    userList = []
    todos = Todo.query.filter_by(user_id=user.id).all()
    for todo in todos:
        userList.append(todo.serialize())
    print(userList)

    
    return jsonify(userList), 200


#--------------------------------------------

if __name__ == '__main__':
    manager.run()