from mkondo import db

class Message(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.String(50), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    caption = db.Column(db.String)