from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    flash,
    url_for,
    g
)
from flask import current_app as app
from flask import session as S
from exts import db,session
from .forms import QuestionForm,AnswerForm
from models import QuestionModel,AnswerModel,FavoriteModel,UserFavoriteQuestionModel,UserModel
from sqlalchemy import or_
from decorators import login_required
from logger import logger1

bp = Blueprint("qa",__name__,url_prefix="/")

@bp.route("/")
def index():
    ifdamin = 0
    user_id = S.get("user_id")
    if user_id == 9:
        ifdamin = 1
    questions = QuestionModel.query.order_by(db.text("-create_time")).all()
    favorite = db.session.query(FavoriteModel).filter(FavoriteModel.author_id == user_id).all()
    user_id = S.get("user_id")
    result_q = QuestionModel.query.join(UserFavoriteQuestionModel).filter(UserFavoriteQuestionModel.user_id ==user_id ).all()
    return render_template("index.html",questions=questions,favorite=favorite,fav_q = result_q,ifdamin = ifdamin)


@bp.route("/question/public",methods=['GET','POST'])
@login_required
def public_question():
    user_id = S.get("user_id")
    if request.method == 'GET':
        return render_template("public_question.html")
    else:
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            city = request.form.get("city")
            geo = request.form.get("geolocation")
            if city == "":
                city = "Secret"
            if geo == "":
                geo = "Secret"
            question = QuestionModel(title=title,content=content,author=g.user,city=city,geolocation=geo)
            db.session.add(question)
            db.session.commit()
            info = "user id" + str(user_id) + " public question" + title
            logger1.log(msg=info, level=20)
            return redirect("/")
        else:
            flash("Wrong format！")
            return redirect(url_for("qa.public_question"))


@bp.route("/question/<int:question_id>")
def question_detail(question_id):
    user_id = S.get("user_id")
    question = QuestionModel.query.get(question_id)
    return render_template("detail.html", question=question,user=user_id)

@bp.route("/delete_a/<int:id>")
def delete_a(id):
    user_id = S.get("user_id")
    try:
        db.session.query(AnswerModel).filter(AnswerModel.id == id).delete()
        db.session.commit()
        info = "user id" + str(user_id) + " delete answer id" + str(id)
        logger1.log(msg=info, level=20)
    except Exception as e:
        info = "user id" + str(user_id) + " fail to delete answer id" + str(id) + "with expection" + e
        logger1.error(msg=info, level=40)
        db.session.rollback()

    return redirect("/")

@bp.route("/answer/<int:question_id>",methods=['POST'])
@login_required
def answer(question_id):
    user_id = S.get("user_id")
    form = AnswerForm(request.form)
    if form.validate():
        content = form.content.data
        answer_model = AnswerModel(content=content,author=g.user,question_id=question_id)
        db.session.add(answer_model)
        db.session.commit()
        info = "user id" + str(user_id) + " give an answer to question "+ str(question_id)
        logger1.log(msg=info, level=20)
        return redirect(url_for("qa.question_detail",question_id=question_id))
    else:
        flash("Wrong format！")
        return redirect(url_for("qa.question_detail", question_id=question_id))


@bp.route("/search")
def search():
    user_id = S.get("user_id")
    q = request.args.get("q")
    print(q)
    questions =QuestionModel.query.filter(or_(QuestionModel.title.contains(q),QuestionModel.content.contains(q))).order_by(db.text("-create_time"))
    print(questions)
    favorite = db.session.query(FavoriteModel).filter(FavoriteModel.author_id == user_id).all()
    user_id = S.get("user_id")
    result_q = QuestionModel.query.join(UserFavoriteQuestionModel).filter(
        UserFavoriteQuestionModel.user_id == user_id).all()
    return render_template("index.html",questions=questions,favorite=favorite,fav_q = result_q)