from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField

class MarcaForm(FlaskForm):
        nombre = StringField('Nombre')
        submit = SubmitField('Guardar')
        