from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main'),
    path('login/', views.login, name='login'),
    path('about/', views.about, name='about'),
    path('post/<int:post_id>/', views.show_post, name='post'),
    path('category/<int:cat_id>/', views.show_category, name='category'),
]
