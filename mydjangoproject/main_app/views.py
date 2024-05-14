from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Posts, Category

menu = [
    {'title': "Главная страница", 'url_name': 'main'},
    {'title': "О сайте", 'url_name': 'about'},
    {'title': "Войти", 'url_name': 'login'},
]

data_db = [
    {'id': 1, 'title': 'Что-то1', 'content': 'Подробности Что-то1', 'is_published': True},
    {'id': 2, 'title': 'Что-то2', 'content': 'Подробности Что-то2', 'is_published': False},
    {'id': 3, 'title': 'Что-то3', 'content': 'Подробности Что-то3', 'is_published': True},
]


def main_page(request):
    posts = Posts.published.all()

    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': posts,
        'cat_selected': 0,
    }

    return render(request, 'main_app/main.html', context=data)


def about(request):
    data = {
        'title': 'О сайте',
        'menu': menu,
    }

    return render(request, 'main_app/about.html', context=data)


def show_post(request, post_slug):
    posts = get_object_or_404(Posts, slug=post_slug)

    data = {
        'title': posts.title,
        'menu': menu,
        'post': posts,
        'cat_selected': 1,
    }

    return render(request, 'main_app/post.html', data)


def login(request):
    return render(request, 'base.html')


def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Posts.published.filter(cat_id=category.pk)

    data = {
        'title': f'Рубрика: {category.name}',
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk,
    }

    return render(request, 'main_app/main.html', context=data)


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
