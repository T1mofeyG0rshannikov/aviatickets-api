from wtforms import Form, PasswordField, StringField
from wtforms.validators import InputRequired

from src.depends.depends import get_password_hasher


class UserCreateForm(Form):
    first_name = StringField("Имя")
    second_name = StringField("Фамилия")
    email = StringField("Email", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

    password_hasher = get_password_hasher()

    def validate_password(form, field):
        if not field.data:
            raise ValueError("Password is Required")

        if len(field.data) < 6:
            raise ValueError("Password length should be more than 5 symbol")

    def populate_obj(self, obj):
        print("EONFWO")
        super().populate_obj(obj)
        obj.hash_password = self.password_hasher.hash_password(obj.password)
        super().populate_obj(obj)
