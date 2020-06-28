from app import db
from sqlalchemy import func

class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(255))
    message = db.Column(db.Text())
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())

    def __repr__(self):
        return '<Message %r>' % self.email
