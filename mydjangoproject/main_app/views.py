from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Posts, Category, TagPost

menu = [
    {'title': "Главная страница", 'url_name': 'main'},
    {'title': "О сайте", 'url_name': 'about'},
    {'title': "Войти", 'url_name': 'login'},
]


def main_page(request):
    posts = Posts.published.all().select_related('cat')

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
    posts = Posts.published.filter(cat_id=category.pk).select_related('cat')

    data = {
        'title': f'Рубрика: {category.name}',
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk,
    }

    return render(request, 'main_app/main.html', context=data)


def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=Posts.Status.PUBLISHED).select_related('cat')

    data = {
        'title': f'Тег: {tag.tag}',
        'menu': menu,
        'posts': posts,
        'cat_selected': None,
    }

    return render(request, 'main_app/main.html', context=data)


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
