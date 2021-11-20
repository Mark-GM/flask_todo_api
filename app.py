from flask import Flask, request
from flask_restful import Api, Resource, abort
import logging, secrets
from models import db, Todo


logging.basicConfig(
    filename="flask.logs",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(name)s in %(module)s: %(message)s",
)


todo_app = Flask(__name__)
todo_api = Api(todo_app)
todo_app.config["SECRET_KEY"] = secrets.token_hex(64)
todo_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
todo_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


#######################
##    RESTful API    ##
#######################


class TodoRUD(Resource):
    def get(self, id):
        """
        Get a task by id
        """
        task = Todo.query.get(id)
        if not task:
            abort(404, message="Not Found")

        data = {
            "id": task.id,
            "name": task.name,
            "description": task.description,
            "priority": task.priority,
            "done": task.done,
        }

        return data, 200

    def patch(self, id):
        """
        Update task data
        """
        try:
            task = Todo.query.get(id)
            if request.form.get("name"):
                task.name = request.form.get("name")
            if request.form.get("description"):
                task.description = request.form.get("description")
            if request.form.get("priority"):
                task.priority = request.form.get("priority")
            if request.form.get("done"):
                # SQLite stores boolean data as integers 0 (false) and 1 (true)
                # see: https://www.sqlite.org/datatype3.html#boolean_datatype
                task.done = int(request.form.get("done"))

            db.session.commit()  # commit to db

            return {"message": f"Task '{task.name}' Updated Successfully"}, 201
        except Exception as e:
            abort(500, message="Internal Server Error")

        pass

    def delete(self, id):
        """
        Delete todo by id
        """
        todo_obj = Todo.query.get(id)

        db.session.delete(todo_obj)  # delete query
        db.session.commit()

        return {"message": "Deleted Successfully"}, 200


class TodoLC(Resource):
    def get(self):
        """
        List all Todo tasks
        """
        try:
            todo_objects = Todo.query.filter().all()

            limit = request.args.get("limit")

            my_new_list = []

            for task in todo_objects:
                data = {
                    "id": task.id,
                    "name": task.name,
                    "description": task.description,
                    "priority": task.priority,
                    "done": task.done,
                }

                my_new_list.append(data)

            if limit:
                my_new_list = my_new_list[: int(limit)]

            return my_new_list

        except Exception as e:
            abort(500, message=f"Internal Server Error {e}")

    def post(self):
        """
        Add a new todo task
        """
        try:
            data = {
                "name": request.form.get("name"),
                "description": request.form.get("description"),
                "priority": int(request.form.get("priority")),
                # SQLite stores boolean data as integers 0 (false) and 1 (true)
                # see: https://www.sqlite.org/datatype3.html#boolean_datatype
                "done": False,
            }

            todo_obj = Todo(**data)  # create object of Todo
            db.session.add(todo_obj)  # insert query inside the db
            db.session.commit()  # commit to db

            return {"message": "Task Created Successfully"}, 201
        except Exception as e:
            abort(500, message="Internal Server Error")


# Register TodoLC Resource class
todo_api.add_resource(TodoLC, "/api/v1/todos/")

# Register TodoRUD Resource class
todo_api.add_resource(TodoRUD, "/api/v1/todos/<int:id>/")

# Attach SQLAlchemy to app
db.init_app(todo_app)


# Create Database Tables
@todo_app.before_first_request
def initiate_data_base_tables():
    db.create_all()


todo_app.run(debug=True)
