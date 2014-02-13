from flask import Flask, render_template, Response, flash, \
redirect, url_for, request
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView
from adminviews import GalleryUserView, GalleryPresentationView, GalleryVoteView
from models import db, User, Presentation, Vote
from authentication import requires_auth
from flask.ext.login import LoginManager, login_user, login_required, \
logout_user, current_user
from forms import LoginForm, AddPresentationForm
from config import SECRET, MAXIMUM_NUMBER_VOTES, PASSWORD_SUBMISSION

app = Flask(__name__)
lm = LoginManager()
app.config.from_object(__name__)
app.config.from_object('config')

app.secret_key = 'this is my secret key'

def create_app(db):
    with app.app_context():
        db.init_app(app)
        db.create_all()

create_app(db)
admin = Admin(app)
lm.init_app(app)
lm.login_view = "login"
admin.add_view(GalleryVoteView(db.session))
admin.add_view(GalleryUserView(db.session))
admin.add_view(GalleryPresentationView(db.session))

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route("/submit-presentation", methods=["POST", "GET"])
def submit_presentation():
	form = AddPresentationForm(request.form)
	if request.method == 'POST' and form.validate():
		if form.password.data == PASSWORD_SUBMISSION:
			add_presentation(form.url.data, form.owner.data)
			if current_user.is_authenticated():
				return render_template("home.html", presentations=get_presentations_and_is_selected(), 
	        		current_user=current_user)
			else:
				return redirect(url_for('login'))
	return render_template("submit-presentation.html", form=form)


@app.route("/results", methods=["GET"])
@login_required
def show_results():
	return render_template("results.html")

def add_presentation(url, owner):
	presentation = Presentation(url, owner)
	db.session.add(presentation)
	db.session.commit()


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
    	if (form.password.data == SECRET):
    		user = get_user(form.email.data)
    		message_welcome = "Welcome back!"
    		if user is None:
    			message_welcome = "Welcome!"
    			user = add_user(form.email.data)
        	login_user(user, True)
        	flash(message_welcome, 'info')
        	return render_template("home.html", presentations=get_presentations_and_is_selected(), 
        		current_user=current_user)
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

def get_vote(id_presentation, id_user):
	return Vote.query.filter_by(presentation=id_presentation, user=id_user).first()

def get_votes_from_current_user():
	return Vote.query.filter_by(user=current_user.id)

@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
	return render_template("home.html", presentations=get_presentations_and_is_selected(), 
		current_user=current_user)


def get_presentations_and_is_selected():
	presentations = Presentation.query.all()
	votes = get_votes_from_current_user()

	results = []

	for p in presentations:
		found = False
		for v in votes:
			if v.vote_presentation.id == p.id:
				found = True
		results.append((p, found))
	return results


@app.route('/vote/<int:id_presentation>', methods=['POST'])
@login_required
def vote(id_presentation):
	response = ({'OK'}, 200)
	vote = get_vote(id_presentation, current_user.id)
	if vote is None :
		is_allowed_to_vote = check_number_votes_for_current_user() < MAXIMUM_NUMBER_VOTES
		if is_allowed_to_vote:
			vote = Vote(id_presentation, current_user.id)
			db.session.add(vote)
		else:
			response = not_allowed_to_vote_response()
	else:
		db.session.delete(vote)
	db.session.commit()
	resp = Response(response[0], status=response[1], mimetype='application/json')
	return resp

def not_allowed_to_vote_response():
	return ({'maximum-number-of-votes-reached'}, 401)

def check_number_votes_for_current_user():
	nb_votes = Vote.query.filter_by(user=current_user.id).count()
	return nb_votes

if __name__ == '__main__':
	app.run(debug=True)