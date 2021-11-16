import uuid
from datetime import datetime, timedelta
from users.models import User
from mkondo import db
from sqlalchemy import or_, desc, and_
from sqlalchemy.sql.expression import func
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declared_attr

playlist_song_table = db.Table('playlist_song',
                               db.Column('playlist_id', db.ForeignKey('playlists.id'), nullable=False),
                               db.Column('song_id', db.ForeignKey('media.id'), nullable=False)
                               )

genre_media_table = db.Table(
    'genre_media',
    db.Column('genre_id', db.Integer, db.ForeignKey('genres.id'), nullable=False),
    db.Column('media_id', db.Integer, db.ForeignKey('media.id'), nullable=False)
)

genre_album_table = db.Table(
    'genre_album',
    db.Column('genre_id', db.Integer, db.ForeignKey('genres.id'), nullable=False),
    db.Column('album_id', db.Integer, db.ForeignKey('albums.id'), nullable=False)
)

genre_series_table = db.Table(
    'genre_series',
    db.Column('genre_id', db.Integer, db.ForeignKey('genres.id'), nullable=False),
    db.Column('series_id', db.Integer, db.ForeignKey('series.id'), nullable=False),
)

class LikeAssociation(db.Model):
    # associates a collection of comment objects with a particular parent
    __tablename__ = 'like_association'

    @classmethod
    def creator(cls, discriminator):
        # provide a creator function to use with the associatoin proxy
        return lambda likes:LikeAssociation(
            likes=likes,
            dicriminator=discriminator)
    
    id = db.Column(db.Integer, primary_key=True)
    dicriminator = db.Column(db.String)
    # referes to the type of parent

    @property
    def parent(self):
        # return the parrent object
        return getattr(self, "%s_parent" % self.dicriminator)

class HasLikes(object):
    # has likes mixin creates the relationship to the likes_association table for each parent

    @declared_attr
    def like_association_id(cls):
        return db.Column(db.Integer, db.ForeignKey('like_association.id'))

    @declared_attr
    def like_association(cls):
        discriminator = cls.__name__.lower()
        cls.likes = association_proxy("like_association", "likes", creator=LikeAssociation.creator(discriminator))
        return db.relationship('LikeAssociation', foreign_keys=[cls.like_association_id], backref=db.backref('%s_parent' % discriminator, uselist=False))

class Like(db.Model):
    __tablename__ = 'likes'

    id = db.Column(db.Integer, primary_key=True)
    like_id = db.Column(db.String(50), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    association_id = db.Column(db.Integer, db.ForeignKey('like_association.id'))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = db.relationship('User', backref='likes')
    association = db.relationship('LikeAssociation', foreign_keys=[association_id], backref="likes")
    parent = association_proxy('association', 'parent')

    def __init__(self, user_id):
        self.user_id = user_id
        self.like_id = uuid.uuid4()

    @classmethod
    def fetch_all(cls):
        """
        Fetch all likes from the database
        """
        return cls.query.all()

    def save(self):
        """
        Save the current like to the database
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        Delete current like from the database.
        """
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def fetch_by_id(cls, like_id):
        """
        Fetch a like by like_id
        """
        return cls.query.filter_by(like_id=like_id).first()

class CommentAssociation(db.Model):
    # associates a collection of comment objects with a particular parent
    __tablename__ = 'comment_association'

    @classmethod
    def creator(cls, discriminator):
        # provide a creator function to use with the associatoin proxy
        return lambda comments:CommentAssociation(
            comments=comments,
            dicriminator=discriminator)
    
    id = db.Column(db.Integer, primary_key=True)
    dicriminator = db.Column(db.String)
    # referes to the type of parent

    @property
    def parent(self):
        # return the parrent object
        return getattr(self, "%s_parent" % self.dicriminator)

class HasComments(object):
    # has comments mixin creates the relationship to the comments_association table for each parent

    @declared_attr
    def comment_association_id(cls):
        return db.Column(db.Integer, db.ForeignKey('comment_association.id'))

    @declared_attr
    def comment_association(cls):
        discriminator = cls.__name__.lower()
        cls.comments = association_proxy("comment_association", "comments", creator=CommentAssociation.creator(discriminator))
        return db.relationship('CommentAssociation', foreign_keys=[cls.comment_association_id], backref=db.backref('%s_parent' % discriminator, uselist=False))

class Comment(HasComments, HasLikes, db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.String(50), unique=True)
    association_id = db.Column(db.Integer, db.ForeignKey('comment_association.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    value = db.Column(db.Text, nullable=False)
    posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    modified = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    archived = db.Column(db.Boolean, nullable=False, default=False)
    user = db.relationship('User', backref='comments')
    association = db.relationship('CommentAssociation', foreign_keys=[association_id], backref="comments")
    parent = association_proxy('association', 'parent')

    def __init__(self, value, user_id):
        self.value = value
        self.user_id = user_id
        self.comment_id = uuid.uuid4()

    @classmethod
    def fetch_all(cls):
        """
        Fetch all comments from the database
        """
        return cls.query.all()

    def save(self):
        """
        Save the current comment to the database
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        Delete current comment from the database.
        """
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def fetch_by_id(cls, comment_id):
        """
        Fetch a comment by comment_id
        """
        return cls.query.filter_by(comment_id=comment_id).first()

class Media(HasComments, HasLikes, db.Model):
    __tablename__ = 'media'

    id = db.Column(db.Integer, primary_key=True)
    media_id = db.Column(db.String(50), nullable=False, unique=True, index=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    cover_url = db.Column(db.Text, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    edited = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    plays = db.Column(db.Float, nullable=False, default=0.0)
    composer = db.Column(db.String, nullable=True)
    song_writer = db.Column(db.String, nullable=True)
    record_label = db.Column(db.String, nullable=True)
    release_date = db.Column(db.DateTime, nullable=True)
    movie_director = db.Column(db.String, nullable=True)
    staring = db.Column(db.String, nullable=True)
    production_company = db.Column(db.String, nullable=True)
    starting_date = db.Column(db.DateTime, nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    archived = db.Column(db.Boolean, nullable=False, default=False)
    shares = db.Column(db.Integer, nullable=False, default=0)
    page_views = db.Column(db.Integer, nullable=False, default=0)
    media_url = db.Column(db.Text, nullable=False)
    owner_avatar_url = db.Column(db.Text, nullable=True)
    album_id = db.Column(db.Integer, db.ForeignKey('albums.id'), nullable=True)
    album = db.relationship('Album', back_populates='songs')
    series_id = db.Column(db.Integer, db.ForeignKey('series.id'), nullable=True)
    order = db.Column(db.Integer, nullable=True)
    series = db.relationship('Series', back_populates='episodes')
    genres = db.relationship('Genre', secondary=genre_media_table, backref='media')
    owner = db.relationship('User')

    def __init__(self, name, description, cover_url, duration, category, owner_id, media_url, record_label=None,
                 release_date=None, composer=None, song_writer=None, owner_avatar_url=None, album_id=None, genres=None, movie_director=None, staring=None, production_company=None, starting_date=None, series_id=None):
        self.media_id = uuid.uuid4()
        self.name = name
        self.description = description
        self.cover_url = cover_url
        self.duration = duration
        self.category = category
        self.owner_id = owner_id
        self.media_url = media_url

        if movie_director:
            self.movie_director = movie_director

        if staring:
            self.staring = staring

        if production_company:
            self.production_company = production_company
        
        if starting_date:
            self.starting_date = starting_date
        
        if album_id:
            self.album_id = album_id

        if song_writer:
            self.song_writer = song_writer

        if record_label:
            self.record_label = record_label

        if composer:
            self.composer = composer

        if release_date:
            self.release_date = release_date
        
        if owner_avatar_url:
            self.owner_avatar_url = owner_avatar_url
        
        if genres:
            for genre in genres:
                self.genres.append(Genre.get_or_create(genre['name']))
            
        if series_id:
            self.series_id = series_id

    def set_genres(self, genres):
        print('setting genres')
        self.genres = []
        for genre in genres:
            print(genre)
            self.genres.append(Genre.get_or_create(genre))

    def __repr__(self):
        """
        Represent a media instance by the media name.
        """
        return self.name

    @classmethod
    def fetch_all(cls):
        """
        Fetch all media files from storage.
        """
        return cls.query.filter_by(archived=False).all()

    @classmethod
    def fetch_latest_release(cls, amount, category):
        """
        Return latest release by amount.
        """
        return cls.query.filter_by(archived=False).filter_by(category=category).order_by(desc(cls.added)).limit(amount).all()

    @classmethod
    def fetch_top_medias(cls, amount, category):
        """
        Return latest release by amount.
        """
        return cls.query.filter_by(archived=False).filter_by(category=category).order_by(desc(cls.plays)).limit(amount).all()

    @classmethod
    def fetch_random_medias(cls, amount, category):
        """
        Return latest release by amount.
        """
        return cls.query.filter_by(archived=False).filter_by(category=category).order_by(func.random()).limit(amount).all()

    @classmethod
    def fetch_trend_medias(cls, amount, category):
        """
        Return latest release by amount.
        """
        delta = datetime.now() - timedelta(hours = 48)
        return cls.query.filter_by(archived=False).filter(and_(cls.category==category, delta < cls.added, 0 < cls.plays)).order_by(desc(cls.plays)).limit(amount).all()

    @classmethod
    def fetch_recommend_medias(cls, amount, category):
        """
        Return latest release by amount.
        """
        return cls.query.filter_by(archived=False).filter_by(category=category).order_by(func.random()).limit(amount).all()

    @classmethod
    def get_media_by_user_id(cls, user_id):
        """
        Return all media belonging to a user
        """
        return cls.query.filter_by(archived=False).filter_by(owner_id=user_id)

    @classmethod
    def fetch_by_id(cls, media_id):
        """
        Fetch a single media object by it's id
        """
        return cls.query.filter_by(media_id=media_id).first()
    
    @classmethod
    def fetch_by_ids(cls, ids):
        """
        Fetch for media by multiple ids
        """
        return cls.query.filter(cls.media_id.in_(ids)).all()

    @classmethod
    def fetch_similar(cls, media_id, limit=10):
        # Return all media that are similar to the paying media
        comparator = cls.fetch_by_id(media_id)

        # similar category medias
        similar_category_meidias = cls.query.filter_by(archived=False).filter_by(category=comparator.category)
        # similar user
        similar_user_medias = cls.get_media_by_user_id(comparator.owner_id)

        return similar_user_medias.filter_by(category=comparator.category).filter(Media.media_id != media_id).order_by(func.random()).limit(limit).all()

    def save(self):
        """
        Save the current media object to the database.
        """
        db.session.add(self)
        db.session.commit()
    
    def update(self, **kwargs):
        for key, value in  kwargs.items():
            print(key, value)
            if (hasattr(self, key) and value is not None):
                print('valid key value')
                try:
                    if key != 'genres':
                        setattr(self, key, value)
                    if key == 'genres':
                        print('genres detected')
                        self.set_genres(value)
                    print('updated')
                except:
                    print('error')

    @classmethod
    def search(cls, query, limit=10):
        """
        Search media by query
        """
        return cls.query.filter_by(archived=False).filter((cls.name.ilike(f'%{query}%')) | (cls.description.ilike(f'%{query}%'))).limit(limit).all()

    def delete(self):
        """
        Delete a single media object permanently.
        """
        self.archived = True;
        self.save();

class Playlist(HasLikes, db.Model):
    __tablename__ = 'playlists'

    id = db.Column(db.Integer, primary_key=True)
    playlist_id = db.Column(db.String(50), nullable=False, unique=True)
    name = db.Column(db.String(255), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    modified = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    duration = db.Column(db.Integer, nullable=False, default=0)
    shares = db.Column(db.Integer, nullable=False, default=0)
    page_views = db.Column(db.Integer, nullable=False, default=0)
    songs = db.relationship('Media', secondary=playlist_song_table, backref=db.backref('playlists'), cascade="all")
    owner = db.relationship('User', backref='playlists')

    def __init__(self, name, owner_id):
        self.name = name
        self.owner_id = owner_id
        self.playlist_id = uuid.uuid4()

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def fetch_by_id(cls, playlist_id):
        """
        Fetch a playlist by id
        """
        return cls.query.filter_by(playlist_id=playlist_id).first()

    @classmethod
    def has_song(cls, song_id):
        """
        Checks and returns True if a song is in the playlist
        """
        songs = cls.query.filter(cls.songs.any(media_id=song_id)).all()

        if len(songs) < 1:
            return False
        else:
            return True

    @classmethod
    def fetch_playlists_by_user_id(cls, user_id):
        return cls.query.filter_by(owner_id=user_id).all()

    def save(self):
        """
        Save current playlist to the database.
        """
        db.session.add(self)
        db.session.commit()

class Album(HasLikes, HasComments, db.Model):
    __tablename__ = 'albums'

    id = db.Column(db.Integer, primary_key=True)
    album_id = db.Column(db.String(50), nullable=False, unique=True)
    name = db.Column(db.String(255), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    modified = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    plays = db.Column(db.Integer, nullable=False, default=0)
    description = db.Column(db.Text, nullable=True)
    cover_image = db.Column(db.Text, nullable=True)
    archived = db.Column(db.Boolean, default=False)
    shares = db.Column(db.Integer, nullable=False, default=0)
    page_views = db.Column(db.Integer, nullable=False, default=0)
    publisher = db.Column(db.String, nullable=True)
    region = db.Column(db.String, nullable=True)
    country = db.Column(db.String, nullable=True)
    record_label = db.Column(db.String, nullable=True)
    release_date = db.Column(db.DateTime, nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    songs = db.relationship('Media', back_populates='album')
    genres = db.relationship('Genre', secondary=genre_album_table, backref='albums')


    def __init__(self, name, owner_id, publisher=None, region=None, country=None, record_label=None, release_date=None, genres=None):
        self.name = name
        self.owner_id = owner_id
        self.album_id = uuid.uuid4()
        
        if region:
            self.region = region
        
        if country:
            self.country = country
        
        if record_label:
            self.record_label = record_label
        
        if publisher:
            self.publisher = publisher
        
        if release_date:
            self.release_date = release_date
        
        if genres:
            for genre in genres:
                self.genres.append(Genre.get_or_create(genre['name']))

    def __repr__(self):
        return self.name

    @classmethod
    def fetch_all(cls):
        """
        Fetch all albums that are not archived from the database
        """
        return cls.query.filter_by(archived=False).all()
    
    @classmethod
    def search(cls, query, limit=10):
        """
        Search media by query
        """
        return cls.query.filter((cls.name.ilike(f'%{query}%')) | (cls.description.ilike(f'%{query}%'))).limit(limit).all()

    def save(self):
        """
        Save the current album to the database.
        """
        db.session.add(self)
        db.session.commit()

    @classmethod
    def fetch_by_id(cls, album_id):
        """
        Fetch an album by it's id
        """
        return cls.query.filter_by(album_id=album_id).first()

    @classmethod
    def fetch_archived(cls):
        """
        Fetch all archived albums
        """
        return cls.query.filter_by(archived=True).all()

    def delete(self):
        """
        Delete current album
        """
        db.session.delete(self)
        db.session.commit()

class Genre(db.Model):
    __tablename__ = 'genres'

    id = db.Column(db.Integer, primary_key=True)
    genre_id = db.Column(db.String(50), nullable=False, unique=True)
    name = db.Column(db.String, nullable=False, unique=True)

    def __init__(self, name):
        self.genre_id = uuid.uuid4()
        self.name = name.lower()
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_or_create(cls, name):
        """
        Gets a genre or creates one if it does not exist.
        """
        genre = cls.query.filter_by(name=name.lower()).first()

        if not genre:
            genre = cls(name.lower())
            genre.save()
        
        return genre

class Slider(db.Model):
    __tablename__ = 'sliders'

    id = db.Column(db.Integer, primary_key=True)
    slider_id = db.Column(db.String(50), nullable=False, unique=True)
    name = db.Column(db.String)
    aspect_ratio_x = db.Column(db.Integer)
    aspect_ratio_y = db.Column(db.Integer)
    items = db.relationship("SliderItem", back_populates="slider")
    
    def __init__(self, name, aspect_ratio_x, aspect_ratio_y):
        self.slider_id = uuid.uuid4()
        self.aspect_ratio_x = aspect_ratio_x
        self.aspect_ratio_y = aspect_ratio_y
        self.name = name
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        # Delete a single slider object permanently.
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def fetch_all(cls):
        """
        Fetch all sliders from storage.
        """
        return cls.query.all()
    
    @classmethod
    def all(cls):
        """
        Fetch all sliders from storage.
        """
        return cls.query.all()

    @classmethod
    def find(cls, slider_id):
        # fetch slider by id
        return  cls.query.filter_by(slider_id=slider_id).first()

class SliderItem(db.Model):
    __tablename__ = 'slider_items'

    id = db.Column(db.Integer, primary_key=True)
    slider_id = db.Column(db.String(50), db.ForeignKey('sliders.slider_id'), nullable=False)
    slider_item_id = db.Column(db.String(50), nullable=False, unique=True)
    image_url = db.Column(db.String)
    slider = db.relationship("Slider", back_populates="items")

    def __init__(self, slider_id, image_url):
        self.slider_item_id = uuid.uuid4()
        self.slider_id = slider_id
        self.image_url = image_url
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        # Delete a single slider object permanently.
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def all(cls):
        # get all records
        return cls.query.all()

    @classmethod
    def findBySlider(cls, slider_id):
        # get pictures by slider id
        return cls.query.filter_by(slider_id=slider_id)
    
    @classmethod
    def find(cls, slider_item_id):
         # fetch slider item by id
        return  cls.query.filter_by(slider_item_id=slider_item_id).first()

class Series(HasLikes, HasComments, db.Model):
    __tablename__ = 'series'

    id = db.Column(db.Integer, primary_key=True)
    series_id = db.Column(db.String(50), nullable=False, unique=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    cover_url = db.Column(db.String)
    trailer_url = db.Column(db.String)
    episodes = db.relationship('Media', back_populates='series')
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    modified = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    genres = db.relationship('Genre', secondary=genre_series_table, backref='series')
    archived = db.Column(db.Boolean, nullable=False, default=False)

    def __init__ (self, title, description, owner_id, cover_url, trailer_url, genres ):
        self.series_id = uuid.uuid4()
        self.title = title
        self.archived = False

        if description:
            self.description = description

        if owner_id:
            self.owner_id = owner_id
        
        if cover_url:
            self.cover_url = cover_url

        if trailer_url:
            self.trailer_url = trailer_url
        
        if genres:
            print(str(genres))
            for genre in genres:
                print(genre);
                self.genres.append(Genre.get_or_create(genre['name']))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        self.archived = True
        self.save()

    @classmethod
    def fetch_all(cls):
        # fetch all series
        return cls.query.filter_by(archived=False).all()

    @classmethod
    def fetch_by_id(cls, series_id):
        # fetch series by id
        return cls.query.filter_by(series_id=series_id).first()