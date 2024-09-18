from . import login_manager, db
from flask import Blueprint, render_template, url_for, request, redirect, flash
from .models import Author
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError


def get_user_details(form_type):
    details = {}
    if form_type == "sign":
       details['username']  = request.form.get('username').strip()
       details['first']  = request.form.get('first_name').strip()
       details['last']  = request.form.get('last_name').strip()
       details['email']  = request.form.get('email').strip()
       details['password']  = request.form.get('password').strip()
       return details

    elif form_type == "login":
        details['username'] = request.form.get('username')
        details['password'] = request.form.get('password')
        return details

def log_in_user(details):
    author = Author.query.filter_by(username=details['username']).first()
    if author:
        if check_password_hash(author.password,details['password']):
            login_user(author)
            return True
        else:
            flash('incorrect password','error')
    else:
        flash('No user found','error')
    return False

auth = Blueprint('auth',__name__)

@login_manager.user_loader
def load_user(user_id):
    return Author.query.get(user_id)

@auth.route('/login',methods=["GET","POST"])
def login():
    if request.method == "POST":
        details = get_user_details('login')
        complete = True
        for value in details.values():
            if value == " " or value == "":
                complete = False
        if complete:
            if log_in_user(details):
                return redirect(url_for('view.home'))
        else:
            flash('details not enough','error')

    return render_template('login.html')

@auth.route('/sign',methods=["GET","POST"])
def sign():
    if request.method == "POST":
        details = get_user_details('sign')
        complete = True 
        for value in details.values():
            if value == " " or value == "":
                complete = False
        if complete:
            try:
                file = request.files['profile_pic']  
                if file.filename == "":
                    file.filename = "profile.png"
                file.save(f"website/assests/user_profile_picture/{file.filename}")
                new_author = Author(username=details['username'],
                                    first_name=details['first'],
                                    last_name=details['last'],
                                    email=details['email'],
                                    password=generate_password_hash(details['password']),
                                    picture=file.filename)
                db.session.add(new_author)
                db.session.commit()
                return redirect(url_for('auth.login'))
            except IntegrityError:
                flash('User already exist','error')
                db.session.rollback()
        else:
            flash('details not enough!','error')

    return render_template('sign.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
