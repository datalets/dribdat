from flask import Flask
from flask_wtf import FlaskForm, RecaptchaField
app = Flask(__name__)
app.config['WTF_CSRF_ENABLED'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = 'test'
app.config['RECAPTCHA_PRIVATE_KEY'] = 'test'

class F(FlaskForm):
    r = RecaptchaField()

with app.app_context():
    f = F()
    print("type:", f.r.type)
