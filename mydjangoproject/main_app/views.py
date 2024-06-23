from django.forms import model_to_dict
from rest_framework import generics
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Posts
from .serializers import PostsSerializer


class PostsAPIView(APIView):
    def get(self, request):
        p = Posts.objects.all()

        return Response({'posts': PostsSerializer(p, many=True).data})

    def post(self, request):
        serializer = PostsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        post_new = Posts.objects.create(
            title=request.data['title'],
            content=request.data['content'],
            cat_id=request.data['cat_id'],
        )

        return Response({'post': PostsSerializer(post_new).data})


# class PostsAPIView(generics.ListAPIView):
#     queryset = Posts.objects.all()
#     serializer_class = PostsSerializer
