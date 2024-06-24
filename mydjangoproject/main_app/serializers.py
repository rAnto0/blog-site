import io

from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from .models import Posts


# class PostsModel:
#     def __init__(self, title, content):
#         self.title = title
#         self.content = content


class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = "__all__"

# def encode():
#     model = PostsModel('Пост 5', 'Content: Пост 5')
#     model_sr = PostsSerializer(model)
#     print(model_sr.data, type(model_sr.data), sep='\n')
#     json = JSONRenderer().render(model_sr.data)
#     print(json)


# def decode():
#     stream = io.BytesIO(
#         b'{"title":"\xd0\x9f\xd0\xbe\xd1\x81\xd1\x82 5","content":"Content: \xd0\x9f\xd0\xbe\xd1\x81\xd1\x82 5"}')
#     data = JSONParser().parse(stream)
#     serializer = PostsSerializer(data=data)
#     serializer.is_valid()
#     print(serializer.validated_data)
