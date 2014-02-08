from flask import Flask, render_template
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView
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
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Presentation, db.session))
admin.add_view(ModelView(Vote, db.session))

@app.route('/')
def home():
	return render_template("home.html", presentations=Presentation.query.all())


if __name__ == '__main__':
	app.run(debug=True)


# <iframe src="http://prezi.com/embed/wp41jvbp-gdv/?bgcolor=ffffff&amp;lock_to_path=0&amp;autoplay=0&amp;autohide_ctrls=0&amp;features=undefined&amp;disabled_features=undefined" width="550" height="400" frameBorder="0"></iframe>