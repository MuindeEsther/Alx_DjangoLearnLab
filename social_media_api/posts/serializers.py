from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment, Like

User = get_user_model()


class AuthorSerializer(serializers.ModelSerializer):
   # Serializer for displaying author information.
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'profile_picture')
        read_only_fields = fields


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for Comment model.
    """
    author = AuthorSerializer(read_only=True)
    author_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Comment
        fields = (
            'id', 'post', 'author', 'author_id', 'content',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at', 'author')

    def create(self, validated_data):
        # Set author from request context
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for Post model with nested comments.
    """
    author = AuthorSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.ReadOnlyField()

    class Meta:
        model = Post
        fields = (
            'id', 'author', 'title', 'content', 'comments_count',
            'comments', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'author', 'created_at', 'updated_at')

    def create(self, validated_data):
        # Set author from request context
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class PostListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for post listing (without comments).
    """
    author = AuthorSerializer(read_only=True)
    comments_count = serializers.ReadOnlyField()

    class Meta:
        model = Post
        fields = (
            'id', 'author', 'title', 'content', 'comments_count',
            'created_at', 'updated_at'
        )
        read_only_fields = fields
        
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']
        read_only_fields = ['user']

