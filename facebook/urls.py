from django.urls import path
from . import views
from .views import PostListView,PostDetailView,PostCreateView

urlpatterns = [
    # path('home/', views.home, name='facebook-home'),
    path('home/', PostListView.as_view(), name='facebook-home'),
    path('post/<int:pk>', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('create_post/', views.create_post, name='facebook-create-post'),

]