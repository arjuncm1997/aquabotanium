from flask import Flask, render_template, request, redirect,  flash, abort, url_for
from aqua import app,db,bcrypt,mail
from aqua.models import *
from aqua.forms import *
from random import randint
import os
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image
from flask_mail import Message
import string
import random       
from random import randint    

@app.route('/')
def  index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/playout')
def playout():
    return render_template("playout.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Login.query.filter_by(email=form.email.data, usertype= 'aqua').first()
        user1 = Login.query.filter_by(email=form.email.data, usertype= 'user').first()
        user2 = Login.query.filter_by(email=form.email.data, usertype= 'admin').first()
        user3 = Login.query.filter_by(email=form.email.data, usertype= 'staff').first()
        user4 = Login.query.filter_by(email=form.email.data, usertype= 'guide').first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/aqindex')
        if user1 and bcrypt.check_password_hash(user1.password, form.password.data):
            login_user(user1, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/uindex')
        if user3 and bcrypt.check_password_hash(user3.password, form.password.data):
            login_user(user3, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/sindex')
        if user4 and bcrypt.check_password_hash(user4.password, form.password.data):
            login_user(user4, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/gindex')
        if user2 and user2.password== form.password.data:
            login_user(user2, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/admin')
        if user2 and bcrypt.check_password_hash(user2.password, form.password.data):
            login_user(user2, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/admin')

        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

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
        flash('Your account has been created! ', 'success')
        return redirect('/')
    return render_template("registeruser.html",form=form)


@app.route('/registeraqua',methods=['GET','POST'])
def registeraqua():
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new = Login(username= form.username.data, email=form.email.data, password=hashed_password,phone = form.phone.data,usertype= 'aqua' )
        db.session.add(new)
        db.session.commit()
        flash('Your account has been created! ', 'success')
        return redirect('/')
    return render_template("registeraqua.html",form=form)



@app.route('/uindex')
def uindex():
    pro = Products.query.all()
    return render_template("uindex.html",pro=pro)

@app.route('/sindex')
def sindex():
    return render_template("sindex.html")

@app.route('/gindex')
def gindex():
    return render_template("gindex.html")

@app.route('/aqindex')
def aqindex():
    return render_template("aqindex.html")


@app.route('/admin')
def admin():
    return render_template("admin.html")


@app.route('/aguideadd',methods=['GET','POST'])
def aguideadd():
    form=RegistrationguideForm()
    if form.validate_on_submit():
        def randomString(stringLength=10):
            letters = string.ascii_lowercase
            return ''.join(random.choice(letters) for i in range(stringLength))
        password =randomString()
        email = form.email.data
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new = Login(username= form.username.data, email=form.email.data, password=hashed_password,phone = form.phone.data,usertype= 'guide' )
        db.session.add(new)
        db.session.commit()
        sendemail(email,password)
        flash('Your account has been created! ', 'success')
        return redirect('/admin')
    return render_template("aguideadd.html",form=form)



def sendemail(email,password):
    msg = Message(' Aqua Botanium Registeration',
                  recipients=[email])
    msg.body = f'''  Your Password is, {password}  '''
    mail.send(msg)

@app.route('/aguideview')
def aguideview():
    guide = Login.query.filter_by(usertype='guide').all()
    return render_template("aguideview.html",guide=guide)


@app.route('/astaffadd',methods=['GET','POST'])
def astaffadd():
    form=RegistrationguideForm()
    if form.validate_on_submit():
        def randomString(stringLength=10):
            letters = string.ascii_lowercase
            return ''.join(random.choice(letters) for i in range(stringLength))
        password =randomString()
        email = form.email.data
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new = Login(username= form.username.data, email=form.email.data, password=hashed_password,phone = form.phone.data,usertype= 'staff' )
        db.session.add(new)
        db.session.commit()
        sendemail(email,password)
        flash('Your account has been created! ', 'success')
        return redirect('/admin')
    return render_template("astaffadd.html",form=form)

@app.route('/astaffview')
def astaffview():
    staff = Login.query.filter_by(usertype='staff').all()
    return render_template("astaffview.html",staff=staff)


@app.route('/aproductadd',methods=['POST','GET'])
def aproductadd():
    form=Product()
    view=" "
    print("hello0")
    if form.validate_on_submit():
        if form.pic.data:
            pic = save_picture(form.pic.data)
            view = pic
        print(view)  
    
        gallery = Products(name=form.name.data,brand=form.brand.data,price=form.price.data,image=view )
       
        db.session.add(gallery)
        db.session.commit()
        flash('image added')
        return redirect('/aproductview')
            
    return render_template('aproductadd.html',form=form)



@app.route('/aproductview')
def aproductview():
    material=Products.query.all()
    return render_template('aproductview.html',material=material)


@app.route('/aproductupdate/<int:id>', methods=['GET', 'POST'])
def aproductupdate(id):
    material = Products.query.get_or_404(id)
    form = Product()
    if form.validate_on_submit():
        if form.pic.data:
            picture_file = save_picture(form.pic.data)
            material.image = picture_file
        material.name = form.name.data
        material.brand = form.brand.data
        material.price = form.price.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect('/aproductview')
    elif request.method == 'GET':
        form.name.data = material.name
        form.brand.data = material.brand
        form.price.data = material.price
    image_file = url_for('static', filename='pics/' + material.image)
    return render_template('aproductupdate.html',form=form, material=material)

@app.route('/aproductdelete/<int:id>')
def aproductdelete(id):
    delete = Products.query.get_or_404(id)
    try:
        db.session.delete(delete)
        db.session.commit()
        return redirect('/aproductview')
    except:
        return 'can not delete'

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


def save_picture(form_picture):
    random_hex = random_with_N_digits(14)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = str(random_hex) + f_ext
    picture_path = os.path.join(app.root_path, 'static/pics', picture_fn)
    
    output_size = (500, 500)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn



@app.route('/uproducts')
def uproducts():
    return render_template("uproducts.html")


@app.route('/ucartview')
def ucartview():
    cart= Cart.query.all()
    return render_template("ucartview.html",cart=cart)

@app.route('/uadd/<int:id>',methods=['GET','POST'])
def uadd(id):
    cart = Cart.query.get_or_404(id)
    if request.method=='POST':
        no= request.form['no']
        print(no)
        price = int(cart.price)*int(no)
        new1 = Buyproduct(name=cart.name,brand=cart.brand,price=price,image=cart.image,qnty=no,bowner=current_user.id)
        try:
            db.session.add(new1)
            db.session.commit()
            return redirect('/ucartbuy/'+str(new1.id))

        except:
            return 'not add'  

@app.route('/ucartadd/<int:id>')
def ucartadd(id):
    cart = Products.query.get_or_404(id)
    new = Cart(name = cart.name,brand= cart.brand,price=cart.price,image=cart.image,owner=current_user.id)
    db.session.add(new)
    db.session.commit()
    return redirect('/uindex')
    return render_template("ucartadd.html")

@app.route('/ucartremove/<int:id>')
def ucartremove(id):
    delete = Cart.query.get_or_404(id)
    try:
        db.session.delete(delete)
        db.session.commit()
        return redirect('/ucartview')
    except:
        return 'can not delete'

@app.route('/ucartbuy/<int:id>',methods=['GET','POST'])
def ucartbuy(id):
    buy = Buyproduct.query.get_or_404(id)
    if request.method=='POST':
        name= request.form['name']
        mobile= request.form['mobile']
        address= request.form['address']
        buy.delname=name
        buy.delmobile=mobile
        buy.deladdress = address
        db.session.commit()
        return redirect('/upayment/'+str(buy.id))
    return render_template("ucartbuy.html",buy=buy)

@app.route('/upayment/<int:id>')
def upayment(id):
    buy = Buyproduct.query.get_or_404(id)
    return render_template("upayment.html",buy=buy)


@app.route('/credit/<int:id>',methods=['GET','POST'])
def credit(id):
    buy1 = Buyproduct.query.get_or_404(id)
    if request.method=='POST':
        name= request.form['name']
        number= request.form['number']
        cvv= request.form['cvv']
        date= request.form['date']
        buy1.status = 'complete'
        buy1.payment = 'creditcard'
        new1 = Credit(name=name,card=number,cvv=cvv,expdate=date,buyid=current_user.id)
        try:
            db.session.add(new1)
            db.session.commit()
            sendmail()
            return redirect('/sucess')

        except:
            return 'not add'  
    return render_template("upayment.html")

@app.route('/cod/<int:id>',methods=['GET','POST'])
def cod(id):
    buy2 = Buyproduct.query.get_or_404(id)
    if request.method=='POST':
        buy2.status = 'complete'
        buy2.payment = 'Cod'
        try:
            db.session.commit()
            sendmail()
            return redirect('/sucess')

        except:
            return 'not add'  
    return render_template("upayment.html")


@app.route('/sucess')
def sucess():
    return render_template("sucess.html")



def sendmail():
    msg = Message('successful',
                  recipients=[current_user.email])
    msg.body = f''' your transaction completed successfullyy '''
    mail.send(msg)


@app.route('/ubuyproduct')
def ubuyproduct():
    cart = Buyproduct.query.filter_by(bowner=current_user.id).all()
    return render_template("ubuyproduct.html",cart=cart)