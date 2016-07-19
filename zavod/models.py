# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User, UserManager, AbstractBaseUser


class CustomUser(AbstractBaseUser):
    email = models.EmailField(max_length=50, unique=True)
    username = models.CharField(max_length=50, unique=True)

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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class ArticleImage(models.Model):
    article = models.ForeignKey(Article)
    article_image = models.FileField(upload_to='media/articles/', blank=True, null=True)


class CategoryProduct(models.Model):
    published = models.BooleanField(default=True)
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, default='', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория продуктов'
        verbose_name_plural = 'Категории продуктов'


class SubCategoryProduct(models.Model):
    published = models.BooleanField(default=True)
    name = models.CharField(max_length=100, default='')
    category = models.ForeignKey(CategoryProduct)
    slug = models.SlugField(max_length=100, default='', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Вложенная категория'
        verbose_name_plural = 'Вложенные категории'


class Product(models.Model):
    published = models.BooleanField(default=True)
    name = models.CharField(max_length=100, default='')
    slug = models.SlugField(max_length=100, default='', unique=True)
    category = models.ForeignKey(CategoryProduct)
    subcategory = models.ForeignKey(SubCategoryProduct, null=True, blank=True)
    product_text = models.TextField()
    title = models.CharField(max_length=100, default='')
    seo_title = models.CharField(max_length=100, default='')
    seo_description = models.CharField(max_length=100, default='')
    seo_keywords = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class ProductImage(models.Model):
    article = models.ForeignKey(Product)
    product_image = models.FileField(upload_to='media/products/', blank=True, null=True)
