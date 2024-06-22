from rest_framework import generics
from django.shortcuts import render
from .models import Posts
from .serializers import PostsSerializer


class PostsAPIView(generics.ListAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer
