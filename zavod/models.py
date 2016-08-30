# -*- coding: utf-8 -*-
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User, UserManager, AbstractBaseUser
from django.contrib.postgres.fields import JSONField


class CustomUser(AbstractBaseUser):
    email = models.EmailField(max_length=50, unique=True)
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50, default='')
    last_name = models.CharField(max_length=50, default='')

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        return True

    def get_short_name(self):
        return self.email


class Tag(models.Model):
    title = models.CharField(max_length=100)


class Article(models.Model):
    published = models.BooleanField(default=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, default='', unique=True)
    preview_post = models.TextField(max_length=200)
    text = models.TextField()
    date_created = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100)
    seo_title = models.CharField(max_length=100, default='')
    seo_description = models.CharField(max_length=100, default='')
    seo_keywords = models.CharField(max_length=100, default='')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('articles_detail', args=[self.slug])

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class News(models.Model):
    published = models.BooleanField(default=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, default='', unique=True)
    preview_post = models.TextField(max_length=200)
    text = models.TextField()
    date_created = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100)
    seo_title = models.CharField(max_length=100, default='')
    seo_description = models.CharField(max_length=100, default='')
    seo_keywords = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('news_detail', args=[self.slug])

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


class ArticleTag(models.Model):
    article = models.ForeignKey(Article)
    tag = models.ForeignKey(Tag)


class NewsTag(models.Model):
    news = models.ForeignKey(News)
    tag = models.ForeignKey(Tag)


class ArticleImage(models.Model):
    article = models.ForeignKey(Article)
    article_image = models.FileField(upload_to='media/articles/', blank=True, null=True)


class NewsImage(models.Model):
    news = models.ForeignKey(News)
    news_image = models.FileField(upload_to='media/news/', blank=True, null=True)


class CategoryProduct(models.Model):
    published = models.BooleanField(default=True)
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, default='', unique=True)
    parent_id = models.ForeignKey("CategoryProduct", default=None, null=True, blank=True)
    title = models.CharField(max_length=100, default='')
    text = models.TextField(default='')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog_category', args=[self.slug])

    class Meta:
        verbose_name = 'Категория продуктов'
        verbose_name_plural = 'Категории продуктов'


class Product(models.Model):
    published = models.BooleanField(default=True)
    name = models.CharField(max_length=100, default='')
    slug = models.SlugField(max_length=100, default='', unique=True)
    category = models.ForeignKey(CategoryProduct)
    product_text = models.TextField()
    title = models.CharField(max_length=100, default='')
    seo_title = models.CharField(max_length=100, default='')
    seo_description = models.CharField(max_length=100, default='')
    seo_keywords = models.CharField(max_length=100, default='')
    properties = JSONField(default='')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('get_product', args=[self.slug])

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Image(models.Model):
    title = models.CharField(max_length=100)
    image = models.FileField(upload_to='media/images/', blank=True, null=True)


class CategoryImage(models.Model):
    category = models.ForeignKey(CategoryProduct)
    category_image = models.ForeignKey(Image)


class ProductImage(models.Model):
    product = models.ForeignKey(Product)
    product_image = models.ForeignKey(Image, blank=True, null=True)


class File(models.Model):
    title = models.CharField(max_length=100)
    file_content = models.FileField(upload_to='media/files/', blank=True, null=True)


class CategoryFile(models.Model):
    category = models.ForeignKey(CategoryProduct)
    category_file = models.ForeignKey(File)


class Gallery(models.Model):
    published = models.BooleanField(default=True)
    type = models.CharField(max_length=100, default='')
    name = models.CharField(max_length=100, default='')
    slug = models.SlugField(max_length=100, default='', unique=True)
    text = models.TextField()
    title = models.CharField(max_length=100, default='')
    seo_title = models.CharField(max_length=100, default='')
    seo_description = models.CharField(max_length=100, default='')
    seo_keywords = models.CharField(max_length=100, default='')
    date_created = models.DateTimeField(auto_now=True)
    cover_image = models.ForeignKey('GalleryImage', default=None, blank=True, null=True, related_name='cover_image')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/people/%i/" % self.id


class GalleryImage(models.Model):
    gallery = models.ForeignKey(Gallery)
    gallery_image = models.FileField(upload_to='media/gallery/', blank=True, null=True)
