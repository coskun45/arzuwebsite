from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager
from flask_mail import Mail,Message



db = SQLAlchemy()
login_manager=LoginManager()
mail=Mail()



def createApp():
    app = Flask(__name__)
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "sqlite:///blog.db"  
    # dbname://kullaniciadi/sifre@nerdecalisacagi:port/dbname
    #postgres:postgres@localhost:5432/zero2herosakt
     #   postgres://coskun:ywMDSb5lByT8gzXoITydeG0b6FvXortS@dpg-cer9josgqg486p7angqg-a/zero2herosakt
    #
    # app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['SECRET_KEY']='mysecretkey'# web formlarinin güvenligi icin gerekli

    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT']=465
    app.config['MAIL_USE_SSL']=True
    app.config['MAIL_USERNAME']='eyupcoskun.de@gmail.com'
    app.config['MAIL_PASSWORD']='irffeaebmoutpmzz'
    Mail(app)



    CORS(app)

    db.init_app(app)
    app.secret_key = 'xxxxyyyyyzzzzz'
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    return app



