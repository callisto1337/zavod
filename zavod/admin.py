from django.contrib import admin
from .models import Article, ArticleImage, CategoryProduct, Product

admin.site.register(Article)
# admin.site.register(ArticleImage)
admin.site.register(CategoryProduct)
admin.site.register(Product)