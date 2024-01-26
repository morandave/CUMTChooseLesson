from flask import render_template, session, redirect, url_for, current_app
from .. import db
from ..models import User, Comment, Lesson
from ..email import send_email
from . import main, cache
from .forms import NameForm, CommentForm


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            if current_app.config['FLASKY_ADMIN']:
                send_email(current_app.config['FLASKY_ADMIN'], 'New User',
                           'mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('.index'))
    return render_template('index.html',
                           form=form, name=session.get('name'),
                           known=session.get('known', False))

@cache.cached(timeout=24*60*60)
@main.route('/<kind>', methods=['GET', 'POST'])
def view(kind):
    if(kind=='art'):
        kind = '艺术鉴赏类_美育类'
    elif(kind=='culture'):
        kind = '人文社科类'
    elif(kind=='innovation'):
        kind = '创新创业类'
    elif(kind=='science'):
        kind = '科学与技术类'
    else:
        kind = 'PE'
    lessons = Lesson.query.filter(Lesson.kind == kind).all()
    return render_template('kind.html',lessons=lessons)


@main.route('/art/<lesson>', methods=['GET', 'POST'])
def comment(lesson):
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,lesson_id=lesson)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('.comment',lesson=lesson))
    comments = Comment.query.filter_by(lesson_id=lesson).order_by(Comment.timestamp.desc()).all()
    return render_template('comment.html', form=form, comments=comments)


@main.route('/search/<lesson>', methods=['GET', 'POST'])
def search(lesson):
    lessons = Lesson.query.filter(Lesson.course.like('%' + lesson + '%')).all()
    return render_template('search.html',lessons=lessons)