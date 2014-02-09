from flask import Flask, render_template, Response
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView
from adminviews import GalleryUserView, GalleryPresentationView
from models import db, User, Presentation, Vote


app = Flask(__name__)
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
admin.add_view(ModelView(Vote, db.session))
admin.add_view(GalleryUserView(db.session))
admin.add_view(GalleryPresentationView(db.session))

@app.route('/')
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