from django.contrib import admin
from .models import Article, ArticleImage, CategoryProduct, Product, SubCategoryProduct


class CategoryProductFields(admin.ModelAdmin):
    list_display = ('name', 'slug')
admin.site.register(CategoryProduct, CategoryProductFields)


class SubCategoryFields(admin.ModelAdmin):
    list_display = ('name', 'category', 'slug')
admin.site.register(SubCategoryProduct, SubCategoryFields)


class ArticleFields(admin.ModelAdmin):
    list_display = ('name', 'date_created')
admin.site.register(Article, ArticleFields)


class ProductFields(admin.ModelAdmin):
    list_display = ('name', 'subcategory', 'category')
admin.site.register(Product, ProductFields)
