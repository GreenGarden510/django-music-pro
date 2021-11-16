from mkondo import marshmallow
from marshmallow import fields
from posts.models import Post
from users.schemas import UserSchema
from media.schemas import CommentSchema, LikeSchema


class FileSchema(marshmallow.SQLAlchemySchema):
    class Meta:
        fields = ('url', 'caption')

class PostSchema(marshmallow.SQLAlchemySchema):
    images = fields.List(fields.Nested(FileSchema), allow_none=True)
    videos = fields.List(fields.Nested(FileSchema), allow_none=True)
    user = fields.Nested(UserSchema)
    post_id = fields.String(allow_none=False)
    caption = fields.String(allow_none=True)
    content = fields.String(allow_none=True)
    description = fields.String(allow_none=True)
    featured_image_url = fields.String(allow_none=True)
    featured_video_url = fields.String(allow_none=True)
    featured_audio_url = fields.String(allow_none=True)
    created_at = fields.Date(allow_none=True)
    comments = marshmallow.Nested(CommentSchema(dump_only=('comment_id'), many=True))
    likes = marshmallow.Nested(LikeSchema(many=True))

    class Meta:
        model = Post
        fields = ('post_id', 'user_id', 'caption', 'content', 'description', 'featured_image_url', 'featured_video_url', 'featured_audio_url', 'images', 'videos', 'user', 'created_at', 'comments', 'likes')
        dump_only = ('content')
        load_only = ('content')