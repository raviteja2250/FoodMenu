from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework import status, generics
from api_app.serializers import UserSerializer, LoginSerializer
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token
#import requests
from rest_framework.decorators import api_view, permission_classes
from .models import *
from .serializers import *
import sys
from datetime import datetime,timedelta
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets

# Create your views here.


class UserCreate(APIView):

    """ 
    Creates the user. 
    """
    
    permission_classes = [AllowAny]
    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.create(user=user)
                json = serializer.data
                json['token'] = token.key
                return Response(json, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserLogin(APIView):

    permission_classes = [AllowAny]
    def post(self, request, format='json'):
        try:
            serializer = LoginSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

            user = serializer.validated_data

            token = Token.objects.get(user=user)

            response = {
                "status":"success",
                "token":token.key,
                "user" : UserSerializer(user).data
            }
            return Response (response , status=status.HTTP_202_ACCEPTED)
        
        except Exception as e:
            print(e)
            return Response({"errors" : "Something went wrong while saving User"}, status=status.HTTP_400_BAD_REQUEST)

    

@api_view(('POST','DELETE',))
@permission_classes([IsAdminUser])
def CreateItem(request,id):
    try:
        if request.method == 'POST':
            if MenuItem.objects.filter(item_id=id).exists():
                i = get_object_or_404(MenuItem, item_id=id)
                serializer = MenuItemSerializer(i, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            else:
                cat_name = request.data.pop("category")
                cat_inst, created = Category.objects.get_or_create(category_name=cat_name)
                c, created = MenuItem.objects.get_or_create(item_id=id,category=cat_inst)#,context={'request': request})
                #request['item_id'] =
                print("cc",c,c.category)
            
                #products_instance = Products.objects.create(**validated_data,category=cat_inst)
                
                serializer = MenuItemSerializer(c,data=request.data)
                
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
             
        elif request.method == 'DELETE':
            i = get_object_or_404(MenuItem, item_id=id)
            i.delete()
            return Response("Item Deleted", status=status.HTTP_200_OK)


        else:
            context = {}
            context['method'] = request.method
            return Response({'detail': context}, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        context = {}
        context['details'] = str(e)
        return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(('POST', ))
@permission_classes([IsAdminUser])
def CreateCategory(request):
    try:
        if request.method == 'POST':
            serializer = CategoryFormSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors)

        else:
            context = {}
            context['method'] = request.method
            return Response({'detail': context}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        context = {}
        context['details'] = str(e)
        return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(('GET',))
@permission_classes([IsAuthenticated])
def CategoryView(request,categoryId=None):
    try:

        if request.method == "GET":
            if categoryId:
                c = Category.objects.get(id=categoryId)
                serializer = CategoryFormSerializer(c)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else: 

                if request.query_params.get('limit'): 
                    paginator = PageNumberPagination()
                    paginator.page_size = 10
                    m = MenuItem.objects.all().order_by('item_id')
                    result_page = paginator.paginate_queryset(m, request) 
                    serializer = MenuItemSerializer(m, many=True)
                    return paginator.get_paginated_response(serializer.data)

                else:
                    c = Category.objects.all()
                    serializer = CategoryFormSerializer(c, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)

           

        else:
            context = {}
            context['method'] = request.method
            return Response({'detail': context}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        context = {}
        context['details'] = str(e)
        return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

