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
from models import FavoriteModel,QuestionModel,UserFavoriteQuestionModel
from decorators import login_required
from logger import logger1

bp = Blueprint("collect",__name__,url_prefix="/collect")


@bp.route("/add/", methods=["POST","GET"])
@login_required
def add(): # add assessment
    user_id = S.get("user_id")
    form_results = request.form # get data from form
    favorite_name = form_results.get("favorite_name")

    # check if all imformation is filled
    if favorite_name == "" :
        flash("Please fill the information!")
        return redirect("/")
    favorite = session.query(FavoriteModel.name).filter(FavoriteModel.name==favorite_name).first()

    if(favorite != None):
        flash("Favorite category already exits! ")
        questions = QuestionModel.query.order_by(db.text("-create_time")).all()
        favorite = FavoriteModel.query.all()
        return redirect("/")
    favorite_model = FavoriteModel(name=favorite_name,num_content=0,author_id=user_id)
    db.session.add(favorite_model)
    db.session.commit()
    info = "user id" + str(user_id) + " add favorite " + favorite_name
    logger1.log(msg=info, level=20)
    questions = QuestionModel.query.order_by(db.text("-create_time")).all()
    favorite = db.session.query(FavoriteModel).filter(FavoriteModel.author_id == user_id).all()
    return redirect("/")

@bp.route("/add_1/", methods=["POST"])
@login_required
def add_1(): # add assessment
    user_id = S.get("user_id")
    form_results = request.form # get data from form
    favorite_name = form_results.get("favorite_name")

    # check if all imformation is filled
    if favorite_name == "" :
        flash("Please fill the information!")
        return redirect("/mine/mine/see_my_collection")
    favorite = session.query(FavoriteModel).all()
    maps = []
    for data in favorite:
        maps.append([data.name,data.author_id])
    print(maps)
    print(favorite_name,user_id)

    if [favorite_name,user_id] in maps:
        flash("Favorite category already exits! ")
        return redirect("/mine/mine/see_my_collection")

    favorite_model = FavoriteModel(name=favorite_name,num_content=0,author_id=user_id)
    db.session.add(favorite_model)
    db.session.commit()
    info = "user id" + str(user_id) + " add favorite " + favorite_name
    logger1.log(msg=info, level=20)
    favorite = session.query(FavoriteModel).all()
    maps = []
    for data in favorite:
        maps.append([data.name, data.author_id])
    print(maps)
    return redirect("/mine/mine/see_my_collection")

@bp.route("/collect/<path:path>", methods=["POST","GET"])
@login_required
def collect(path): # add collect item
    user_id = S.get("user_id")
    q_id = int(path[:path.index("*")])
    f_id = int(path[path.index("*")+1:])
    favorite = FavoriteModel.query.filter(FavoriteModel.id == f_id).first()
    question = QuestionModel.query.filter(QuestionModel.id == q_id).first()
    if request.method == 'POST':
        if question not in favorite.qs:
            favorite.qs.append(question)
            f_org = favorite.num_content + 1
            db.session.query(FavoriteModel).filter(FavoriteModel.id == f_id).update({'num_content': f_org})
            db.session.commit()
            user_favorite_model = UserFavoriteQuestionModel(question_id=q_id, favorite_id=f_id, user_id=user_id)
            db.session.add(user_favorite_model)
            db.session.query(UserFavoriteQuestionModel).filter(UserFavoriteQuestionModel.question_id == q_id,
                                                               UserFavoriteQuestionModel.favorite_id == f_id,
                                                               UserFavoriteQuestionModel.user_id == None).delete()
            print("post")
            db.session.commit()
        else:
            favorite.qs.remove(question)
            f_org = favorite.num_content - 1
            db.session.query(FavoriteModel).filter(FavoriteModel.id == f_id).update({'num_content': max(f_org,0)})
            db.session.query(UserFavoriteQuestionModel).filter(UserFavoriteQuestionModel.question_id==q_id, UserFavoriteQuestionModel.favorite_id==f_id,UserFavoriteQuestionModel.user_id==user_id).delete()
            db.session.commit()
        return redirect("/")
    else:
        if question not in favorite.qs:
            favorite.qs.append(question)
            f_org = favorite.num_content + 1
            db.session.query(FavoriteModel).filter(FavoriteModel.id == f_id).update({'num_content': f_org})
            db.session.commit()
            user_favorite_model = UserFavoriteQuestionModel(question_id=q_id, favorite_id=f_id, user_id=user_id)
            db.session.add(user_favorite_model)
            db.session.query(UserFavoriteQuestionModel).filter(UserFavoriteQuestionModel.question_id == q_id,
                                                               UserFavoriteQuestionModel.favorite_id == f_id,
                                                               UserFavoriteQuestionModel.user_id == None).delete()
            db.session.commit()
        else:
            favorite.qs.remove(question)
            f_org = favorite.num_content - 1
            db.session.query(FavoriteModel).filter(FavoriteModel.id == f_id).update({'num_content': max(f_org,0)})
            db.session.query(UserFavoriteQuestionModel).filter(UserFavoriteQuestionModel.question_id==q_id, UserFavoriteQuestionModel.favorite_id==f_id,UserFavoriteQuestionModel.user_id==user_id).delete()
            db.session.commit()
        return redirect("/")

