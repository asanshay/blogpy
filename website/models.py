from . import db
from flask_login import UserMixin
from sqlalchemy.orm import relationship


class Author(db.Model,UserMixin):
    def __init__(self,username,first_name,last_name,email,password,picture):
        self.username  = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.picture = picture


    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80),unique=True,nullable=False)
    first_name = db.Column(db.String(80),unique=False,nullable=False)
    last_name = db.Column(db.String(80),unique=False,nullable=False)
    email = db.Column(db.String(80),unique=True,nullable=False)
    password = db.Column(db.String(120),unique=False,nullable=False)
    blog = relationship('Blog',backref='author')
    picture = db.Column(db.String(400),unique=False,nullable=False)

class Blog(db.Model):
    def __init__(self,content,author_id):
        self.content = content
        self.author_id = author_id

    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.String(250000),unique=False,nullable=False)
    author_id = db.Column(db.Integer,db.ForeignKey(Author.id))
    comments = relationship('Comment',backref="blog")

class Comment(db.Model):
    def __init__(self,content,author_id,post_id):
        self.content = content
        self.author_id = author_id
        self.post_id = post_id

    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.String(2500),unique=False,nullable=False)
    author_id = db.Column(db.Integer,db.ForeignKey(Blog.id))

