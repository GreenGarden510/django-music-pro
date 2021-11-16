from flask_restful import Resource, reqparse
from .models import Post
from .schemas import PostSchema, FileSchema
from sqlalchemy import exc
import logging
from mkondo.security import authorized_users
from users.models import User
from media.schemas import CommentSchema
from media.models import Like, Comment

class PostListResource(Resource):
    parser = reqparse.RequestParser(trim=True, bundle_errors=True)
    parser.add_argument('user_id', type=str, required=True, location=['form', 'json'])
    parser.add_argument('caption', type=str, required=False, location=['form', 'json'])
    parser.add_argument('content', type=str, required=False, location=['form', 'json'])
    parser.add_argument('description', type=str, required=False, location=['form', 'json'])
    parser.add_argument('featured_image_url', required=False, nullable=True, location=['form', 'json'])
    parser.add_argument('featured_video_url', required=False, nullable=True, location=['form', 'json'])
    parser.add_argument('featured_audio_url', required=False, nullable=True, location=['form', 'json'])
    parser.add_argument('images', action='append', type=dict, required=False, nullable=True, location=['form', 'json'])
    parser.add_argument('videos', action='append', type=dict, required=False, nullable=True, location=['form', 'json'])

    @staticmethod
    @authorized_users(['SA', 'A', 'C', 'U', 'V'])
    def get():
        return {
            'posts': PostSchema(many=True).dump(Post.all())
        }, 200

    @staticmethod
    @authorized_users(['SA', 'A', 'C', 'U', 'V'])
    def post():
        payload = PostListResource.parser.parse_args()
        user = User.fetch_by_id(payload["user_id"]);
        if not user:
            return {
                "success": False,
                "message": "We could not find the user"
            }, 400

        payload["user_id"] = int(user.id)
        # print(payload['images']);
        
        if payload["images"]:
            payload["images"] = FileSchema(many=True).load(payload["images"])

        if payload["videos"]:
            payload["videos"] = FileSchema(many=True).load(payload["videos"])
        
        print(payload['images'])
        print(payload['videos'])
        loaded = PostSchema().load(payload)
        post = Post(**loaded);

        try:
            post.save()
        except exc.SQLAlchemyError as e:
            logging.error(e)
            return {
                       'success': False,
                       'message': 'We encountered an error while attempting to save the post.'
                   }, 500

        return {
            'post': PostSchema().dump(post)
        }, 201

class PostResource(Resource):
    parser = reqparse.RequestParser(trim=True, bundle_errors=True)
    parser.add_argument('user_id', type=str, required=False, location=['form', 'json'])
    parser.add_argument('caption', type=str, required=False, location=['form', 'json'])
    parser.add_argument('content', type=str, required=False, location=['form', 'json'])
    parser.add_argument('description', type=str, required=False, location=['form', 'json'])
    parser.add_argument('featured_image_url', required=False, nullable=True, location=['form', 'json'])
    parser.add_argument('featured_video_url', required=False, nullable=True, location=['form', 'json'])
    parser.add_argument('featured_audio_url', required=False, nullable=True, location=['form', 'json'])
    parser.add_argument('images', action='append', type=dict, required=False, nullable=True, location=['form', 'json'])
    parser.add_argument('videos', action='append', type=dict, required=False, nullable=True, location=['form', 'json'])

    @staticmethod
    @authorized_users(['SA', 'A', 'C', 'U', 'V'])
    def get(post_id):
        return {
            'post': PostSchema().dump(Post.fetch_by_id(post_id))
        }, 200

    @staticmethod
    @authorized_users(['SA', 'A', 'C'])
    def delete(post_id):
        post = Post.fetch_by_id(post_id)

        if not post:
            return {
                       'success': False,
                       'message': 'Post not found.'
                   }, 404

        post.delete()

        return {
                   'success': True,
                   'message': 'Post deleted successfully'
               }, 204
    
    @staticmethod
    @authorized_users(['SA', 'A', 'C'])
    def put(post_id):
        json_data = PostResource.parser.parse_args()

        post = Post.fetch_by_id(post_id)

        if not post:
            return {
                       'success': False,
                       'message': 'Post not found.'
                   }, 404

        post.update(**json_data)

        try:
            post.save()
        except exc.SQLAlchemyError as e:
            logging.error(e)
            return {
                       'success': False,
                       'message': 'Something went wrong while update post data.'
                   }, 500

        return {
                   'success': True,
                   'message': 'Post updated successfully'
               }, 200

class PostCommentListResource(Resource):
    parser = reqparse.RequestParser(trim=True, bundle_errors=True)
    parser.add_argument('user_id', required=True, type=str)
    parser.add_argument('value', required=True, type=str)

    @staticmethod
    @authorized_users(['SA', 'A', 'C', 'U'])
    def get(post_id):
        post = Post.fetch_by_id(post_id)

        if not post:
            return {
                'success': False,
                'message': 'Post not found'
            }

        comments = post.comments

        if not comments:
            return {
                       'success': False,
                       'message': 'No comments for this post was found'
                   }, 404
        
        jsonResponse = comments_schema.dump(comments)
        for i in range(len(jsonResponse)):
            comment = Comment.fetch_by_id(comments[i].comment_id)
            if comment.comments:
                jsonResponse[i]['no_of_replies'] = len(comment.comments)
                jsonResponse[i]['comments'] = comments_schema.dump(comment.comments)
            else:
                jsonResponse[i]['no_of_replies'] = 0
                jsonResponse[i]['comments'] = []

        return {
                   'success': True,
                   'comments': jsonResponse
               }, 200
    
    @staticmethod
    @authorized_users(['SA', 'A', 'C', 'U'])
    def post(post_id):
        json_data = PostCommentListResource.parser.parse_args()
        
        post = Post.fetch_by_id(post_id)
        if not post:
            return {
                       'success': False,
                       'message': 'Post not found'
                   }, 404

        user = User.fetch_by_id(json_data['user_id'])
        if not user:
            return {
                       'success': False,
                       'message': 'User not found'
                   }, 404

        comment_data = CommentSchema().load(json_data)
        comment_data['user_id'] = user.id
        # comment_data['media_id'] = media.id
        # del comment_data['media']
        del comment_data['user']
        comment = Comment(**comment_data)
        
        if not post.comments:
            post.comments = []

        post.comments.append(comment)
        
        try:
            post.save()
        except Exception as e:
            logging.error(e)
            return {
                       'success': False,
                       'message': 'We encountered an error while attempting to save the comment'
                   }, 500

        return {
                   'success': True,
                   'message': 'Comment added successfully'
               }, 201

class PostLikeListResource(Resource):
    parser = reqparse.RequestParser(trim=True, bundle_errors=True)
    parser.add_argument("user_id", required=True, type=str)

    @staticmethod
    def post(post_id):
        json_data = PostLikeListResource.parser.parse_args()
        
        post = Post.fetch_by_id(post_id);
        if not post:
            return {
                       'success': False,
                       'message': 'Post not found'
                   }, 404

        user = User.fetch_by_id(json_data["user_id"])
        if not user:
            return {
                'success': False,
                'message': 'User not Found'
            }, 404
        
        if post.likes and any(like.user_id == user.id for like in post.likes): 
            return {
                    'success': False,
                    'message': 'Like already exists'
                }, 500
        else:
            if not post.likes:
                post.likes = []
            
            like = Like(user.id)
            post.likes.append(like)

            try:
                post.save()
            except Exception as e:
                logging.error(e)
                return {
                    'success': False,
                    'message': 'There was an error updating post likes'
                }, 500

        return {
            'success': True,
            'message': 'Post liked successfully'
        }, 200
    
    @staticmethod
    def delete(post_id):
        json_data = PostLikeListResource.parser.parse_args()

        post = Post.fetch_by_id(post_id)
        if not post:
            return {
                success: False,
                message: "Post not found"
            }, 404

        user = User.fetch_by_id(json_data["user_id"])
        if not user:
            return {
                success: False,
                message: "User not found"
            }, 404
        
        if not post.likes or not any(like.user_id == user.id for like in post.likes):
            pass
        else:
            _like = [like for like in post.likes if like.user_id == user.id][0]

            try:
                _like.delete()
            except:
                return {
                    'success': False,
                    'message': 'There was an error updating post likes'
                }, 500

        return {
            'success': True,
            'message': 'Post likes removed successfully'
        }, 204