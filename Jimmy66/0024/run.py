import os
from flask import Flask, render_template, session, redirect, url_for, flash ,abort
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required
from flask.ext.sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)


class Todo(db.Model):
    __tablename__ = 'todo'
    id = db.Column(db.Integer, primary_key=True)
    mission = db.Column(db.String(64))
    status = db.Column(db.Integer)

    def __repr__(self):
        return '<Todo %r>' % self.mission


class NameForm(Form):
    mission = TextAreaField('Add a mission here', validators=[Required()])
    submit = SubmitField('Submit')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

#just for test
@app.route('/123')
def test():
    abort(500)

@app.route('/delete/<int:id>')
def delete_mission(id):
    delete_mission = Todo.query.get(id)
    db.session.delete(delete_mission)
    #return render_template('index.html', form=form, array=array)
    return redirect(url_for('index'))

@app.route('/done/<int:id>')
def complete_mission(id):
    complete_mission = Todo.query.get(id)
    complete_mission.status = 1
    db.session.add(complete_mission)
    return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        record = Todo(mission=form.mission.data,status=0)
        db.session.add(record)
        return redirect(url_for('index'))
    array = Todo.query.all()
    if not array:
        flash('Here is no mission, you can add some.')
    return render_template('index.html', form=form, array=array)


if __name__ == '__main__':
    db.create_all()
    manager.run()
