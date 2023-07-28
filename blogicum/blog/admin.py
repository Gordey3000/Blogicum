from django.contrib import admin

from .models import Category, Location, Post


class PostInline(admin.StackedInline):
    model = Post
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = (
        PostInline,
    )


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    inlines = (
        PostInline,
    )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'pub_date',
        'author',
        'location',
        'category',
        'is_published',
        'created_at'
    )
    list_editable = (
        'is_published',
        'category',
        'pub_date'
    )
    search_fields = ('title',)
    list_filter = ('category',)
    list_display_links = ('title',)
