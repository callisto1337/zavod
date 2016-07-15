from django.contrib import admin
from .models import Article, ArticleImage, CategoryProduct, Product, SubCategoryProduct


admin.site.register(CategoryProduct)
admin.site.register(SubCategoryProduct)

class ArticleFields(admin.ModelAdmin):
	list_display = ('name', 'date_created')
admin.site.register(Article, ArticleFields)

class ProductFields(admin.ModelAdmin):
	list_display = ('name', 'subcategory', 'category')
admin.site.register(Product, ProductFields)