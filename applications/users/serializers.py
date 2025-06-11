from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','first_name','last_name','email','course','experience','level','school_id','last_name','username','is_superuser')
        extra_kwargs = {
            'is_superuser': {'read_only': True}
        }

class UserLoginSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ('email','password')