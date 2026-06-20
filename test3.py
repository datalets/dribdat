from flask import Flask, render_template_string
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField

app = Flask(__name__)
app.config['WTF_CSRF_ENABLED'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = 'test'
app.config['RECAPTCHA_PRIVATE_KEY'] = 'test'

class F(FlaskForm):
    name = StringField("name")
    recaptcha = RecaptchaField()

template = """
{% macro render_input(field) %}
  INPUT: {{ field(class_="form-control") }}
{% endmacro %}

{% for field in form %}
  {% if field.type == "RecaptchaField" %}
     {{ field }}
  {% else %}
     {{ render_input(field) }}
  {% endif %}
{% endfor %}
"""

with app.app_context():
    f = F()
    print(render_template_string(template, form=f))
