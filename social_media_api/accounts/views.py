from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import get_object_or_404
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserSummarySerializer,
    FollowSerializer
)

User = get_user_model()


class UserRegistrationView(generics.CreateAPIView):
    """
    API endpoint for user registration.
    Returns user data and authentication token.
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate token for the new user
        token, created = Token.objects.get_or_create(user=user)
        
        # Return user data with token
        user_data = UserProfileSerializer(user).data
        
        return Response({
            'user': user_data,
            'token': token.key,
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    """
    API endpoint for user login.
    Returns authentication token on successful login.
    """
    serializer = UserLoginSerializer(data=request.data)
    
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            user_data = UserProfileSerializer(user).data
            
            return Response({
                'user': user_data,
                'token': token.key,
                'message': 'Login successful'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    """
    API endpoint for user logout.
    Deletes the user's authentication token.
    """
    try:
        request.user.auth_token.delete()
        return Response({
            'message': 'Logout successful'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    API endpoint for retrieving and updating user profile.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, user_id):
    """
    Follow a user.
    """
    user_to_follow = get_object_or_404(User, id=user_id)
    
    # Check if trying to follow self
    if user_to_follow == request.user:
        return Response({
            'error': 'You cannot follow yourself.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if already following
    if request.user.is_following(user_to_follow):
        return Response({
            'error': 'You are already following this user.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Follow the user
    request.user.follow(user_to_follow)
    
    return Response({
        'message': f'You are now following {user_to_follow.username}.',
        'user': UserSummarySerializer(user_to_follow, context={'request': request}).data
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow_user(request, user_id):
    """
    Unfollow a user.
    """
    user_to_unfollow = get_object_or_404(User, id=user_id)
    
    # Check if trying to unfollow self
    if user_to_unfollow == request.user:
        return Response({
            'error': 'You cannot unfollow yourself.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if not following
    if not request.user.is_following(user_to_unfollow):
        return Response({
            'error': 'You are not following this user.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Unfollow the user
    request.user.unfollow(user_to_unfollow)
    
    return Response({
        'message': f'You have unfollowed {user_to_unfollow.username}.',
        'user': UserSummarySerializer(user_to_unfollow, context={'request': request}).data
    }, status=status.HTTP_200_OK)


class FollowersListView(generics.ListAPIView):
    """
    List all followers of the authenticated user.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserSummarySerializer
    
    def get_queryset(self):
        return self.request.user.followers.all()


class FollowingListView(generics.ListAPIView):
    """
    List all users the authenticated user is following.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserSummarySerializer
    
    def get_queryset(self):
        return self.request.user.following.all()


class UserFollowersView(generics.ListAPIView):
    """
    List followers of a specific user.
    """
    serializer_class = UserSummarySerializer
    
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        user = get_object_or_404(User, id=user_id)
        return user.followers.all()


class UserFollowingView(generics.ListAPIView):
    """
    List users that a specific user is following.
    """
    serializer_class = UserSummarySerializer
    
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        user = get_object_or_404(User, id=user_id)
        return user.following.all()
