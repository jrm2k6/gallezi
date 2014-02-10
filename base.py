from flask import Flask, render_template, Response, flash, redirect, url_for, request
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView
from adminviews import GalleryUserView, GalleryPresentationView
from models import db, User, Presentation, Vote
from authentication import requires_auth
from flask.ext.login import LoginManager, login_user, login_required, \
logout_user
from forms import LoginForm
import config

app = Flask(__name__)
lm = LoginManager()
app.config.from_object(__name__)
app.config.from_object('config')

# just because of the session
app.secret_key = 'this is my secret key'

def create_app(db):
    with app.app_context():
        db.init_app(app)
        db.create_all()

create_app(db)
admin = Admin(app)
lm.init_app(app)
lm.login_view = "login"
admin.add_view(ModelView(Vote, db.session))
admin.add_view(GalleryUserView(db.session))
admin.add_view(GalleryPresentationView(db.session))

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
    	if (form.password.data == config.SECRET):
    		user = get_user(form.email.data) 
    		if user is None:
    			user = add_user(form.email.data)
        	login_user(user)
        	flash("Logged in successfully.")
        	return render_template("home.html", presentations=Presentation.query.all())
    	else:
    		flash(u'Invalid password provided', 'error')
    return render_template("login.html", form=form)

@app.route("/logout", methods=["GET"])
@login_required
def logout():
	logout_user()
	return redirect(url_for("login"))

def get_user(email):
	return User.query.filter_by(email=email).first()

def add_user(email):
	user = User(email)
	db.session.add(user)
	db.session.commit()
	return user

@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
	return render_template("home.html", presentations=Presentation.query.all())

@app.route('/vote/<int:id_presentation>/<int:id_user>', methods=['POST'])
def vote(id_presentation, id_user):
	vote = Vote(id_presentation, id_user)
	db.session.add(vote)
	db.session.commit()
	resp = Response({}, status=200, mimetype='application/json')
	return resp

if __name__ == '__main__':
	app.run(debug=True)