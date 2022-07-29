import os

from utils.dep import db
from flask import url_for


     


class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100))
    user = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete="CASCADE"))
    text = db.Column(db.Text)
    date_time = db.Column(
        db.DateTime, default=db.func.now(), onupdate=db.func.now())


class EditableHTML(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    editor_name = db.Column(db.String(100), unique=True)
    value = db.Column(db.Text)

    @staticmethod
    def get_editable_html(editor_name:str):
        """Returns a specific page"""
        editable_html_obj = EditableHTML.query.filter_by(
            editor_name=editor_name).first()

        if editable_html_obj is None:
            editable_html_obj = EditableHTML(editor_name=editor_name, value='')
        return editable_html_obj

    @property
    def serialize(self):
        return {
            'id': self.id,
            'editor_name': self.editor_name,
            'value': self.value
        }


class SiteLogo(db.Model):
    """Maps Site logo image to table"""
    _tablename_ = "logo"
    id = db.Column(db.Integer, primary_key=True)
    logo_image = db.Column(db.String(256), nullable=False)

    @property
    def image_url(self):
        return url_for('_uploads.uploaded_file', setname='images', filename=self.logo_image, external=True)

    @property
    def image_path(self):
        from flask import current_app
        return os.path.join(current_app.config['UPLOADED_IMAGES_DEST'], self.logo_image)


class BackgroundImage(db.Model):
    """Maps Site background image to table"""
    _tablename_ = "background_image"
    id = db.Column(db.Integer, primary_key=True)
    background_image = db.Column(db.String(256), nullable=False)

    @property
    def image_url(self):
        return url_for('_uploads.uploaded_file', setname='images', filename=self.background_image, external=True)

    @property
    def image_path(self):
        from flask import current_app
        return os.path.join(current_app.config['UPLOADED_IMAGES_DEST'], self.background_image)


class LandingSetting(db.Model):
    """Maps Site global setting to table"""
    __tablename__ = 'landing_settings'

    id = db.Column(db.Integer, primary_key=True)
    site_name = db.Column(db.String(128), unique=True, nullable=True)
    title = db.Column(db.String(128), unique=True, nullable=True)
    description = db.Column(db.String(180), unique=True, nullable=True)
    working_hours = db.Column(db.String(100), nullable=True, default=None)
    email = db.Column(db.String(100), nullable=True, default=None)
    contact_phone = db.Column(db.String(200), nullable=True, default=None)
    address = db.Column(db.String(200), default=None, nullable=True)
    twitter = db.Column(db.String(25), unique=True, nullable=True, default=None)
    facebook = db.Column(db.String(25), unique=True, nullable=True, default=None)
    instagram = db.Column(db.String(25), unique=True, nullable=True, default=None)
    linkedin = db.Column(db.String(25), unique=True, nullable=True, default=None)
    tiktok = db.Column(db.String(25), unique=True, nullable=True, default=None)
    snap_chat = db.Column(db.String(25), unique=True, nullable=True, default=None)
    youtube = db.Column(db.String(25), unique=True, nullable=True, default=None)
    google_analytics_id = db.Column(db.String(25), unique=True, nullable=True, default=None)
    other_tracking_analytics_one = db.Column(db.Text, nullable=True, default=None)
    other_tracking_analytics_two = db.Column(db.Text, nullable=True, default=None)
    other_tracking_analytics_three = db.Column(db.Text, nullable=True, default=None)
    other_tracking_analytics_four = db.Column(db.Text, nullable=True, default=None)
