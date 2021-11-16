from mkondo import marshmallow
from .models import Media, Playlist, Album, Comment, Genre, Slider, SliderItem, Like, Series
from marshmallow import fields, EXCLUDE

class LikeSchema(marshmallow.SQLAlchemyAutoSchema):
    user_id = fields.String(attribute="user.user_id")

    class Meta:
        model = Like
        fields = ('like_id', 'user_id', 'created_at', 'updated_at')
        dump_only = ('like_id')

class CommentSchema(marshmallow.SQLAlchemyAutoSchema):
    commenter_name = fields.String(attribute='user.full_name')
    avatar_user_url = fields.String(attribute='user.avatar_url')
    # media_id = fields.String(attribute='media.media_id')
    user_id = fields.String(attribute='user.user_id')
    likes = marshmallow.Nested(LikeSchema(dump_only=('like_id',), many=True))


    class Meta:
        model = Comment
        fields = ('value', 'comment_id', 'user_id', 'posted', 'modified', 'commenter_name', 'avatar_user_url', 'likes')
        dump_only = ('commenter_name', 'avatar_user_url')

class MediaSchema(marshmallow.SQLAlchemySchema):
    category = fields.String(allow_none=True)
    duration = fields.Integer(allow_none=True)
    order = fields.Integer(allow_none=True)
    composer = fields.String(allow_none=True)
    cover_url = fields.String(allow_none=True)
    release_date = fields.Date(allow_none=True)
    record_label = fields.String(allow_none=True)
    song_writer = fields.String(allow_none=True)
    movie_director = fields.String(allow_none=True)
    staring = fields.String(allow_none=True)
    starting_date = fields.String(allow_none=True)
    production_company = fields.String(allow_none=True)
    owner_avatar_url = fields.String(allow_none=True)
    album_id = fields.String(attribute='album.album_id', allow_none=True)
    owner_id = fields.String(attribute='owner.user_id', allow_none=True)
    owner_name = fields.String(attribute='owner.full_name', allow_none=True)
    genres = fields.Pluck('GenreSchema', 'name', many=True)
    likes = marshmallow.Nested(LikeSchema(dump_only=('like_id',), many=True))
    comments = marshmallow.Nested(CommentSchema(dump_only=('comment_id'), many=True))
    series_id = fields.String(attribute='series.series_id', allow_none=True)

    class Meta:
        model = Media
        fields = (
            'media_id', 'name', 'description', 'cover_url', 'duration', 'category', 'added', 'edited', 'plays',
            'owner_id', 'order',
            'archived', 'likes', 'media_url', 'page_views', 'shares', 'composer', 'release_date', 'song_writer',
            'record_label', 'owner_avatar_url', 'album_id', 'owner_name', 'genres', 'production_company', 'movie_director', 'staring', 'starting_date', 'comments', 'series_id')
        dump_only = ('owner_name',)


class PlaylistSchema(marshmallow.SQLAlchemySchema):
    songs = marshmallow.Nested(MediaSchema, many=True)
    owner_user_id = fields.String(attribute='owner.user_id')

    class Meta:
        model = Playlist
        fields = ('name', 'owner_id', 'duration', 'created', 'modified', 'songs', 'page_views', 'shares', 'likes', 'playlist_id', 'owner_user_id')
        load_only = ('owner_id',)
        dump_only = ('songs', 'owner_user_id')


class AlbumSchema(marshmallow.SQLAlchemySchema):
    songs = marshmallow.Nested(MediaSchema, many=True)
    release_date = fields.String(allow_none=True)
    record_label = fields.String(allow_none=True)
    publisher = fields.String(allow_none=True)
    country = fields.String(allow_none=True)
    region = fields.String(allow_none=True)
    genres = fields.Pluck('GenreSchema', 'name', many=True)

    class Meta:
        model = Album
        fields = (
            'name', 'description', 'songs', 'plays', 'genres', 'cover_image', 'modified', 'archived', 'created',
            'owner_id',
            'album_id', 'page_views', 'shares', 'likes', 'publisher', 'release_date', 'region', 'country', 'record_label')
        dump_only = ('songs',)
        load_only = ('owner_id',)
        include_fk = True


class GenreSchema(marshmallow.SQLAlchemySchema):
    class Meta:
        model = Genre
        fields = ('name', 'genre_id')
        dump_only = ('genre_id',)

class SliderItemSchema(marshmallow.SQLAlchemySchema):
    class Meta:
        model = SliderItem
        fields = ('slider_item_id', 'image_url', 'slider_id')
        dump_only = ('slider_item_id',)

class SliderSchema(marshmallow.SQLAlchemySchema):
    items = marshmallow.Nested(SliderItemSchema, many=True)
    class Meta:
        model = Slider
        fields = ('name', 'slider_id', 'aspect_ratio_x', 'aspect_ratio_y', 'items')
        dump_only = ('slider_id',)

class SeriesSchema(marshmallow.SQLAlchemySchema):
    description = fields.String(allow_none=True)
    owner_name = fields.String(attribute='owner.full_name', allow_none=True)
    genres = fields.Pluck('GenreSchema', 'name', many=True)
    episodes = marshmallow.Nested(MediaSchema, many=True)
    title = fields.String(allow_none=False)
    class Meta:
        model = Series
        unknown = EXCLUDE
        fields = ('series_id', 'owner_id', 'title', 'description', 'cover_url', 'trailer_url', 'owner', 'owner_name', 'created_at', 'episodes', 'genres')