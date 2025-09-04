from django.contrib import admin
from .models import Category, NewsPage, User, Staff

# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(NewsPage)
admin.site.register(Staff)