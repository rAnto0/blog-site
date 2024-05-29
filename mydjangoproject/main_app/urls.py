from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main'),
    path('login/', views.login, name='login'),
    path('about/', views.about, name='about'),
    path('addpage/', views.addpage, name='addpage'),
    path('post/<slug:post_slug>/', views.show_post, name='post'),
    path('category/<slug:cat_slug>/', views.show_category, name='category'),
    path('tag/<slug:tag_slug>/', views.show_tag_postlist, name='tag'),
]
