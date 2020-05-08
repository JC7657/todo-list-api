from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    __tablename__= 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    todos = db.relationship('Todo', backref='user', lazy=True)

    def __repr__(self):
        return "<User %r>" % self.id

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "todos": self.todos
        }

class Todo(db.Model):
    __tablename__= 'todos'
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String, nullable=False)
    done = db.Column(db.Boolean, default=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return "<Todo %r>" % self.id

    def serialize(self):
        return {
            "id": self.id,
            "label": self.label,
            "done": self.done
        }
