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
bp = Blueprint("admin",__name__,url_prefix="/admin")

@bp.route("/")
@login_required
def index():
    users = UserModel.query.order_by(db.text("-join_time")).all()
    return render_template("administrator.html",users = users)

@bp.route("/delete/<int:id>",methods=["GET","POST"])
@login_required
def delete(id):
    ip = request.remote_addr
    try:
        u_id = id
        db.session.query(UserFavoriteQuestionModel).filter(UserFavoriteQuestionModel.user_id == u_id).delete()
        db.session.commit()
        db.session.query(FavoriteModel).filter(FavoriteModel.author_id == u_id).delete()
        db.session.commit()
        db.session.query(AnswerModel).filter(AnswerModel.author_id == u_id).delete()
        db.session.commit()
        db.session.query(QuestionModel).filter(QuestionModel.author_id == u_id).delete()
        db.session.commit()
        db.session.query(UserModel).filter(UserModel.id == u_id).delete()
        db.session.commit()
        info = "administrator delete user id " + str(u_id) + " successfully in ip"+ ip
        logger1.log(msg=info, level=20)
    except Exception as e:
        info = "administrator fail to delete user id" + str(u_id) +" with exception" + e + "in ip" + ip
        logger1.log(msg=info, level=40)
        logger1.error(msg=e)
        db.session.rollback()

    users = UserModel.query.order_by(db.text("-join_time")).all()
    return render_template("administrator.html", users=users)
