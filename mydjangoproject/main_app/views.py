from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response

from .models import Posts, Category
from .permissions import IsAdminOrReadOnlu, IsOwnerOrReadOnly
from .serializers import PostsSerializer


class PostsAPIList(generics.ListCreateAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )


class PostsAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer
    permission_classes = (IsOwnerOrReadOnly, )


class PostsAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer
    permission_classes = (IsAdminOrReadOnlu, )
