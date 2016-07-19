from django.contrib import admin
from .models import Article, ArticleImage, CategoryProduct, Product, SubCategoryProduct, CustomUser


class CategoryProductFields(admin.ModelAdmin):
    list_display = ('name', 'slug', 'published')
admin.site.register(CategoryProduct, CategoryProductFields)


class SubCategoryFields(admin.ModelAdmin):
    list_display = ('name', 'category', 'slug', 'published')
admin.site.register(SubCategoryProduct, SubCategoryFields)


class ArticleFields(admin.ModelAdmin):
    list_display = ('name', 'date_created', 'published')
admin.site.register(Article, ArticleFields)


class ProductFields(admin.ModelAdmin):
    list_display = ('name', 'subcategory', 'category', 'published')
admin.site.register(Product, ProductFields)


class CustomUserFields(admin.ModelAdmin):
    list_display = ('email', 'is_superuser')
admin.site.register(CustomUser, CustomUserFields)
