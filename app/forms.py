from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField,PasswordField
from wtforms.validators import DataRequired

class DnsCheck(FlaskForm):
    password = StringField('The password')
    check_type = StringField('Check_type')
    domain = StringField('The domain', validators=[DataRequired()])
    license = StringField('The License')


class ZohoCheck(FlaskForm):
    keyword = StringField('client name', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    search_type = StringField('Search Type')

class Web_config(FlaskForm):
    change_input = StringField('input')
    super_password = PasswordField('super password',validators=[DataRequired()])
    change_type=StringField('change_type',validators=[DataRequired()])
