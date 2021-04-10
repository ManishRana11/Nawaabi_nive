from flask import Flask, render_template, request, flash, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import json
import math
from datetime import datetime

with open('config.json', 'r') as c:
    params = json.load(c)["params"]

local_server = True
app = Flask(__name__, template_folder='C:\\Users\\new\\Desktop\\Nawaabi_nive\\tempelate',
            static_folder='C:\\Users\\new\\Desktop\\Nawaabi_nive\\static')
app.secret_key = 'super-secret-key'
app.config['UPLOAD_FOLDER'] = params['upload_location']
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['gmail-user'],
    MAIL_PASSWORD=params['gmail-password']
)
mail = Mail(app)
if local_server:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db = SQLAlchemy(app)


class Contact(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    firstn = db.Column(db.String, nullable=False)
    lastn = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    msg = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=True)


class Desktop(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    homedesk = db.Column(db.String, nullable=True)
    recipedesk = db.Column(db.String, nullable=True)
    aboutdesk = db.Column(db.String, nullable=True)
    orderdesk = db.Column(db.String, nullable=True)
    contactdesk = db.Column(db.String, nullable=True)
    admindesk = db.Column(db.String, nullable=True)
    date = db.Column(db.String, nullable=True)


class Footer(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    gallery = db.Column(db.String, nullable=True)


class Quote(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    src = db.Column(db.String, nullable=True)
    pre = db.Column(db.String, nullable=False)


class About(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    profile = db.Column(db.String, nullable=True)
    about = db.Column(db.String, nullable=False)


class Items(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String, nullable=False)
    detail = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    pic = db.Column(db.String, nullable=True)
    date = db.Column(db.String, nullable=True)


class Recipe(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    ingredient = db.Column(db.String, nullable=False)
    process = db.Column(db.String, nullable=False)
    img = db.Column(db.String, nullable=True)
    yt = db.Column(db.String, nullable=True)
    date = db.Column(db.String, nullable=True)


@app.route("/", methods=['GET', 'POST'])
def home():
    recipe = Recipe.query.filter_by().limit(6).all()
    footer = Footer.query.filter_by().limit(5).all()
    quote = Quote.query.filter_by().limit(1).all()
    desktop = Desktop.query.filter_by().limit(1).all()
    if request.method == 'POST':
        flash("Message Sent Successfully")
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        message = request.form.get('message')
        entry = Contact(firstn=firstname, lastn=lastname, msg=message, date=datetime.now(), email=email)
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New message from ' + firstname + " " + lastname,
                          sender=email,
                          recipients=[params['gmail-user']],
                          body=message + "\n" + email
                          )
        return redirect(url_for('home'))
    return render_template('home.html', params=params, desktop=desktop, recipe=recipe, footer=footer, quote=quote)


@app.route("/recipe")
def recipe():
    recipe = Recipe.query.filter_by().all()
    footer = Footer.query.filter_by().limit(5).all()
    desktop = Desktop.query.filter_by().limit(1).all()
    last = math.ceil(len(recipe)/int(params['no_of_recipes']))
    # [0: params['no_of_posts']]
    # posts = posts[]
    page = request.args.get('page')
    if not str(page).isnumeric():
        page = 1
    page = int(page)
    recipe = recipe[(page-1)*int(params['no_of_recipes']): (page-1)*int(params['no_of_recipes']) +
                                                           int(params['no_of_recipes'])]
    # Pagination Logic
    # First
    if page == 1:
        prev = "#"
        next = "/recipe?page=" + str(page+1)
    elif page == last:
        prev = "/recipe?page=" + str(page - 1)
        next = "#"
    else:
        prev = "/recipe?page=" + str(page - 1)
        next = "/recipe?page=" + str(page + 1)
    return render_template('recipes.html', desktop=desktop, params=params, recipe=recipe, prev=prev, next=next, footer=footer)


@app.route("/about")
def about():
    footer = Footer.query.filter_by().limit(5).all()
    desktop = Desktop.query.filter_by().limit(1).all()
    about = About.query.filter_by().limit(1).all()
    return render_template('about.html', params=params, desktop=desktop, footer=footer, about=about)


@app.route("/order")
def order():
    footer = Footer.query.filter_by().limit(5).all()
    desktop = Desktop.query.filter_by().limit(1).all()
    items = Items.query.filter_by().all()
    return render_template('order.html', params=params, desktop=desktop, footer=footer, items=items)


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    footer = Footer.query.filter_by().limit(5).all()
    desktop = Desktop.query.filter_by().limit(1).all()
    if request.method == 'POST':
        flash("Message Sent Successfully")
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        message = request.form.get('message')
        entry = Contact(firstn=firstname, lastn=lastname, msg=message, date=datetime.now(), email=email)
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New message from ' + firstname + " " + lastname,
                          sender=email,
                          recipients=[params['gmail-user']],
                          body=message + "\n" + email
                          )
        return redirect(url_for('contact'))
    return render_template('contact.html', params=params, desktop=desktop, footer=footer)


@app.route("/recipe/<string:recipe_name>", methods=['GET'])
def post_route(recipe_name):
    recipe = Recipe.query.filter_by(name=recipe_name).first()
    about = About.query.filter_by().limit(1).all()
    footer = Footer.query.filter_by().limit(5).all()
    desktop = Desktop.query.filter_by().limit(1).all()
    return render_template('making.html', params=params, desktop=desktop, recipe=recipe, footer=footer, about=about)


@app.route("/order/<string:items_item>", methods=['GET'])
def item_route(items_item):
    items = Items.query.filter_by(item=items_item).first()
    about = About.query.filter_by().limit(1).all()
    footer = Footer.query.filter_by().limit(5).all()
    desktop = Desktop.query.filter_by().limit(1).all()
    return render_template('item.html', params=params, desktop=desktop, recipe=recipe, footer=footer, about=about, items=items)


@app.route("/admin", methods=['GET', 'POST'])
def admin():
    if 'user' in session and session['user'] == params['admin_user']:
        recipe = Recipe.query.filter_by().all()
        footer = Footer.query.filter_by().limit(5).all()
        desktop = Desktop.query.filter_by().limit(1).all()
        last = math.ceil(len(recipe) / int(params['no_of_recipes']))
        # [0: params['no_of_posts']]
        # posts = posts[]
        page = request.args.get('page')
        if not str(page).isnumeric():
            page = 1
        page = int(page)
        recipe = recipe[(page - 1) * int(params['no_of_recipes']): (page - 1) * int(params['no_of_recipes']) +
                                                                   int(params['no_of_recipes'])]
        # Pagination Logic
        # First
        if page == 1:
            prev = "#"
            next = "/recipe?page=" + str(page + 1)
        elif page == last:
            prev = "/recipe?page=" + str(page - 1)
            next = "#"
        else:
            prev = "/recipe?page=" + str(page - 1)
            next = "/recipe?page=" + str(page + 1)
        return render_template('adminrecipe.html', params=params, prev=prev, next=next, recipe=recipe, desktop=desktop, footer=footer)

    if request.method == 'POST':
        username = request.form.get('uname')
        userpass = request.form.get('pass')
        if username == params['admin_user'] and userpass == params['admin_password']:
            # set the session variable
            session['user'] = username
            recipe = Recipe.query.filter_by().all()
            footer = Footer.query.filter_by().limit(5).all()
            desktop = Desktop.query.filter_by().limit(1).all()
            last = math.ceil(len(recipe) / int(params['no_of_recipes']))
            # [0: params['no_of_posts']]
            # posts = posts[]
            page = request.args.get('page')
            if not str(page).isnumeric():
                page = 1
            page = int(page)
            recipe = recipe[(page - 1) * int(params['no_of_recipes']): (page - 1) * int(params['no_of_recipes']) +
                                                                       int(params['no_of_recipes'])]
            # Pagination Logic
            # First
            if page == 1:
                prev = "#"
                next = "/recipe?page=" + str(page + 1)
            elif page == last:
                prev = "/recipe?page=" + str(page - 1)
                next = "#"
            else:
                prev = "/recipe?page=" + str(page - 1)
                next = "/recipe?page=" + str(page + 1)
            return render_template('adminrecipe.html', params=params, prev=prev, next=next, desktop=desktop, recipe=recipe, footer=footer)
        else:
            flash("Wrong User Credentials")
            return redirect(url_for('admin'))

    return render_template('admin.html', params=params)


@app.route("/adminhome", methods=['GET', 'POST'])
def adminhome():
    recipe = Recipe.query.filter_by().limit(6).all()
    footer = Footer.query.filter_by().limit(5).all()
    desktop = Desktop.query.filter_by().limit(1).all()
    quote = Quote.query.filter_by().limit(1).all()
    if request.method == 'POST':
        flash("Message Sent Successfully")
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        message = request.form.get('message')
        entry = Contact(firstn=firstname, lastn=lastname, msg=message, date=datetime.now(), email=email)
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New message from ' + firstname + " " + lastname,
                          sender=email,
                          recipients=[params['gmail-user']],
                          body=message + "\n" + email
                          )
        return redirect(url_for('adminhome'))
    return render_template('adminhome.html', params=params, desktop=desktop, recipe=recipe, footer=footer, quote=quote)


@app.route("/adminrecipe")
def adminrecipe():
    recipe = Recipe.query.filter_by().all()
    footer = Footer.query.filter_by().limit(5).all()
    desktop = Desktop.query.filter_by().limit(1).all()
    last = math.ceil(len(recipe)/int(params['no_of_recipes']))
    # [0: params['no_of_posts']]
    # posts = posts[]
    page = request.args.get('page')
    if not str(page).isnumeric():
        page = 1
    page = int(page)
    recipe = recipe[(page-1)*int(params['no_of_recipes']): (page-1)*int(params['no_of_recipes']) +
                                                           int(params['no_of_recipes'])]
    # Pagination Logic
    # First
    if page == 1:
        prev = "#"
        next = "/adminrecipe?page=" + str(page+1)
    elif page == last:
        prev = "/adminrecipe?page=" + str(page - 1)
        next = "#"
    else:
        prev = "/adminrecipe?page=" + str(page - 1)
        next = "/adminrecipe?page=" + str(page + 1)
    return render_template('adminrecipe.html', params=params, desktop=desktop, recipe=recipe, prev=prev, next=next, footer=footer)


@app.route("/adminrecipe/<string:adminrecipe_name>", methods=['GET'])
def adminpost_route(adminrecipe_name):
    recipe = Recipe.query.filter_by(name=adminrecipe_name).first()
    about = About.query.filter_by().limit(1).all()
    footer = Footer.query.filter_by().limit(5).all()
    desktop = Desktop.query.filter_by().limit(1).all()
    return render_template('adminmaking.html', params=params, desktop=desktop, recipe=recipe, footer=footer, about=about)


@app.route("/adminorder/<string:adminitems_item>", methods=['GET'])
def adminitem_route(adminitems_item):
    items = Items.query.filter_by(item=adminitems_item).first()
    about = About.query.filter_by().limit(1).all()
    footer = Footer.query.filter_by().limit(5).all()
    desktop = Desktop.query.filter_by().limit(1).all()
    return render_template('adminitem.html', params=params, desktop=desktop, recipe=recipe, footer=footer, about=about, items=items)


@app.route("/adminabout")
def adminabout():
    footer = Footer.query.filter_by().limit(5).all()
    desktop = Desktop.query.filter_by().limit(1).all()
    about = About.query.filter_by().limit(1).all()
    return render_template('adminabout.html', desktop=desktop, params=params, footer=footer, about=about)


@app.route("/adminorder")
def adminorder():
    footer = Footer.query.filter_by().limit(5).all()
    desktop = Desktop.query.filter_by().limit(1).all()
    items = Items.query.filter_by().all()
    return render_template('adminorder.html', params=params, desktop=desktop, footer=footer, items=items)


@app.route("/admincontact", methods=['GET', 'POST'])
def admincontact():
    footer = Footer.query.filter_by().limit(5).all()
    desktop = Desktop.query.filter_by().limit(1).all()
    if request.method == 'POST':
        flash("Message Sent Successfully")
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        message = request.form.get('message')
        entry = Contact(firstn=firstname, lastn=lastname, msg=message, date=datetime.now(), email=email)
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New message from ' + firstname + " " + lastname,
                          sender=email,
                          recipients=[params['gmail-user']],
                          body=message + "\n" + email
                          )
        return redirect(url_for('admincontact'))
    return render_template('admincontact.html', params=params, desktop=desktop, footer=footer)


@app.route("/logout")
def logout():
    session.pop('user')
    return redirect('/admin')


@app.route("/recipedelete/<string:sno>", methods=['GET', 'POST'])
def recipedelete(sno):
    if 'user' in session and session['user'] == params['admin_user']:
        recipe = Recipe.query.filter_by(sno=sno).first()
        db.session.delete(recipe)
        db.session.commit()
    return redirect('/adminrecipe')


@app.route("/orderdelete/<string:sno>", methods=['GET', 'POST'])
def orderdelete(sno):
    if 'user' in session and session['user'] == params['admin_user']:
        item = Items.query.filter_by(sno=sno).first()
        db.session.delete(item)
        db.session.commit()
    return redirect('/adminorder')


@app.route("/recipeedit/<string:sno>", methods=['GET', 'POST'])
def recipeedit(sno):
    if 'user' in session and session['user'] == params['admin_user']:
        if request.method == 'POST':
            name = request.form.get('name')
            ingredient = request.form.get('ingredient')
            yt = request.form.get('yt')
            process = request.form.get('process')
            img = request.form.get('img')
            date = datetime.now()

            if sno == '0':
                recipe = Recipe(name=name, yt=yt, process=process, ingredient=ingredient, img=img, date=date)
                db.session.add(recipe)
                db.session.commit()
            else:
                recipe = Recipe.query.filter_by(sno=sno).first()
                recipe.name = name
                recipe.ingredient = ingredient
                recipe.process = process
                recipe.yt = yt
                recipe.img = img
                recipe.date = date
                db.session.commit()
                return redirect('/recipeedit/'+sno)
        recipe = Recipe.query.filter_by(sno=sno).first()
        footer = Footer.query.filter_by().limit(5).all()
        desktop = Desktop.query.filter_by().limit(1).all()
        return render_template('recipeedit.html', params=params, desktop=desktop, recipe=recipe, sno=sno, footer=footer)


@app.route("/desktopedit/<string:sno>", methods=['GET', 'POST'])
def desktopedit(sno):
    if 'user' in session and session['user'] == params['admin_user']:
        if request.method == 'POST':
            homedesk = request.form.get('homedesk')
            recipedesk = request.form.get('recipedesk')
            aboutdesk = request.form.get('aboutdesk')
            orderdesk = request.form.get('orderdesk')
            contactdesk = request.form.get('contactdesk')
            admindesk = request.form.get('admindesk')
            date = datetime.now()

            if sno == '0':
                desktop = Desktop(homedesk=homedesk, recipedesk=recipedesk, aboutdesk=aboutdesk, orderdesk=orderdesk,
                                  contactdesk=contactdesk, admindesk=admindesk, date=date)
                db.session.add(desktop)
                db.session.commit()
            else:
                desktop = Desktop.query.filter_by(sno=sno).limit(1).first()
                desktop.homedesk = homedesk
                desktop.recipedesk = recipedesk
                desktop.aboutdesk = aboutdesk
                desktop.orderdesk = orderdesk
                desktop.contactdesk = contactdesk
                desktop.admindesk = admindesk
                db.session.commit()
                return redirect('/desktopedit/'+sno)
        desktop = Desktop.query.filter_by(sno=sno).limit(1).first()
        footer = Footer.query.filter_by().limit(5).all()
        return render_template('recipeedit.html', params=params, desktop=desktop, sno=sno, footer=footer)


@app.route("/quoteedit/<string:sno>", methods=['GET', 'POST'])
def quoteedit(sno):
    if 'user' in session and session['user'] == params['admin_user']:
        if request.method == 'POST':
            src = request.form.get('src')
            date = datetime.now()

            if sno == '0':
                quote = Quote(src=src, date=date)
                db.session.add(quote)
                db.session.commit()
            else:
                quote = Quote.query.filter_by(sno=sno).limit(1).first()
                quote.src = src
                db.session.commit()
                return redirect('/quoteedit/'+sno)
        quote = Quote.query.filter_by(sno=sno).limit(1).first()
        footer = Footer.query.filter_by().limit(5).all()
        return render_template('quoteedit.html', params=params, quote=quote, sno=sno, footer=footer)


@app.route("/aboutedit/<string:sno>", methods=['GET', 'POST'])
def aboutedit(sno):
    if 'user' in session and session['user'] == params['admin_user']:
        if request.method == 'POST':
            profile = request.form.get('profile')
            date = datetime.now()

            if sno == '0':
                about = About(profile=profile, date=date)
                db.session.add(about)
                db.session.commit()
            else:
                about = About.query.filter_by(sno=sno).limit(1).first()
                about.profile = profile
                about.date = date
                db.session.commit()
                return redirect('/aboutedit/'+sno)
        about = About.query.filter_by(sno=sno).limit(1).first()
        footer = Footer.query.filter_by().limit(5).all()
        desktop = Desktop.query.filter_by().limit(1).all()
        return render_template('aboutedit.html', params=params, about=about, desktop=desktop, sno=sno, footer=footer)


@app.route("/orderedit/<string:sno>", methods=['GET', 'POST'])
def orderedit(sno):
    if 'user' in session and session['user'] == params['admin_user']:
        if request.method == 'POST':
            item = request.form.get('item')
            price = request.form.get('price')
            detail = request.form.get('detail')
            pic = request.form.get('pic')
            date = datetime.now()

            if sno == '0':
                items = Items(item=item, detail=detail, price=price, pic=pic, date=date)
                db.session.add(items)
                db.session.commit()
            else:
                items = Items.query.filter_by(sno=sno).first()
                items.items = item
                items.price = price
                items.detail = detail
                items.pic = pic
                items.date = date
                db.session.commit()
                return redirect('/orderedit/'+sno)
        items = Items.query.filter_by(sno=sno).first()
        footer = Footer.query.filter_by().limit(5).all()
        desktop = Desktop.query.filter_by().limit(1).all()
        return render_template('orderedit.html', params=params, desktop=desktop, items=items, sno=sno, footer=footer)


app.run(debug=True)
