from flask import Flask, render_template, request, redirect,  flash, abort, url_for
from aqua import app,db,bcrypt,mail
from aqua.models import *
from aqua.forms import *
from random import randint
import os
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image
from flask_mail import Message

@app.route('/')
def  index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/playout')
def playout():
    return render_template("playout.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/contact',methods=['GET', 'POST'])
def contact():
    if request.method=='POST':
        name= request.form['name']
        email= request.form['email']
        phone= request.form['phone']
        subject= request.form['subject']
        message= request.form['message']
        print(message)
        new1 = Feedback(name=name,email=email,phone=phone,subject=subject,message=message,usertype='public')
        try:
            db.session.add(new1)
            db.session.commit()
            return redirect('/')

        except:
            return 'not add'  
    return render_template("contact.html")


@app.route('/registeruser',methods=['GET','POST'])
def registeruser():
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new = Login(username= form.username.data, email=form.email.data, password=hashed_password,phone = form.phone.data,usertype= 'user' )
        db.session.add(new)
        db.session.commit()
        flash('Your account has been created! waiting for approval', 'success')
        return redirect('/')
    return render_template("registeruser.html",form=form)


@app.route('/registeraqua',methods=['GET','POST'])
def registeraqua():
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new = Login(username= form.username.data, email=form.email.data, password=hashed_password,phone = form.phone.data,usertype= 'user' )
        db.session.add(new)
        db.session.commit()
        flash('Your account has been created! waiting for approval', 'success')
        return redirect('/')
    return render_template("registeraqua.html",form=form)