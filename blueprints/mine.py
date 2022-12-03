from flask import (
    Blueprint,
    render_template,
    request,
    session,
    flash,
    redirect
)
from flask import session as S
from exts import db,session
from models import FavoriteModel,QuestionModel,UserModel
from decorators import login_required
from werkzeug.security import generate_password_hash,check_password_hash

bp = Blueprint("mine",__name__,url_prefix="/mine")
@bp.route("/mine/see_my_collection")
@login_required
def see_my_collection():
    user_id = S.get("user_id")
    favorite = db.session.query(FavoriteModel).filter(UserModel.id == user_id).all()
    return render_template("mine.html",favorite=favorite)

@bp.route("/mine/see_my_collection_item/<int:id>")
@login_required
def see_my_collection_item(id):
    user_id = S.get("user_id")
    favorites = db.session.query(FavoriteModel).filter(FavoriteModel.id ==id).first()
    q_fav = favorites.qs
    print(q_fav)
    return render_template("favorite_item.html",qs=q_fav)

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
    questions = db.session.query(QuestionModel).filter(UserModel.id == user_id).all()
    return render_template("my_question.html",questions=questions)

@bp.route("/change_password/", methods=["POST"])
@login_required
def change_password(): # add assessment
    user_id = S.get("user_id")
    user = db.session.query(UserModel).filter(UserModel.id == user_id).first()
    form_results = request.form # get data from form
    initial_password = form_results.get("initial_password")
    new_password = form_results.get("new_password")
    # check if all imformation is filled
    if check_password_hash(user.password,initial_password):
        flash("Wrong password!")
        info = db.session.query(UserModel).filter(UserModel.id == user_id).first()
        return render_template("personal_info.html",info=info)
    hash_password = generate_password_hash(new_password)
    db.session.query(UserModel).filter(UserModel.id == user_id).update({'password': hash_password})
    db.session.commit()
    info = db.session.query(UserModel).filter(UserModel.id == user_id).first()
    return render_template("personal_info.html",info=info)

@bp.route("/add/", methods=["POST"])
@login_required
def add(): # add assessment
    user_id = S.get("user_id")
    print(user_id)
    form_results = request.form # get data from form
    favorite_name = form_results.get("favorite_name")

    # check if all imformation is filled
    if favorite_name == "" :
        flash("Please fill the information!")
        return ("nothing")
    favorite_model = FavoriteModel(name=favorite_name,num_content=0,author_id=user_id)
    db.session.add(favorite_model)
    db.session.commit()
    return("nothing")

@bp.route("/collect/", methods=["POST","GET"])
@login_required
def collect(): # add assessment
    # user_id = S.get("user_id")
    print("ok")
    f_id = request.json.get("f_id")
    q_id = request.json.get("q_id")
    favorite = FavoriteModel.query.filter(FavoriteModel.id == f_id).first()
    question = QuestionModel.query.filter(QuestionModel.id == q_id).first()
    print(favorite.qs)
    if question not in favorite.qs:
        favorite.qs.append(question)
        f_org = favorite.num_content + 1
        q_org = question.iscollect + 1
        db.session.query(FavoriteModel).filter(FavoriteModel.id == f_id).update({'num_content': f_org})
        db.session.query(QuestionModel).filter(QuestionModel.id == q_id).update({'iscollect': q_org})
        db.session.commit()
    else:
        favorite.qs.remove(question)
        f_org = favorite.num_content - 1
        q_org = question.iscollect - 1
        db.session.query(FavoriteModel).filter(FavoriteModel.id == f_id).update({'num_content': max(f_org,0)})
        db.session.query(QuestionModel).filter(QuestionModel.id == q_id).update({'iscollect': max(q_org,0)})
        db.session.commit()
    return("nothing")

