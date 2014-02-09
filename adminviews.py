from flask.ext.admin.contrib.sqla import ModelView
from models import User, Presentation


class GalleryUserView(ModelView):
    column_exclude_list = ['votes']
    form_excluded_columns = ['votes']

    def __init__(self, session, **kwargs):
        super(GalleryUserView, self).__init__(User, session, **kwargs)

class GalleryPresentationView(ModelView):
    column_exclude_list = ['votes']
    form_excluded_columns = ['votes']

    def __init__(self, session, **kwargs):
        super(GalleryPresentationView, self).__init__(Presentation, session, **kwargs)