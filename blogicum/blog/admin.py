from django.contrib import admin

from .models import Category, Location, Post


class PostInline(admin.StackedInline):
    model = Post
    extra = 0


class CategoryAdmin(admin.ModelAdmin):
    inlines = (
        PostInline,
    )


class LocationAdmin(admin.ModelAdmin):
    inlines = (
        PostInline,
    )


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


admin.site.register(Category)
admin.site.register(Location)
admin.site.register(Post)
