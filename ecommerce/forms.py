from wtforms.validators import  DataRequired,Length,Email
from flask_wtf import  FlaskForm
from wtforms import StringField, PasswordField,SubmitField,SelectField,TextAreaField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    name=StringField('Name',validators=[DataRequired(), Length(min=2,max=20)])
    brans=SelectField('Brans',validators=[DataRequired()],
    choices=[
        ('cho_1','Developer'),
        ('cho_2','System'),
        ('cho_3','Cyber Security'),
        ('cho_4','Data Science'),
        ('cho_5','GIS'),
        ('cho_6','Diger')
        ]
    )
    email=StringField('Email',validators=[DataRequired(), Email()])
    referans_email=StringField('Referans_email',validators=[DataRequired(), Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    submit=SubmitField('sign')

class LoginForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(), Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    submit=SubmitField('LOGIN')

class PostForm(FlaskForm):
    title=StringField('Title',validators=[DataRequired()])
    subtitle=StringField('Subtitle',validators=[DataRequired()])
    post_text=TextAreaField('Post Text',validators=[DataRequired()])
    submit=SubmitField('ADD POST')

class ContactForm(FlaskForm):
    name=StringField('Name',validators=[DataRequired()])
    email=StringField('Email',validators=[DataRequired(), Email()])

    phone=StringField('Phon number',validators=[DataRequired()])
    message=TextAreaField('Message',validators=[DataRequired()])
    submit=SubmitField('ADD POST')

    