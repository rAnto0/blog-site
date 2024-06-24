from rest_framework import generics

from .models import Posts
from .serializers import PostsSerializer


class PostsAPIList(generics.ListCreateAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer


class PostsAPIUpdate(generics.UpdateAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer


class PostsAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer
