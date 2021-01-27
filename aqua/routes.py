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
    pro = Products.query.all()
    aqua = Aquaproducts.query.all()
    return render_template("index.html",pro = pro, aqua=aqua)

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

@app.route('/ucontact',methods=['GET', 'POST'])
def ucontact():
    if request.method=='POST':
        name= request.form['name']
        email= request.form['email']
        phone= request.form['phone']
        subject= request.form['subject']
        message= request.form['message']
        print(message)
        new1 = Feedback(name=name,email=email,phone=phone,subject=subject,message=message,usertype='user')
        try:
            db.session.add(new1)
            db.session.commit()
            return redirect('/uindex')

        except:
            return 'not add'  
    return render_template("ucontact.html")

@app.route('/aqcontact',methods=['GET', 'POST'])
def aqcontact():
    if request.method=='POST':
        name= request.form['name']
        email= request.form['email']
        phone= request.form['phone']
        subject= request.form['subject']
        message= request.form['message']
        print(message)
        new1 = Feedback(name=name,email=email,phone=phone,subject=subject,message=message,usertype='aqua')
        try:
            db.session.add(new1)
            db.session.commit()
            return redirect('/aqindex')

        except:
            return 'not add'  
    return render_template("aqcontact.html")

@app.route('/scontact',methods=['GET', 'POST'])
def scontact():
    if request.method=='POST':
        name= request.form['name']
        email= request.form['email']
        phone= request.form['phone']
        subject= request.form['subject']
        message= request.form['message']
        print(message)
        new1 = Feedback(name=name,email=email,phone=phone,subject=subject,message=message,usertype='staff')
        try:
            db.session.add(new1)
            db.session.commit()
            return redirect('/sindex')

        except:
            return 'not add'  
    return render_template("scontact.html")

@app.route('/gcontact',methods=['GET', 'POST'])
def gcontact():
    if request.method=='POST':
        name= request.form['name']
        email= request.form['email']
        phone= request.form['phone']
        subject= request.form['subject']
        message= request.form['message']
        print(message)
        new1 = Feedback(name=name,email=email,phone=phone,subject=subject,message=message,usertype='guide')
        try:
            db.session.add(new1)
            db.session.commit()
            return redirect('/gindex')

        except:
            return 'not add'  
    return render_template("gcontact.html")

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
    aqua = Aquaproducts.query.all()
    return render_template("uindex.html",pro=pro, aqua=aqua)

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
        def randomString(stringLength=5):
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
        def randomString(stringLength=5):
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
    cart= Cart.query.filter_by(owner=current_user.id).all()
    aqcart = Aquacart.query.filter_by(owner=current_user.id).all()
    return render_template("ucartview.html",cart=cart, aqcart=aqcart)

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

@app.route('/uaqadd/<int:id>',methods=['GET','POST'])
def uaqadd(id):
    cart = Aquacart.query.get_or_404(id)
    if request.method=='POST':
        no= request.form['no']
        print(no)
        price = int(cart.price)*int(no)
        new1 = Aquabuyproduct(aqowner=cart.aqowner,name=cart.name,brand=cart.brand,price=price,image=cart.image,qnty=no,bowner=current_user.id)
        try:
            db.session.add(new1)
            db.session.commit()
            return redirect('/uaqcartbuy/'+str(new1.id))

        except:
            return 'not add'  

@app.route('/ucartadd/<int:id>')
def ucartadd(id):
    cart = Products.query.get_or_404(id)
    new = Cart(name = cart.name,brand= cart.brand,price=cart.price,image=cart.image,owner=current_user.id)
    db.session.add(new)
    db.session.commit()
    return redirect('/uindex')

@app.route('/uaqcartadd/<int:id>')
def uaqcartadd(id):
    cart = Aquaproducts.query.get_or_404(id)
    new = Aquacart(aqowner=cart.aqowner,name = cart.name,brand= cart.brand,price=cart.price,image=cart.image,owner=current_user.id)
    db.session.add(new)
    db.session.commit()
    return redirect('/uindex')

@app.route('/ucartremove/<int:id>')
def ucartremove(id):
    delete = Cart.query.get_or_404(id)
    try:
        db.session.delete(delete)
        db.session.commit()
        return redirect('/ucartview')
    except:
        return 'can not delete'

@app.route('/uaqcartremove/<int:id>')
def uaqcartremove(id):
    delete = Aquacart.query.get_or_404(id)
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

@app.route('/uaqcartbuy/<int:id>',methods=['GET','POST'])
def uaqcartbuy(id):
    buy = Aquabuyproduct.query.get_or_404(id)
    if request.method=='POST':
        name= request.form['name']
        mobile= request.form['mobile']
        address= request.form['address']
        buy.delname=name
        buy.delmobile=mobile
        buy.deladdress = address
        db.session.commit()
        return redirect('/uaqpayment/'+str(buy.id))
    return render_template("uaqcartbuy.html",buy=buy)

@app.route('/upayment/<int:id>')
def upayment(id):
    buy = Buyproduct.query.get_or_404(id)
    return render_template("upayment.html",buy=buy)

@app.route('/uaqpayment/<int:id>')
def uaqpayment(id):
    buy = Aquabuyproduct.query.get_or_404(id)
    return render_template("uaqpayment.html",buy=buy)


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

@app.route('/aqcredit/<int:id>',methods=['GET','POST'])
def aqcredit(id):
    buy1 = Aquabuyproduct.query.get_or_404(id)
    if request.method=='POST':
        name= request.form['name']
        number= request.form['number']
        cvv= request.form['cvv']
        date= request.form['date']
        buy1.status = 'complete'
        buy1.payment = 'creditcard'
        new1 = Aquacredit(aqowner=buy1.aqowner,name=name,card=number,cvv=cvv,expdate=date,buyid=current_user.id)
        try:
            db.session.add(new1)
            db.session.commit()
            sendmail()
            return redirect('/sucess')

        except:
            return 'not add'  
    return render_template("uaqpayment.html")

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

@app.route('/aqcod/<int:id>',methods=['GET','POST'])
def aqcod(id):
    buy2 = Aquabuyproduct.query.get_or_404(id)
    if request.method=='POST':
        buy2.status = 'complete'
        buy2.payment = 'Cod'
        try:
            db.session.commit()
            sendmail()
            return redirect('/sucess')

        except:
            return 'not add'  
    return render_template("uaqpayment.html")


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
    pdt = Aquabuyproduct.query.filter_by(bowner=current_user.id).all()
    return render_template("ubuyproduct.html",cart=cart,pdt=pdt)

@app.route('/abuyproduct')
def abuyproduct():
    buy = Buyproduct.query.filter_by(status='complete',staff='no').all()
    user = Login.query.filter_by(usertype='staff').all()
    return render_template("abuyproduct.html",buy=buy,user=user)

@app.route('/staffadd/<int:id>',methods=['GET','POST'])
def staffadd(id):
    buy = Buyproduct.query.filter_by(status='complete',staff='no').all()
    user = Login.query.filter_by(usertype='staff').all()
    buy2=Buyproduct.query.get_or_404(id)
    if request.method=='POST':
        buy2.staff = 'add'
        buy2.staffid = request.form['staff']
        staf = Login.query.get_or_404(buy2.staffid)
        buy2.staffname = staf.username
        try:
            db.session.commit()
            return redirect('/admin')

        except:
            return 'not add' 
    return render_template("abuyproduct.html",buy=buy,user=user)

@app.route('/aboughtproduct')
def aboughtproduct():
    buy = Buyproduct.query.filter_by(status='complete',staff='add').all()
    return render_template("aboughtproduct.html",buy=buy)

@app.route('/spendingpdts')
def spendingpdts():
    buy = Buyproduct.query.filter_by(status='complete',staff='add',staffid=current_user.id).all()
    return render_template("spendingpdts.html",buy=buy)

@app.route('/saqpendingpdts')
def saqpendingpdts():
    buy = Aquabuyproduct.query.filter_by(status='complete',staff='add',staffid=current_user.id).all()
    return render_template("saqpendingpdts.html",buy=buy)

@app.route('/sdel/<int:id>',methods=['GET','POST'])
def sdel(id):
    buy = Buyproduct.query.filter_by(status='complete',staff='add',staffid=current_user.id).all()
    buy2=Buyproduct.query.get_or_404(id)
    if request.method=='POST':
        buy2.delivery = request.form['del']
        try:
            db.session.commit()
            return redirect('/sindex')

        except:
            return 'not add' 
    return render_template("spendingpdts.html",buy=buy)

@app.route('/saqdel/<int:id>',methods=['GET','POST'])
def saqdel(id):
    buy = Aquabuyproduct.query.filter_by(status='complete',staff='add',staffid=current_user.id).all()
    buy2=Aquabuyproduct.query.get_or_404(id)
    if request.method=='POST':
        buy2.delivery = request.form['del']
        try:
            db.session.commit()
            return redirect('/saqpendingpdts')

        except:
            return 'not add' 
    return render_template("saqpendingpdts.html",buy=buy)


@app.route('/aqproductadd',methods=['POST','GET'])
def aqproductadd():
    form=Product()
    if form.validate_on_submit():
        if form.pic.data:
            pic = save_picture(form.pic.data)
            view = pic
        gallery = Aquaproducts(aqowner= current_user.id,name=form.name.data,brand=form.brand.data,price=form.price.data,image=view )
       
        db.session.add(gallery)
        db.session.commit()
        return redirect('/aqindex')
            
    return render_template('aqproductadd.html',form=form)

@app.route('/aqproductview')
def aqproductview():
    pdt = Aquaproducts.query.filter_by(aqowner=current_user.id).all()
    return render_template("aqproductview.html",pdt=pdt)

@app.route('/aqproductupdate/<int:id>', methods=['GET', 'POST'])
def aqproductupdate(id):
    material = Aquaproducts.query.get_or_404(id)
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
        return redirect('/aqproductview')
    elif request.method == 'GET':
        form.name.data = material.name
        form.brand.data = material.brand
        form.price.data = material.price
    image_file = url_for('static', filename='pics/' + material.image)
    return render_template('aqproductupdate.html',form=form, material=material)

@app.route('/aqpdtremove/<int:id>')
def aqpdtremove(id):
    delete = Aquaproducts.query.get_or_404(id)
    try:
        db.session.delete(delete)
        db.session.commit()
        return redirect('/aqproductview')
    except:
        return 'can not delete'

@app.route('/aaqproductview')
def aaqproductview():
    pdt = Aquaproducts.query.all()
    return render_template("aaqproductview.html",pdt=pdt)



@app.route('/aaqbuyproduct')
def aaqbuyproduct():
    buy = Aquabuyproduct.query.filter_by(status='complete',staff='no').all()
    user = Login.query.filter_by(usertype='staff').all()
    return render_template("aaqbuyproduct.html",buy=buy,user=user)

@app.route('/staffaddaq/<int:id>',methods=['GET','POST'])
def staffaddaq(id):
    buy = Aquabuyproduct.query.filter_by(status='complete',staff='no').all()
    user = Login.query.filter_by(usertype='staff').all()
    buy2=Aquabuyproduct.query.get_or_404(id)
    if request.method=='POST':
        buy2.staff = 'add'
        buy2.staffid = request.form['staff']
        staf = Login.query.get_or_404(buy2.staffid)
        buy2.staffname = staf.username
        try:
            db.session.commit()
            return redirect('/admin')

        except:
            return 'not add' 
    return render_template("aaqbuyproduct.html",buy=buy,user=user)

@app.route('/aaqboughtproduct')
def aaqboughtproduct():
    buy = Aquabuyproduct.query.filter_by(status='complete',staff='add').all()
    return render_template("aaqboughtproduct.html",buy=buy)

@app.route('/aqboughtproduct')
def aqboughtproduct():
    buy = Aquabuyproduct.query.filter_by(status='complete',staff='add',aqowner = current_user.id).all()
    return render_template("aqboughtproduct.html",buy=buy)


@app.route('/apfeed')
def apfeed():
    feedback1=Feedback.query.filter_by(usertype='public').all()
    return render_template("apfeed.html",feedback=feedback1)

@app.route('/asfeed')
def asfeed():
    feedback1=Feedback.query.filter_by(usertype='staff').all()
    return render_template("asfeed.html",feedback=feedback1)

@app.route('/aufeed')
def aufeed():
    feedback1=Feedback.query.filter_by(usertype='user').all()
    return render_template("aufeed.html",feedback=feedback1)

@app.route('/aaqfeed')
def aaqfeed():
    feedback1=Feedback.query.filter_by(usertype='aqua').all()
    return render_template("aaqfeed.html",feedback=feedback1)

@app.route('/agfeed')
def agfeed():
    feedback1=Feedback.query.filter_by(usertype='guide').all()
    return render_template("agfeed.html",feedback=feedback1)

@app.route('/gclassadd',methods=['POST','GET'])
def gclassadd():
    form=Agentclass()
    if form.validate_on_submit():
        link =form.link.data
        new=link.split('//')[1].lstrip().split('/')[1]
        gallery = Classvideo(owner= current_user.id,desc=form.name.data,video=new)
        print(new)
        db.session.add(gallery)
        db.session.commit()
        return redirect('/gindex')
            
    return render_template('gclassadd.html',form=form)

@app.route('/gclassview')
def gclassview():
    guide = Classvideo.query.all()
    return render_template("gclassview.html",guide=guide)


@app.route('/gclassdelete/<int:id>')
def gclassdelete(id):
    delete = Classvideo.query.get_or_404(id)
    try:
        db.session.delete(delete)
        db.session.commit()
        return redirect('/gclassview')
    except:
        return 'can not delete'

@app.route('/uclassview')
def uclassview():
    guide = Classvideo.query.all()
    return render_template("uclassview.html",guide=guide)

@app.route('/uprofile/<int:id>',methods=['GET','POST'])
def uprofile(id):
    form = Profile()
    login = Login.query.get_or_404(id)
    if form.validate_on_submit():
        if form.pic.data:
            picture_file = save_picture(form.pic.data)
            login.image_file = picture_file
        login.username = form.username.data
        login.address = form.address.data
        login.phone = form.phone.data
        login.email = form.email.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect('/uindex')
    elif request.method == 'GET':
        form.username.data = login.username
        form.address.data = login.address
        form.phone.data = login.phone
        form.email.data = login.email
        form.pic.data = login.image_file
    image_file = url_for('static', filename='pics/' + login.image_file)
    return render_template("uprofile.html",form=form)

@app.route('/sprofile/<int:id>',methods=['GET','POST'])
def sprofile(id):
    form = Profile()
    login = Login.query.get_or_404(id)
    if form.validate_on_submit():
        if form.pic.data:
            picture_file = save_picture(form.pic.data)
            login.image_file = picture_file
        login.username = form.username.data
        login.address = form.address.data
        login.phone = form.phone.data
        login.email = form.email.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect('/sindex')
    elif request.method == 'GET':
        form.username.data = login.username
        form.address.data = login.address
        form.phone.data = login.phone
        form.email.data = login.email
        form.pic.data = login.image_file
    image_file = url_for('static', filename='pics/' + login.image_file)
    return render_template("sprofile.html",form=form)

@app.route('/aqprofile/<int:id>',methods=['GET','POST'])
def aqprofile(id):
    form = Profile()
    login = Login.query.get_or_404(id)
    if form.validate_on_submit():
        if form.pic.data:
            picture_file = save_picture(form.pic.data)
            login.image_file = picture_file
        login.username = form.username.data
        login.address = form.address.data
        login.phone = form.phone.data
        login.email = form.email.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect('/aqindex')
    elif request.method == 'GET':
        form.username.data = login.username
        form.address.data = login.address
        form.phone.data = login.phone
        form.email.data = login.email
        form.pic.data = login.image_file
    image_file = url_for('static', filename='pics/' + login.image_file)
    return render_template("aqprofile.html",form=form)

@app.route('/gprofile/<int:id>',methods=['GET','POST'])
def gprofile(id):
    form = Profile()
    login = Login.query.get_or_404(id)
    if form.validate_on_submit():
        if form.pic.data:
            picture_file = save_picture(form.pic.data)
            login.image_file = picture_file
        login.username = form.username.data
        login.address = form.address.data
        login.phone = form.phone.data
        login.email = form.email.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect('/gindex')
    elif request.method == 'GET':
        form.username.data = login.username
        form.address.data = login.address
        form.phone.data = login.phone
        form.email.data = login.email
        form.pic.data = login.image_file
    image_file = url_for('static', filename='pics/' + login.image_file)
    return render_template("gprofile.html",form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect('/')


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('resettoken', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@app.route("/resetrequest", methods=['GET', 'POST'])
def resetrequest():
    form = RequestResetForm()
    if form.validate_on_submit():
        user = Login.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect('/login')
    return render_template('resetrequest.html', title='Reset Password', form=form)



@app.route("/resetpassword/<token>", methods=['GET', 'POST'])
def resettoken(token):
    user = Login.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect('/resetrequest')
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect('/login')
    return render_template('resetpassword.html', title='Reset Password', form=form)


@app.route('/imageadd',methods=['POST','GET'])
def imageadd():
    form=Imageadd()

    if form.validate_on_submit():

        if form.pic.data:
            pic_file = save_picture(form.pic.data)
            view = pic_file
        print(view)  
    
        gallery = Gallery(name=form.name.data,img=view )
       
        db.session.add(gallery)
        db.session.commit()
        print(gallery)
        flash('image added')
        return redirect('/viewimage')
            
    return render_template('imageadd.html',form=form)

@app.route('/viewimage')
def viewimage():
    gallery=Gallery.query.all()
    return render_template('viewimage.html',gallery=gallery)

@app.route("/view/<int:id>", methods=['GET', 'POST'])
def update_post(id):
    gallery = Gallery.query.get_or_404(id)
    form = Imageupdate()
    if form.validate_on_submit():
        if form.pic.data:
            picture_file = save_picture(form.pic.data)
            gallery.img = picture_file
        gallery.name = form.name.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect('/viewimage')
    elif request.method == 'GET':
        form.name.data = gallery.name
    image_file = url_for('static', filename='pics/' + gallery.img)
    return render_template('galleryupdate.html',form=form)

@app.route("/view/<int:id>/delete")
def deleteimage(id):
    gallery =Gallery.query.get_or_404(id)
    db.session.delete(gallery)
    db.session.commit()
    flash('image has been deleted!', 'success')
    return redirect('/viewimage')


@app.route('/gallery')
def gallery():
    gal = Gallery.query.all()
    return render_template('gallery.html',gal=gal)