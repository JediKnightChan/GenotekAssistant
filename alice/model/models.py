from alice import db
from sqlalchemy_utils import JSONType


class AppUser(db.Model):
    yandex_id = db.Column(db.String(64), primary_key=True)
    username = db.Column(db.String(32))
    json_filename = db.Column(db.String(128))
    location = db.Column(JSONType)
    search_request = db.relationship('SearchRequest', backref='app_user', lazy=True, uselist=False)

    def __repr__(self):
        return '<User {}: {}>'.format(self.yandex_id, self.username)


class SearchRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    potential_paths = db.Column(JSONType)
    available_specifying_options = db.Column(JSONType)
    comparison_depth = db.Column(db.SmallInteger)
    app_user_id = db.Column(db.Integer, db.ForeignKey('app_user.yandex_id'),
                            nullable=True)
