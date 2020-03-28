from django.urls import path,include
from . import views
from django.conf.urls import url


urlpatterns = [
    path('home/', views.home, name='facebook-home'),
    path('create_post/', views.create_post, name='facebook-create-post'),
    url(r'^connent/(?P<operation>.+)/(?P<pk>\d+)/$', views.confirm_friend, name='confirm_friend'),

]

