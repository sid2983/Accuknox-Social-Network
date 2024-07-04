from django.contrib import admin

# Register your models here.
from .models import BlacklistedToken, FriendRequest, Friendship

admin.site.register(BlacklistedToken)
admin.site.register(FriendRequest)
admin.site.register(Friendship) 
