from wtforms import Form, PasswordField, StringField
from wtforms.validators import InputRequired

from src.infrastructure.depends.base import InfraDIContainer


class UserCreateForm(Form):
    first_name = StringField("Имя")
    second_name = StringField("Фамилия")
    email = StringField("Email", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

    password_hasher = InfraDIContainer.password_hasher()

    def validate_password(form, field):
        if not field.data:
            raise ValueError("Password is Required")

        if len(field.data) < 6:
            raise ValueError("Password length should be more than 5 symbol")

    def populate_obj(self, obj):
        super().populate_obj(obj)
        obj.hash_password = self.password_hasher.hash_password(obj.password)
        super().populate_obj(obj)
