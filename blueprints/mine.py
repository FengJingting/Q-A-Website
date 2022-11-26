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


bp = Blueprint("mine",__name__,url_prefix="/mine")

