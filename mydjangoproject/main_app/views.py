from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView

from .forms import AddPostForm, UploadFileForm
from .models import Posts, Category, TagPost, UploadFiles

import uuid

menu = [
    {'title': "Главная страница", 'url_name': 'main'},
    {'title': "Добавить статью", 'url_name': 'addpage'},
    {'title': "О сайте", 'url_name': 'about'},
    {'title': "Войти", 'url_name': 'login'},
]


# def main_page(request):
#     posts = Posts.published.all().select_related('cat')
#
#     data = {
#         'title': 'Главная страница',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': 0,
#     }
#
#     return render(request, 'main_app/main.html', context=data)


class MainPage(ListView):
    # model = Posts
    template_name = 'main_app/main.html'
    context_object_name = 'posts'
    extra_context = {
        'title': 'Главная страница',
        'menu': menu,
        'cat_selected': 0,
    }

    def get_queryset(self):
        return Posts.published.all().select_related('cat')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Главная страница'
    #     context['menu'] = menu
    #     context['posts'] = Posts.published.all().select_related('cat'),
    #     context['cat_selected'] = int(self.request.GET.get('cat_id', 0))
    #     return context


# def handle_uploaded_file(f):
#     file_name, file_extension = f.name.split('.')
#     with open(f"uploads/{file_name}-{uuid.uuid4()}.{file_extension}", "wb+") as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)


def about(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # handle_uploaded_file(form.cleaned_data['file'])
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()

    data = {
        'title': 'О сайте',
        'menu': menu,
        'form': form,
    }

    return render(request, 'main_app/about.html', context=data)


# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             # try:
#             #     Posts.objects.create(**form.cleaned_data)
#             #     return redirect('main')
#             # except:
#             #     form.add_error(None, 'Ошибка добавления поста')
#             form.save()
#             return redirect('main')
#     else:
#         form = AddPostForm()
#
#     data = {
#         'title': 'Добавить статью',
#         'menu': menu,
#         'form': form,
#     }
#
#     return render(request, 'main_app/addpage.html', context=data)


class AddPage(FormView):
    form_class = AddPostForm
    template_name = 'main_app/addpage.html'
    success_url = reverse_lazy('main')  # reverse_lazy позволяет выстраивать маршрут лишь тогда когда он будет необходим
    extra_context = {
        'title': 'Добавить статью',
        'menu': menu,
    }

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

# class AddPage(View):
#     def get(self, request):
#         form = AddPostForm()
#
#         data = {
#             'title': 'Добавить статью',
#             'menu': menu,
#             'form': form,
#         }
#
#         return render(request, 'main_app/addpage.html', context=data)
#
#     def post(self, request):
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('main')
#
#         data = {
#             'title': 'Добавить статью',
#             'menu': menu,
#             'form': form,
#         }
#
#         return render(request, 'main_app/addpage.html', context=data)


# def show_post(request, post_slug):
#     posts = get_object_or_404(Posts, slug=post_slug)
#
#     data = {
#         'title': posts.title,
#         'menu': menu,
#         'post': posts,
#         'cat_selected': 1,
#     }
#
#     return render(request, 'main_app/post.html', data)


class ShowPost(DetailView):
    model = Posts
    template_name = 'main_app/post.html'
    slug_url_kwarg = 'post_slug'  # заменяем дефолт slug/pk на свой
    context_object_name = 'post'  # заменяем дефолт object на свой

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post'].title
        context['menu'] = menu
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Posts.published, slug=self.kwargs[self.slug_url_kwarg])


def login(request):
    return render(request, 'base.html')


# def show_category(request, cat_slug):
#     category = get_object_or_404(Category, slug=cat_slug)
#     posts = Posts.published.filter(cat_id=category.pk).select_related('cat')
#
#     data = {
#         'title': f'Рубрика: {category.name}',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': category.pk,
#     }
#
#     return render(request, 'main_app/main.html', context=data)


class PostsCategory(ListView):
    template_name = 'main_app/main.html'
    # в html шаблоне обращение идёт к posts,
    # если не указать этот атрибут context_object_name тогда по дефолту нужно указывать - object_list
    context_object_name = 'posts'
    allow_empty = False  # для отображения ошибки 404 при пустом списке

    def get_queryset(self):
        self.cat = get_object_or_404(Category, slug=self.kwargs['cat_slug'])
        return self.cat.post.filter(is_published=1).select_related('cat')
        # return Posts.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # cat = context['posts'][0].cat
        context['title'] = f'Категория - {self.cat.name}'
        context['menu'] = menu
        context['cat_selected'] = self.cat.pk
        return context


# def show_tag_postlist(request, tag_slug):
#     tag = get_object_or_404(TagPost, slug=tag_slug)
#     posts = tag.tags.filter(is_published=Posts.Status.PUBLISHED).select_related('cat')
#
#     data = {
#         'title': f'Тег: {tag.tag}',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': None,
#     }
#
#     return render(request, 'main_app/main.html', context=data)


class PostsTagPostList(ListView):
    template_name = 'main_app/main.html'
    # в html шаблоне обращение идёт к posts,
    # если не указать этот атрибут context_object_name тогда по дефолту нужно указывать - object_list
    context_object_name = 'posts'
    allow_empty = False  # для отображения ошибки 404 при пустом списке

    def get_queryset(self):
        self.tag = get_object_or_404(TagPost, slug=self.kwargs['tag_slug'])
        return self.tag.tags.filter(is_published=1).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Посты с тегом - {self.tag.tag}'
        context['menu'] = menu
        context['cat_selected'] = None
        return context


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
