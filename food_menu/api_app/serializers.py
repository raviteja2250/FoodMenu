from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model, authenticate
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class MenuItemSerializer(serializers.ModelSerializer):
    item_id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=500, required=False)
    category = serializers.CharField(required=False)
    thumb_image_url = serializers.ImageField(max_length=50,use_url=True, allow_null=True, required=False)

    class Meta:
        model = MenuItem
        fields = '__all__'



class CategoryFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('__all__')
        depth = 1

    category_name = serializers.CharField()
    category_detail = serializers.CharField(required=False)
    items = MenuItemSerializer(many=True,read_only=True)

    def create(self, validated_data):
        category_instance = Category.objects.create(**validated_data)
        return category_instance


    
class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    username = serializers.CharField(
            max_length=32,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    password = serializers.CharField(min_length=8, write_only=True)


    def create(self, validated_data):
        user = User(email=validated_data['email'],
                username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=False)
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user:
            return user

        raise serializers.ValidationError("Incorrect Credentials")
