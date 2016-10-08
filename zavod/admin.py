from django.contrib import admin

from .models import Article, CategoryProduct, Product, CustomUser, Tag, Question, News, Image, Gallery, GalleryImage, \
    File, Employee


class CategoryProductFields(admin.ModelAdmin):
    list_display = ('name', 'slug', 'published')
admin.site.register(CategoryProduct, CategoryProductFields)


class ArticleFields(admin.ModelAdmin):
    list_display = ('title', 'date_created', 'published')
admin.site.register(Article, ArticleFields)


class ProductFields(admin.ModelAdmin):
    list_display = ('name', 'category', 'published')
admin.site.register(Product, ProductFields)


class CustomUserFields(admin.ModelAdmin):
    list_display = ('email', 'is_superuser')
admin.site.register(CustomUser, CustomUserFields)


class EmployeeFields(admin.ModelAdmin):
    list_display = ('name', 'first_name', 'last_name', 'position', 'published')
admin.site.register(Employee, EmployeeFields)


class TagFields(admin.ModelAdmin):
    list_display = ('title',)
admin.site.register(Tag, TagFields)


class QuestionFields(admin.ModelAdmin):
    list_display = ('text', 'answer', 'published')
admin.site.register(Question, QuestionFields)


class NewsFields(admin.ModelAdmin):
    list_display = ('title', 'date_created', 'published')
admin.site.register(News, NewsFields)


class ImageFields(admin.ModelAdmin):
    list_display = ('title', 'image')
admin.site.register(Image, ImageFields)


class FileFields(admin.ModelAdmin):
    list_display = ('title', 'file_content')
admin.site.register(File, FileFields)


class GalleryImageInline(admin.StackedInline):
    model = GalleryImage


class GalleryFields(admin.ModelAdmin):
    list_display = ('name', 'slug', 'published')
    inlines = [GalleryImageInline]
admin.site.register(Gallery, GalleryFields)
