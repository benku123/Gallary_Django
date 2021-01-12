from django.contrib import admin
from .models import *

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'id')
    list_display_links = ('title',)

@admin.register(Review)
class Review(admin.ModelAdmin):
    list_display = ('post', 'name', 'email')
    list_display_links = ('post',)


