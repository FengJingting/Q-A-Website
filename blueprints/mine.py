from flask import (
    Blueprint,
    render_template,
    request,
    session,
    flash,
    redirect,
    jsonify
)
import json
from flask import session as S
from exts import db,session
from models import FavoriteModel,QuestionModel,UserModel,UserFavoriteQuestionModel,AnswerModel
from decorators import login_required
from werkzeug.security import generate_password_hash,check_password_hash
from logger import logger1
from .forms import ModifypasswordForm,ModifyusernameForm,ModifyEmailForm
bp = Blueprint("mine",__name__,url_prefix="/mine")


@bp.route("/mine/see_my_collection")
@login_required
def see_my_collection():
    user_id = S.get("user_id")
    favorite = db.session.query(FavoriteModel).filter(FavoriteModel.author_id == user_id).all()
    return render_template("mine.html",favorite=favorite)

@bp.route("/mine/delete_f/<int:id>",methods=["GET","POST"])
@login_required
def delete_f(id):
        user_id = S.get("user_id")
        try:
            f_id = id
            db.session.query(UserFavoriteQuestionModel).filter(UserFavoriteQuestionModel.favorite_id == f_id).delete()
            db.session.commit()
            db.session.query(FavoriteModel).filter(FavoriteModel.id == f_id).delete()
            db.session.commit()
            info = "user id" + str(user_id) + " delete favorite id" + str(f_id)
            logger1.log(msg=info, level=20)
        except Exception as e:
            info = "user id" + str(user_id) + " fail to delete favorite id" + str(f_id) +"with expection"+e
            logger1.error(msg=info,level=40)
            db.session.rollback()
        user_id = S.get("user_id")
        favorite = db.session.query(FavoriteModel).filter(FavoriteModel.author_id == user_id).all()
        print(favorite)

        return render_template("mine.html", favorite=favorite)

@bp.route("/mine/see_my_collection_item/<int:id>")
@login_required
def see_my_collection_item(id):
    favorites = db.session.query(FavoriteModel).filter(FavoriteModel.id ==id).first()
    q_fav = favorites.qs
    return render_template("favorite_item.html",qs=q_fav,favorites = favorites)

@bp.route("/mine/see_my_info")
@login_required
def see_my_info():
    user_id = S.get("user_id")
    info = db.session.query(UserModel).filter(UserModel.id == user_id).first()
    return render_template("personal_info.html",info=info)

@bp.route("/mine/see_my_question")
@login_required
def see_my_question():
    user_id = S.get("user_id")
    questions = db.session.query(QuestionModel).filter(QuestionModel.author_id == user_id).all()
    return render_template("my_question.html",questions=questions)

@bp.route("/mine/delete_q/<int:id>",methods=["GET","POST"])
@login_required
def delete_q(id):
    user_id = S.get("user_id")
    try:
        q_id = id
        db.session.query(AnswerModel).filter(AnswerModel.question_id == q_id).delete()
        db.session.query(UserFavoriteQuestionModel).filter(UserFavoriteQuestionModel.question_id == q_id).delete()
        db.session.query(QuestionModel).filter(QuestionModel.id == q_id).delete()
        db.session.commit()
        info = "user id" + str(user_id) + " delete question id" + str(q_id)
        logger1.log(msg=info, level=20)
    except Exception as e:
        info = "user id" + str(user_id) + " fail to delete question id" + str(q_id) + "with expection" + e
        logger1.error(msg=info, level=40)
        db.session.rollback()

    user_id = S.get("user_id")
    questions = db.session.query(QuestionModel).filter(QuestionModel.author_id == user_id).all()
    return render_template("my_question.html", questions=questions)

@bp.route("/mine/edit_q/<int:id>",methods=["GET","POST"])
@login_required
def edit_q(id):
    user_id = S.get("user_id")
    form_results = request.form  # get data from form
    title = form_results.get("title")
    content = form_results.get("content")
    city = form_results.get("city")
    geolocation = form_results.get("geolocation")
    if title != "":
        if 3<=len(title) and len(title)<=200:
            db.session.query(QuestionModel).filter(QuestionModel.id == id).update({'title': title})
            info = "user id" + str(user_id) + " modify title in question id" + id
            logger1.log(msg=info, level=20)
        else:
            flash("content should between 3-200 letter!")

    if content != "" :
        if 5<=len(content):
            db.session.query(QuestionModel).filter(QuestionModel.id == id).update({'content': content})
            info = "user id" + str(user_id) + " modify content in question id" + id
            logger1.log(msg=info, level=20)
        else:
            flash("content should be larger than 5 letter!")
    if city:
        db.session.query(QuestionModel).filter(QuestionModel.id == id).update({'city': city})
        info = "user id" + str(user_id) + " modify city in question id" + id
        logger1.log(msg=info, level=20)
    if geolocation:
        db.session.query(QuestionModel).filter(QuestionModel.id == id).update({'city': geolocation})
        info = "user id" + str(user_id) + " modify geolocation in question id" + id
        logger1.log(msg=info, level=20)
    db.session.commit()
    return redirect("/mine/mine/see_my_question")

@bp.route("/change_password/", methods=["POST"])
@login_required
def change_password(): # add assessment
    user_id = S.get("user_id")
    user = db.session.query(UserModel).filter(UserModel.id == user_id).first()
    form = ModifypasswordForm(request.form)
    print(form.validate())
    if form.validate():# get data from form
        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        # check if all imformation is filled
        if check_password_hash(user.password,old_password):
            flash("Old Password does not match!")
            return redirect("/mine/mine/see_my_info")

        hash_password = generate_password_hash(new_password)
        db.session.query(UserModel).filter(UserModel.id == user_id).update({'password': hash_password})
        db.session.commit()
        ip = request.remote_addr
        info = "user id" + str(user.id) + " successfully change password in ip" + ip
        logger1.log(msg=info, level=20)
        flash("Success !")
    else:
        flash("Wrong format!")
    return redirect("/mine/mine/see_my_info")


@bp.route("/change_email/", methods=["POST"])
@login_required
def change_email(): # add assessment
    user_id = S.get("user_id")
    user = db.session.query(UserModel).filter(UserModel.id == user_id).first()
    form = ModifyEmailForm(request.form)
    if form.validate():  # get data from form
        new_email = request.form.get("new_email")
        db.session.query(UserModel).filter(UserModel.id == user_id).update({'email': new_email})
        db.session.commit()
        ip = request.remote_addr
        info = "user id" + str(user.id) + " successfully change email in ip" + ip
        logger1.log(msg=info, level=20)
        flash("Success !")
    return redirect("/mine/mine/see_my_info")

@bp.route("/change_username/", methods=["POST"])
@login_required
def change_username(): # add assessment
    user_id = S.get("user_id")
    user = db.session.query(UserModel).filter(UserModel.id == user_id).first()
    form = ModifyusernameForm(request.form)
    print(form.validate())
    if form.validate():  # get data from form
        new_username = request.form.get("new_username")
        db.session.query(UserModel).filter(UserModel.id == user_id).update({'username': new_username})
        db.session.commit()
        ip = request.remote_addr
        info = "user id" + str(user.id) + " successfully change username in ip" + ip
        logger1.log(msg=info, level=20)
        flash("Success !")
    else:
        flash("Wrong format!")
    return redirect("/mine/mine/see_my_info")