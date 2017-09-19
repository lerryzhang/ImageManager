#coding=utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField,PasswordField,SubmitField,IntegerField,RadioField,SelectField
from wtforms.validators import DataRequired
from wtforms.validators import Required



class RegisterForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password =PasswordField('password',validators=[DataRequired()])
    email=StringField('email',validators=[DataRequired()])
    age=IntegerField('age')
    sex= SelectField('Job',choices=[
        ('1',u'男' ),
        ('2',u'女'),

    ])
    tel=IntegerField('tel')
    address = StringField('address')
    #remember_me = BooleanField('remember_me', default=False)
    submit = SubmitField(u'注册')


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password =PasswordField('password',validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
    submit = SubmitField(u'登陆')