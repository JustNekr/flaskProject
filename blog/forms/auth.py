from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectMultipleField, SelectField, widgets
from wtforms.validators import Email, DataRequired, Length, EqualTo


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=50)])
    remember = BooleanField('Remember me', default=False)
    submit = SubmitField('Submit')


class RegisterForm(FlaskForm):
    name = StringField("Имя: ", validators=[Length(min=4, max=100, message="Имя должно быть от 4 до 100 символов")])
    email = StringField("Email: ", validators=[Email("Некорректный email")])
    password = PasswordField("Пароль: ", validators=[DataRequired(),
                                                     Length(
                                                         min=4,
                                                         max=100,
                                                         message="Пароль должен быть от 4 до 100 символов")
                                                     ]
                             )

    password_2 = PasswordField("Повтор пароля: ", validators=[DataRequired(), EqualTo('password', message="Пароли не совпадают")])
    submit = SubmitField("Регистрация")


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class AppointmentForm(FlaskForm):
    barber = SelectField("Барбер", validators=[DataRequired(message='choose barber')])
    services = MultiCheckboxField("Услуги", validators=[DataRequired(message='choose even 1 service')])
    submit = SubmitField("заказ")