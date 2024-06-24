from django.forms import model_to_dict
from rest_framework import generics
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Posts
from .serializers import PostsSerializer


class PostsAPIList(generics.ListCreateAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer


class PostsAPIView(APIView):
    def get(self, request):
        p = Posts.objects.all()

        return Response({'posts': PostsSerializer(p, many=True).data})

    def post(self, request):
        serializer = PostsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'post': serializer.data})

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Method PUT not allowed'})

        try:
            instance = Posts.objects.get(pk=pk)
        except:
            return Response({'error': 'Object does not exists'})

        serializer = PostsSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'post': serializer.data})

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Method DELETE not allowed'})

        try:
            instance = Posts.objects.get(pk=pk)
            instance.delete()
            return Response({'post': f'Object {pk} is deleted'})
        except:
            return Response({'error': 'Object does not exists'})

# class PostsAPIView(generics.ListAPIView):
#     queryset = Posts.objects.all()
#     serializer_class = PostsSerializer
