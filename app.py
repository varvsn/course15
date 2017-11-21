# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import Engine
from sqlalchemy import event

#Enable or disable FK check
#@event.listens_for(Engine, "connect")
#def set_sqlite_pragma(dbapi_connection, connection_record):
#    cursor = dbapi_connection.cursor()
#    cursor.execute("PRAGMA foreign_keys=ON")
#    cursor.close()

import config as config

app = Flask(__name__, template_folder='templates')
app.url_map.strict_slashes = False  # Last slash problem
app.config.from_object(config)

db = SQLAlchemy(app)


@app.route('/course15', methods=['GET', 'POST'])
def main():
    from models import Post, Comment
    from forms import PostForm

    if request.method == 'GET':
        posts = Post.query.all()

        return render_template('home.html', posts=posts)

    if request.method == 'POST':
        form = PostForm(request.form)
        if form.validate():
            post = Post(**form.data)
            db.session.add(post)
            db.session.commit()
            flash('A very good Post number {} was added'.format(post.id))
            return render_template('flash_page.html'), 200
        else:
            flash('Something wrong! {}'.format(str(form.errors)))
            return render_template('flash_page.html'), 403


@app.route('/course15/add_comment/<int:post_id>', methods=['POST'])
def add_comment(post_id):
    from models import Comment
    from forms import CommentForm
    comment = CommentForm(request.form)
    #
    # if not Post.query.get(post_id):  # КАК СДЕЛАТЬ ВАЛИДАТОР ПО ЛЮДСКИ??
    #     flash('No such Post! Nothing to comment')
    #     return render_template('flash_page.html'), 403

    if comment.validate():
        comment = Comment(**comment.data)
        comment.post_id = post_id
        db.session.add(comment)
        db.session.commit()
        flash('A very good Comment was added for Post number {}'.format(comment.post_id))
        return render_template('flash_page.html'), 200
    else:
        flash('Something wrong! {}'.format(str(comment.errors)))
        return render_template('flash_page.html'), 403


@app.route('/course15/delete_all')
def del_all():
    db.session.query(Post).delete()
    db.session.query(Comment).delete()
    db.session.commit()
    flash('All data deleted')
    return render_template('flash_page.html'), 200


if __name__ == '__main__':


    from models import *
    db.create_all()
    # Running app:
    app.run('0.0.0.0', port=5001, threaded=True)
