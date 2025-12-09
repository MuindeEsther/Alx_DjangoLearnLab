from django.shortcuts import render
from rest_framework import viewsets, permissions, filters, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from .models import Post, Comment, Like
from notifications.utils import create_notification  
from .serializers import (
    PostSerializer,
    PostListSerializer,
    CommentSerializer
)
from .permissions import IsAuthorOrReadOnly
from .pagination import StandardResultsPagination
# Create your views here.

User = get_user_model()
class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Post model.
    Provides CRUD operations with pagination and filtering.
    """
    queryset = Post.objects.all().select_related('author').prefetch_related('comments')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = StandardResultsPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content', 'author__username']
    ordering_fields = ['created_at', 'updated_at', 'title']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """
        Use different serializers for list and detail views.
        """
        if self.action == 'list':
            return PostListSerializer
        return PostSerializer

    def perform_create(self, serializer):
        """
        Set the author to the current user when creating a post.
        """
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """
        Custom action to retrieve all comments for a specific post.
        """
        post = self.get_object()
        comments = post.comments.all()
        page = self.paginate_queryset(comments)
        
        if page is not None:
            serializer = CommentSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my_posts(self, request):
        """
        Custom action to retrieve posts created by the authenticated user.
        """
        posts = self.queryset.filter(author=request.user)
        page = self.paginate_queryset(posts)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)
    
    action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user

        if Like.objects.filter(user=user, post=post).exists():
            return Response({"error": "You already liked this post."}, status=400)

        Like.objects.create(user=user, post=post)

        # Create notification
        create_notification(
            recipient=post.author,
            actor=user,
            verb="liked your post",
            target=post
        )

        return Response({"message": "Post liked successfully."})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unlike(self, request, pk=None):
        post = self.get_object()
        user = request.user

        like = Like.objects.filter(user=user, post=post).first()
        if not like:
            return Response({"error": "You have not liked this post."}, status=400)

        like.delete()
        return Response({"message": "Post unliked successfully."})


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Comment model.
    Provides CRUD operations with pagination and filtering.
    """
    queryset = Comment.objects.all().select_related('author', 'post')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = StandardResultsPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['post', 'author']
    search_fields = ['content', 'author__username']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        """
        Set the author to the current user when creating a comment.
        """
        serializer.save(author=self.request.user)

    @action(detail=False, methods=['get'])
    def my_comments(self, request):
        """
        Custom action to retrieve comments created by the authenticated user.
        """
        comments = self.queryset.filter(author=request.user)
        page = self.paginate_queryset(comments)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data)
    
class FeedView(generics.ListAPIView):
    """
    Feed view that displays posts from users the authenticated user follows.
    Posts are ordered by creation date (newest first).
    """
    serializer_class = PostListSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsPagination
    
    def get_queryset(self):
        """
        Return posts from users that the current user follows.
        """
        user = self.request.user
        # Get all users the current user is following
        following_users = user.following.all()
        # Return posts from those users, ordered by creation date
        queryset = Post.objects.filter(author__in=following_users).order_by('-created_at')
        return queryset.select_related('author')
    
    def list(self, request, *args, **kwargs):
        """
        Override list to add additional context.
        """
        queryset = self.get_queryset()
        
        # If user is not following anyone
        if not queryset.exists():
            return Response({
                'message': 'Your feed is empty. Start following users to see their posts!',
                'count': 0,
                'results': []
            }, status=status.HTTP_200_OK)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
