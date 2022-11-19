from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    #path('getavaliableroom/', views.getAvaliableRoom, name="test01datas"),
    path('postMember/', views.postMember, name="postMember"),
]