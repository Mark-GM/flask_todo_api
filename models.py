from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()


class Todo(db.Model):
    """
    Todos database model
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text())
    priority = db.Column(db.Integer)
    done = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.created_at = datetime.now()
