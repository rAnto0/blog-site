from django import template
import main_app.views as views
from main_app.models import Category


register = template.Library()


@register.inclusion_tag('main_app/list_categories.html')
def show_categories(cat_selected=0):
    cats = Category.objects.all()
    return {'cats': cats, 'cat_selected': cat_selected}
