from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Posts, Category
from .serializers import PostsSerializer


class PostsViewSet(viewsets.ModelViewSet):
    # queryset = Posts.objects.all()
    serializer_class = PostsSerializer

    def get_queryset(self):
        pk = self.kwargs.get("pk")

        if not pk:
            return Posts.objects.all()[:3]

        return Posts.objects.filter(pk=pk)

    @action(methods=['get'], detail=True)
    def category(self, request, pk=None):
        cats = Category.objects.get(pk=pk)
        return Response({'cats': cats.name})

# class PostsAPIList(generics.ListCreateAPIView):
#     queryset = Posts.objects.all()
#     serializer_class = PostsSerializer
#
#
# class PostsAPIUpdate(generics.UpdateAPIView):
#     queryset = Posts.objects.all()
#     serializer_class = PostsSerializer
#
#
# class PostsAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Posts.objects.all()
#     serializer_class = PostsSerializer
