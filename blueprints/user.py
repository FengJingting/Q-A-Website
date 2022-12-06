from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    jsonify,
    session,
    flash,
)
from flask import current_app as app
from exts import mail,db
from flask_mail import Message
from models import EmailCaptchaModel,UserModel,FavoriteModel
import string
import random
from datetime import datetime
from .forms import RegisterForm,LoginForm
from werkzeug.security import generate_password_hash,check_password_hash

bp = Blueprint("user",__name__,url_prefix="/user")

@bp.route("/login",methods=['GET','POST'])
def login(): # check if the user can log in
    if request.method == 'GET':
        return render_template("login.html")
    else:
        form = LoginForm(request.form)
        print(form.email.data,form.password.data)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if user and check_password_hash(user.password,password):
                session['user_id'] = user.id
                app.logger.info('%s logged in successfully', user.username)
                return redirect("/")
            else:
                flash("Your email and Password doesn't match!")
                app.logger.info('%s failed to log in because of wrong password or email', user.username)
                return redirect(url_for("user.login"))
        else:
            flash("Invalid format of email or Password")
            return redirect(url_for("user.login"))

@bp.route("/register",methods=['GET','POST'])
def register():# check if the user can successfully register
    if request.method == 'GET':
        return render_template("register.html")
    else:
        form = RegisterForm(request.form)
        print(form.email.data)
        print(form.password.data)

        if form.validate():
            email = form.email.data
            username = form.username.data
            # check if email already exit
            user_model = UserModel.query.filter_by(email=email).first()
            user_name = UserModel.query.filter_by(username=username).first()
            if user_model:
                flash("Email already exits!")
                return redirect(url_for("user.register"))
            if user_name:
                flash("User Name already exits!")
                return redirect(url_for("user.register"))

            username = form.username.data
            password = form.password.data
            hash_password = generate_password_hash(password)
            user = UserModel(email=email, username=username, password=hash_password)
            db.session.add(user)
            db.session.commit()
            user_id = db.session.query(UserModel).filter(UserModel.username == username).first()
            favorite_model = FavoriteModel(name="default", num_content=0, author_id=user_id)
            db.session.add(favorite_model)
            db.session.commit()
            return redirect(url_for("user.login"))
        else:
            return redirect(url_for("user.register"))

@bp.route("/logout")
def logout():
    # clear data in session
    session.clear()
    return redirect(url_for('user.login'))

@bp.route("/captcha",methods=['POST'])
def get_captcha(): # get data in captcha
    email = request.form.get("email")
    letters = string.ascii_letters + string.digits
    captcha = "".join(random.sample(letters,4))
    if email:
        message = Message(
            subject="Welcome to register TodoList",
            recipients=[email],
            body=f"【TodoList】Your verification code is：{captcha}"
        )
        mail.send(message)
        captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
        if captcha_model:
            captcha_model.captcha = captcha
            captcha_model.create_time = datetime.now()
            db.session.commit()
        else:
            captcha_model = EmailCaptchaModel(email=email,captcha=captcha)
            db.session.add(captcha_model)
            db.session.commit()
        print("captcha:",captcha)
        # success
        return jsonify({"code": 200})
    else:
        # error
        flash("Please input Email first!")
        return jsonify({"code": 400,"message": "No Input Email！"})