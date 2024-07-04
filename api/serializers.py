
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate
from .models import BlacklistedToken, FriendRequest, Friendship 

import logging

logger = logging.getLogger(__name__)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 6},  # Ensure password is write_only
        }






class BlacklistedTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlacklistedToken
        fields = '__all__'



class UserSearchSerializer(serializers.Serializer):
    search_keyword = serializers.CharField(max_length=100)





# serializers.py



class FriendRequestSerializer(serializers.ModelSerializer):
    sender_username = serializers.SerializerMethodField()
    class Meta:
        model = FriendRequest
        fields = ['id', 'sender', 'sender_username', 'receiver', 'status', 'created_at']
        read_only_fields = ['id', 'sender', 'created_at']

    def get_sender_username(self, obj):
        return obj.sender.username

    def validate(self, data):
        sender = self.context['request'].user
        receiver = data['receiver']
        # Ensure sender and receiver are different
        if sender == receiver:
            raise serializers.ValidationError("Cannot send friend request to yourself.")
        return data



class FriendshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friendship
        fields = ['id', 'user', 'friend']





