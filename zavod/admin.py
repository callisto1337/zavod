from django.contrib import admin

from .models import Article, CategoryProduct, Product, CustomUser


class CategoryProductFields(admin.ModelAdmin):
    list_display = ('name', 'slug', 'published')
admin.site.register(CategoryProduct, CategoryProductFields)


class ArticleFields(admin.ModelAdmin):
    list_display = ('name', 'date_created', 'published')
admin.site.register(Article, ArticleFields)


class ProductFields(admin.ModelAdmin):
    list_display = ('name', 'category', 'published')
admin.site.register(Product, ProductFields)


class CustomUserFields(admin.ModelAdmin):
    list_display = ('email', 'is_superuser')
admin.site.register(CustomUser, CustomUserFields)
