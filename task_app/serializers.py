from rest_framework import serializers
from django.contrib.auth.models import User
from .models import*
from django.contrib.auth import authenticate


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True}  
        }

    def validate(self, data):
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('Username is already taken!')
        
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')  
        user = User(**validated_data)  
        user.set_password(password)  
        user.save()  
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        
        if user is None:
            raise serializers.ValidationError("Invalid login credentials")
        
        data['user'] = user
        return data
    
class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'title', 'content']
        
class BlogSerializer(serializers.ModelSerializer):
    total_likes = serializers.SerializerMethodField()
    class Meta:
        model = Blog
        fields = ['id', 'title', 'content', 'liked_by', 'total_likes']
        
    def get_total_likes(self, obj):
        return obj.total_likes()

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['comment']