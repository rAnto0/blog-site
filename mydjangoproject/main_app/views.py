from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render

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
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': data_db,
    }
    return render(request, 'main_app/main.html', context=data)


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


def about(request):
    data = {
        'title': 'О сайте',
        'menu': menu,
    }
    return render(request, 'main_app/about.html', context=data)


def show_post(request, post_id):
    return HttpResponse(f'Отображение статьи с id = {post_id}')


def login(request):
    return render(request, 'base.html')
