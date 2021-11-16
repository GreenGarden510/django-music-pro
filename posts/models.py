import uuid
from mkondo import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB
from users.models import User
from media.models import HasLikes, HasComments

class Post(HasLikes, HasComments, db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.String(50), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    caption = db.Column(db.String)
    content = db.Column(db.Text)
    description = db.Column(db.Text)
    featured_image_url = db.Column(db.String)
    featured_video_url = db.Column(db.String)
    featured_audio_url = db.Column(db.String)
    images = db.Column(JSONB, nullable=True)
    videos = db.Column(JSONB, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user = db.relationship('User', backref='posts')
    

    def __init__(self, user_id, caption, content, description, featured_image_url, featured_video_url, featured_audio_url, images, videos):
        self.post_id = uuid.uuid4()
        self.user_id = user_id
        self.caption = caption
        self.content = content
        self.description = description
        self.featured_image_url = featured_image_url
        self.featured_video_url = featured_video_url
        self.featured_audio_url = featured_video_url
        self.images = images
        self.videos = videos
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        # Delete a single post object permanently.
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def all(cls):
        posts = cls.query.order_by(Post.created_at.desc()).all()
        return posts;

    @classmethod
    def fetch_by_id(cls, post_id):
        """
        Fetch a single post object by it's id
        """
        return cls.query.filter_by(post_id=post_id).first()