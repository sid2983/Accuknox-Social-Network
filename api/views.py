
# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, UserSearchSerializer, FriendRequestSerializer,FriendshipSerializer
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from .models import BlacklistedToken, FriendRequest, Friendship 
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime, timedelta
from django.contrib.auth.hashers import make_password
import logging


logger = logging.getLogger(__name__)





### Home Page Description View ###
@api_view(['GET'])
@permission_classes([AllowAny])
def home_page(request):
    data = {
        'message': 'Welcome to the home page of our API!',
        'api_version': 'v1',
        'status': 'active',
        'author': 'Siddharth Kumar Pandey',
    }
    return Response(data, status=status.HTTP_200_OK)








### User Registration View ###

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    print("POST request data: %s", request.data)
    if request.method == 'POST':
        password = request.data.get('password')
        
        serializer = UserSerializer(data=request.data)
        print("Serializer data:", serializer)
        print(request.data)

        if serializer.is_valid():
            # Create user object, setting password explicitly
            user = User(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email'],
                password=make_password(password),  # Hash password
            )
            user.save()

            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







### User Login View ###

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    print("Received email:", email)
    if not email or not password:
        return Response({'detail': 'Must include "email" and "password".'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'detail': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    # Verify password
    if user.check_password(password):
        # Password correct, generate tokens
        refresh = RefreshToken.for_user(user)
        print(f"User {user} logged in successfully.")
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)

    else:
        # Password incorrect
        return Response({'detail': 'Invalid email or password.'}, status=status.HTTP_400_BAD_REQUEST)
    






### User Logout View ###

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    
    try:
        token = request.data.get('refresh')
        print("Received refresh token:", token)
        if not token:
            return Response({'detail': 'Refresh Token is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Blacklist the token
        BlacklistedToken.objects.create(token=token, user=request.user)

        return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    






#### User Search View ####

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_users(request):
    serializer = UserSearchSerializer(data=request.GET)
    if serializer.is_valid():
        search_keyword = serializer.validated_data['search_keyword']

        # Perform search based on email or name
        users = User.objects.filter(
            Q(email__iexact=search_keyword) |
            Q(username__icontains=search_keyword)
        )

        # Pagination
        paginator = Paginator(users, 10)  # 10 users per page
        page_number = request.GET.get('page')
        try:
            paginated_users = paginator.page(page_number)
        except PageNotAnInteger:
            paginated_users = paginator.page(1)
        except EmptyPage:
            paginated_users = paginator.page(paginator.num_pages)

        # Serialize paginated data
        serialized_users = UserSerializer(paginated_users, many=True)

        return Response(serialized_users.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







#### Send Friend Request View ####

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_friend_request(request):
    one_minute_ago = datetime.now() - timedelta(minutes=1)
    recent_requests_count = FriendRequest.objects.filter(
        sender=request.user,
        created_at__gte=one_minute_ago
    ).count()
    if recent_requests_count >= 3:
        return Response({'detail': 'You cannot send more than 3 friend requests within a minute.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

    receiver_username = request.data.get('receiver_username')
    if not receiver_username:
        return Response({'detail': 'Receiver username is required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        
        receiver = User.objects.get(username=receiver_username)
    except User.DoesNotExist:
        return Response({'detail': 'User with this username does not exist.'}, status=status.HTTP_404_NOT_FOUND)
    
    # print(request.user.id, receiver.id)
    data = {
        'sender': request.user.id,
        'receiver': receiver.id
    }
    serializer = FriendRequestSerializer(data=data,context={'request': request})
    if serializer.is_valid():
        serializer.save(sender=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





#### Accept Friend Request Views ####

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_friend_request(request, request_id):
    try:
        friend_request = FriendRequest.objects.get(sender=request_id, receiver=request.user)
        # print(friend_request)
        friend_request.accept()
        return Response({'detail': 'Friend request accepted.'}, status=status.HTTP_200_OK)
    except FriendRequest.DoesNotExist:
        return Response({'detail': 'Friend request not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)





#### Reject Friend Request View ####

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reject_friend_request(request, request_id):
    try:
        friend_request = FriendRequest.objects.get(sender=request_id, receiver=request.user)
        friend_request.reject()
        return Response({'detail': 'Friend request rejected.'}, status=status.HTTP_200_OK)
    except FriendRequest.DoesNotExist:
        return Response({'detail': 'Friend request not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)




#### List Friends (Accepted) View ####

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_friends(request):
    friends = request.user.friends.all()
    # print(friends)
    serializer = FriendshipSerializer(friends, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)




#### List Pending Friend Requests View ####

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_pending_friend_requests(request):
    pending_requests = FriendRequest.objects.filter(receiver=request.user, status='pending')
    serializer = FriendRequestSerializer(pending_requests, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
