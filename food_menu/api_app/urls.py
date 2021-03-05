from django.urls import path, include
from rest_framework.authtoken import views
from .views import *


urlpatterns = [
    path('users/', UserCreate.as_view(), name='account-create'),
    path('login/', UserLogin.as_view(), name='account-login'),
    path('category/', CreateCategory, name='categories'),
    path('menu/<int:categoryId>', CategoryView, name='categories_view'),
    path('menu/', CategoryView, name='menu_view'),

    path('item/<int:id>', CreateItem, name='add-item'),

]