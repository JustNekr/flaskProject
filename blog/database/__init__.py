from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

__all__ = [    # указывает что импортируется при from HERE import *
    "db",
    ]