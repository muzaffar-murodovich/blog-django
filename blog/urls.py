from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='home'),
    path('post/new/', views.PostCreateView.as_view(), name='add_post'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('category/<slug:slug>/', views.CategoryPostListView.as_view(), name='category_posts'),
    path('tag/<slug:slug>/', views.TagPostListView.as_view(), name='tag_posts'),
    path('post/<slug:slug>/update/', views.PostUpdateView.as_view(), name='update_post'),
    path('post/<slug:slug>/delete/', views.PostDeleteView.as_view(), name='delete_post'),
]