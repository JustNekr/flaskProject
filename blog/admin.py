from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from blog.database import db
from blog.database.models import User, Barber

admin = Admin(name="Barber Admin", template_mode="bootstrap4")

admin.add_view(ModelView(User, db.session, endpoint="users_"))
admin.add_view(ModelView(Barber, db.session, endpoint="barber"))