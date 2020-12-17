from flask import Flask, render_template, request, redirect, url_for, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
#import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://anna@localhost:5432/todonew'
db = SQLAlchemy(app)

migrate = Migrate(app, db)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    comleted = db.Column(db.Boolean, nullable=True, default=True)

    def __repr__(self):
        return '<Todo {self.id} {self.description} {self.completed}>'

db.create_all()

@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    body = {}
    try:
        description = request.get_json()['description']
        todo = Todo(description=description)
        db.session.add(todo)
        db.session.commit()
        body['description'] = todo.description
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort (400)
    else:
        return jsonify(body)

    @app.route('/todos/<todo_id>/set-completed', methods=['POST'])
    def set_completed_todo(todo_id):
      try:
        completed = request.get_json()['completed']
        print('completed', completed)
        todo = Todo.query.get(todo_id)
        todo.completed = completed
        db.session.commit()
      except:
        db.session.rollback()
      finally:
        db.session.close()
      if error:
        abort (400)
      else:
        return jsonify(body)
      return redirect(url_for('index'))

@app.route('/')
def index():
    data=Todo.query.all()
    print (data)

    return render_template('index.html', data=Todo.query.all())

# if __name__ == '__main__':
    # app.run(
        # port=3000,
        # debug=True,
        # host='0.0.0.0'
        # )
