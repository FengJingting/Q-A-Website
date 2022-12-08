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

bp = Blueprint("qa",__name__,url_prefix="/")

@bp.route("/")
def index():
    user_id = S.get("user_id")
    questions = QuestionModel.query.order_by(db.text("-create_time")).all()
    favorite = db.session.query(FavoriteModel).filter(FavoriteModel.author_id == user_id).all()
    user_id = S.get("user_id")
    result_q = QuestionModel.query.join(UserFavoriteQuestionModel).filter(UserFavoriteQuestionModel.user_id ==user_id ).all()
    print(result_q)
    return render_template("index.html",questions=questions,favorite=favorite,fav_q = result_q)


@bp.route("/question/public",methods=['GET','POST'])
@login_required
def public_question():
    # user_id_1 = request.cookie.get("user_id")
    # app.logger.info('user id is %s', user_id_1)
    # 判断是否登录，如果没有登录，跳转到登录页面
    if request.method == 'GET':
        return render_template("public_question.html")
    else:
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            question = QuestionModel(title=title,content=content,author=g.user)
            db.session.add(question)
            db.session.commit()
            return redirect("/")
        else:
            flash("标题或内容格式错误！")
            return redirect(url_for("qa.public_question"))


@bp.route("/question/<int:question_id>")
def question_detail(question_id):
    question = QuestionModel.query.get(question_id)
    return render_template("detail.html", question=question)


@bp.route("/answer/<int:question_id>",methods=['POST'])
@login_required
def answer(question_id):
    form = AnswerForm(request.form)
    if form.validate():
        content = form.content.data
        answer_model = AnswerModel(content=content,author=g.user,question_id=question_id)
        db.session.add(answer_model)
        db.session.commit()
        return redirect(url_for("qa.question_detail",question_id=question_id))
    else:
        flash("Wrong format！")
        return redirect(url_for("qa.question_detail", question_id=question_id))


@bp.route("/search")
def search():
    q = request.args.get("q")
    questions =QuestionModel.query.filter(or_(QuestionModel.title.contains(q),QuestionModel.content.contains(q))).order_by(db.text("-create_time"))
    print(questions)
    return render_template("index.html",questions=questions)