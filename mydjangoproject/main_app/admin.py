from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import Posts, Category


class AdditionalInfoFilter(admin.SimpleListFilter):
    title = 'Статус доп информации'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('additional_info', 'Доп информация'),
            ('not_additional_info', 'Доп информация отсутствует')
        ]

    def queryset(self, request, queryset):
        if self.value() == 'additional_info':
            return queryset.filter(additional_info__isnull=False)
        elif self.value() == 'not_additional_info':
            return queryset.filter(additional_info__isnull=True)


@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'content', 'photo', 'post_photo', 'cat', 'additional_info', 'tags']
    # exclude = ['tags', 'is_published']
    readonly_fields = ['post_photo']
    prepopulated_fields = {'slug': ('title', )}
    filter_horizontal = ['tags']
    # filter_vertical = ['tags']
    list_display = ('title', 'post_photo', 'time_create', 'is_published', 'cat')
    list_display_links = ('title', )
    ordering = ['time_create', 'title']
    list_editable = ('is_published', )
    list_per_page = 10
    actions = ['set_published', 'set_draft']
    search_fields = ['title', 'cat__name']
    list_filter = [AdditionalInfoFilter, 'cat__name', 'is_published']
    save_on_top = True

    @admin.display(description='Изображение', ordering='content')
    def post_photo(self, post: Posts):
        if post.photo:
            return mark_safe(f'<img src="{post.photo.url}" width=50>')
        return 'Без фото'

    @admin.action(description='Опубликовать выбранные записи')
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Posts.Status.PUBLISHED)
        self.message_user(request, f'{count} записи опубликовано')

    @admin.action(description='Снять с публикации выбранные записи')
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Posts.Status.DRAFT)
        self.message_user(request, f'{count} записи сняты с публикации!', messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
