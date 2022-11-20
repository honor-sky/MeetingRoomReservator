from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    #path('', views.Avaliable, name="avaliableroom"),
    path('postMember/', views.postMember, name="postMember"),
]