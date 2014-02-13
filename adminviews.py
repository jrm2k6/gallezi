from flask.ext.admin.contrib.sqla import ModelView
from models import User, Presentation, Vote
from flask.ext.login import LoginManager, login_user, login_required, \
logout_user, current_user
from config import EMAIL_ADMINS


class GalleryUserView(ModelView):
    column_exclude_list = ['votes']
    form_excluded_columns = ['votes']

    def __init__(self, session, **kwargs):
        super(GalleryUserView, self).__init__(User, session, **kwargs)

    def is_accessible(self):
    	return current_user.is_authenticated() and current_user.email in EMAIL_ADMINS

class GalleryPresentationView(ModelView):
    column_exclude_list = ['votes']
    form_excluded_columns = ['votes']

    def __init__(self, session, **kwargs):
        super(GalleryPresentationView, self).__init__(Presentation, session, **kwargs)

    def is_accessible(self):
    	return current_user.is_authenticated() and current_user.email in EMAIL_ADMINS

class GalleryVoteView(ModelView):
    def __init__(self, session, **kwargs):
        super(GalleryVoteView, self).__init__(Vote, session, **kwargs)

    def is_accessible(self):
    	return current_user.is_authenticated() and current_user.email in EMAIL_ADMINS