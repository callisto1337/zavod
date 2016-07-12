from django.contrib import admin
from .models import Article, ArticleImage, CategoryProduct, Product, SubProduct

admin.site.register(Article)
admin.site.register(CategoryProduct)
admin.site.register(Product)
admin.site.register(SubProduct)