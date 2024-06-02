from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from .forms import AddPostForm, UploadFileForm
from .models import Posts, Category, TagPost

import uuid

menu = [
    {'title': "Главная страница", 'url_name': 'main'},
    {'title': "Добавить статью", 'url_name': 'addpage'},
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


def handle_uploaded_file(f):
    file_name, file_extension = f.name.split('.')
    with open(f"mydjangoproject/uploads/{file_name}-{uuid.uuid4()}.{file_extension}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def about(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(form.cleaned_data['file'])
    else:
        form = UploadFileForm()

    data = {
        'title': 'О сайте',
        'menu': menu,
        'form': form,
    }

    return render(request, 'main_app/about.html', context=data)


def addpage(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            # try:
            #     Posts.objects.create(**form.cleaned_data)
            #     return redirect('main')
            # except:
            #     form.add_error(None, 'Ошибка добавления поста')
            form.save()
            return redirect('main')
    else:
        form = AddPostForm()

    data = {
        'title': 'Добавить статью',
        'menu': menu,
        'form': form,
    }

    return render(request, 'main_app/addpage.html', context=data)


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
