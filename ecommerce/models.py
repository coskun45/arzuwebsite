from dataclasses import dataclass
from ecommerce import db,login_manager
from datetime import datetime
from flask_login import  UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)




@dataclass
class User(db.Model,UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    brans = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    referans_email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, id, name,brans,referans_email, email, password):
        self.id = id
        self.name = name
        self.brans = brans
        self.referans_email = referans_email
        self.email = email
        self.password = password
    def __repr__(self):
        return f'User: {self.name}, {self.email}'

    @classmethod
    def add_user(cls, name, brans,referans_email,email, password):
        user = cls(None, name,brans,referans_email, email, password)
        db.session.add(user)
        db.session.commit()
    @classmethod
    def get_user_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
    @classmethod
    def get_user_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
    @classmethod
    def get_user_by_email(cls, referans_email):
        return cls.query.filter_by(email=referans_email).first()

@dataclass
class Post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    subtitle = db.Column(db.String(120), nullable=False)
    post_date = db.Column(db.DateTime, nullable=False,default=datetime.now)#().strftime('%Y-%m-%d'))
    post_text = db.Column(db.String(120), nullable=False)
    post_from = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    


    
    def __init__(self, id, title, subtitle, post_text,user_id,post_from):
        self.id = id
        self.title = title
        self.subtitle = subtitle
        self.post_text = post_text
        self.user_id=user_id
        self.post_from=post_from
    
    @classmethod
    def add_post(cls, title, subtitle,post_text,user_id,post_from):
        post = cls(None, title,subtitle,post_text,user_id,post_from)
        db.session.add(post)
        db.session.commit()
    @classmethod
    def get_all_posts(cls):
        return cls.query.order_by(cls.id.desc()).all()

'''
    def __repr__(self):
        return f'Post: {self.title}, {self.subtitle}'
    @classmethod
    def add_post(cls, title, subtitle,post_text,user_id):
        post = cls(None, title,subtitle,post_text,user_id)
        db.session.add(post)
        db.session.commit()


    @classmethod
    def get_all_users(cls):
        return cls.query.all()

    @classmethod
    def get_user_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    

    @classmethod
    def update_user(cls, id, username, email, password):
        user = cls.query.filter_by(id=id).first()
        user.username = username
        user.email = email
        user.password = password
        db.session.commit()

    @classmethod
    def delete_user(cls, id):
        user = cls.query.filter_by(id=id).first()
        db.session.delete(user)
        db.session.commit()

    @classmethod
    def activate_user(cls, id):
        user = cls.query.filter_by(id=id).first()
        user.activated = True
        db.session.commit()

    @classmethod
    def deactivate_user(cls, id):
        user = cls.query.filter_by(id=id).first()
        user.activated = False
        db.session.commit()


@dataclass
class Admin(db.Model):
    __tablename__ = "admin"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120))
    mod = db.Column(db.Integer, default=0)

    def __init__(self, id, name, email, password, mod):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.mod = mod

    @classmethod
    def get_all_admins(cls):
        return cls.query.all()

    @classmethod
    def get_admin_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def add_admin(cls, name, email, password):
        admin = cls(None, name, email, password, 0)
        db.session.add(admin)
        db.session.commit()

    @classmethod
    def update_admin(cls, id, name, email, password):
        admin = cls.query.filter_by(id=id).first()
        admin.name = name
        admin.email = email
        admin.password = password
        db.session.commit()

    @classmethod
    def delete_admin(cls, id):
        admin = cls.query.filter_by(id=id).first()
        db.session.delete(admin)
        db.session.commit()

'''
