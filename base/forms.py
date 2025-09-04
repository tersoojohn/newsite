from django.forms import ModelForm
from .models import NewsPage


class PageForm(ModelForm):
    model = NewsPage
    fields = "__all__"