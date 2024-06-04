from django.urls import path
from . import views

urlpatterns = [
    path('', views.MainPage.as_view(), name='main'),
    path('login/', views.login, name='login'),
    path('about/', views.about, name='about'),
    path('addpage/', views.AddPage.as_view(), name='addpage'),
    path('post/<slug:post_slug>/', views.show_post, name='post'),
    path('category/<slug:cat_slug>/', views.PostsCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', views.PostsTagPostList.as_view(), name='tag'),
]
