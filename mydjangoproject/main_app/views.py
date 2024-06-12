from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView, DeleteView

from .forms import AddPostForm, UploadFileForm
from .models import Posts, Category, TagPost, UploadFiles

import uuid

from .utils import DataMixin


class MainPage(DataMixin, ListView):
    # model = Posts
    template_name = 'main_app/main.html'
    context_object_name = 'posts'
    title_page = 'Главная страница'
    cat_selected = 0

    def get_queryset(self):
        return Posts.published.all().select_related('cat')


@login_required
def about(request):
    contact_list = Posts.published.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    data = {
        'title': 'О сайте',
        'page_obj': page_obj,
    }

    return render(request, 'main_app/about.html', context=data)


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'main_app/addpage.html'
    title_page = 'Добавление статьи'

    def form_valid(self, form):
        p = form.save(commit=False)
        p.author = self.request.user
        return super().form_valid(form)


class UpdatePage(DataMixin, UpdateView):
    model = Posts
    fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = 'main_app/addpage.html'
    success_url = reverse_lazy('main')  # reverse_lazy позволяет выстраивать маршрут лишь тогда когда он будет нужен
    title_page = 'Редактирование статьи'


class DeletePage(DataMixin, DeleteView):
    model = Posts
    success_url = reverse_lazy('main')
    title_page = 'Удаление статьи'


class ShowPost(DataMixin, DetailView):
    template_name = 'main_app/post.html'
    slug_url_kwarg = 'post_slug'  # заменяем дефолт slug/pk на свой
    context_object_name = 'post'  # заменяем дефолт object на свой

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Posts.published, slug=self.kwargs[self.slug_url_kwarg])


def login(request):
    return render(request, 'base.html')


class PostsCategory(DataMixin, ListView):
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
        return self.get_mixin_context(context, title=f'Категория - {self.cat.name}', cat_selected=self.cat.pk)


class PostsTagPostList(DataMixin, ListView):
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
        return self.get_mixin_context(context, title=f'Посты с тегом - {self.tag.tag}')


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
