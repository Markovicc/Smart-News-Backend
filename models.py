from app import app, db

from datetime import datetime


class NewsFeed(db.Model):
    __tablename__ = 'newsfeed'

    id = db.Column(db.Integer, primary_key=True)
    medij = db.Column(db.String, nullable=False)
    naslov = db.Column(db.String, nullable=False)
    uvod = db.Column(db.Text, nullable=False)
    link = db.Column(db.String, nullable=False)
    komentari = db.Column(db.Integer, nullable=False)
    vreme = db.Column(db.DateTime, nullable=False, default=datetime.now)
    foto = db.Column(db.String, nullable=False)
    rubrika = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<id {}>'.format(self.id)
