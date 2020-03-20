from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='facebook-home'),
    path('', views.create_first_post, name='facebook-create-post'),

]