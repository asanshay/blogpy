from flask import render_template, redirect, Blueprint, request, url_for, send_from_directory
from flask_login import login_user, logout_user, login_required, current_user
from . import db
from .models import Blog, Author
from random import shuffle

view = Blueprint('view',__name__)


@view.route('/')
def home():
    blog_posts = Blog.query.all()
    shuffle(blog_posts)
    if current_user.is_authenticated:
        return render_template('home.html',loggedin=True,blog_posts=blog_posts,current_user=current_user)
    return render_template('home.html',blog_posts=blog_posts)


@view.route('/create',methods=["GET","POST"])
@login_required
def create():
    if request.method == "POST":
        data = request.get_json()
        content = data['content']
        if content != "" and content != " ":
            new_blog = Blog(content=content,author_id=current_user.id)
            db.session.add(new_blog)
            db.session.commit()
    return render_template('create.html')
@view.route('/profile/<int:author_id>')
@login_required
def profile(author_id):
    author_id = int(author_id)
    if current_user.id != author_id:
        return "Not authorized to View that profile", 401
    author = Author.query.filter_by(id=author_id).first()
    author_blogs = author.blog
    for blog in author_blogs:
        print(blog.content)
    return render_template('profile.html',author_name=author.username,blogs=author_blogs,picture=author.picture)

@view.route('/delete/<int:blogid>')
@login_required
def delete(blogid):
    blogid = int(blogid)
    blog = Blog.query.filter_by(id=blogid).first()
    if blog.author.id != current_user.id:
        return "Not authorized to delete", 401
    if blog:
        db.session.delete(blog)
        db.session.commit()
        return redirect(url_for('view.home'))
    return redirect(url_for('view.home'))

@view.route('/images/<filename>')
def send_images(filename):
    print(filename)
    return send_from_directory("assests/user_profile_picture",filename)

@view.route('/upload', methods=['GET','POST'])
def upload_images():
    if request.method == "POST":
        file = request.files['profile_pic']
        if file.filename != "":
            current_user.picture = file.filename
            db.session.commit()
            file.save(f"website/assests/user_profile_picture/{file.filename}")

    return redirect(url_for('view.profile',author_id=f"{current_user.id}"))
