from django.http import HttpResponseNotFound
from django.shortcuts import render


def main_page(request):
    return render(request, 'main.html')


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
