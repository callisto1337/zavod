from django.db import models
from django.utils import timezone


class Article(models.Model):
	name = models.CharField(max_length = 100)
	slug = models.SlugField(max_length = 100, default='', unique=True)
	preview_post = models.TextField(max_length = 200)
	text = models.TextField()
	date_created = models.DateTimeField(default=timezone.now)
	seo_title = models.CharField(max_length = 100, default='')
	seo_description = models.CharField(max_length = 100, default='')
	seo_keywords = models.CharField(max_length = 100, default='')
	def __str__(self):
		return self.name

class ArticleImage(models.Model):
	article = models.ForeignKey(Article)
	article_image = models.FileField(upload_to='media/articles/', blank=True, null=True)


class CategoryProduct(models.Model):
	name = models.CharField(max_length=50)
	slug = models.SlugField(max_length = 100, default='')
	def __str__(self):
		return self.name

class Product(models.Model):
	name = models.CharField(max_length = 100, default='')
	slug = models.SlugField(max_length = 100, default='')
	product_category = models.ForeignKey(CategoryProduct)
	product_text = models.TextField()
	seo_title = models.CharField(max_length = 100, default='')
	seo_description = models.CharField(max_length = 100, default='')
	seo_keywords = models.CharField(max_length = 100, default='')
	def __str__(self):
	    return self.name

class SubProduct(models.Model):
	name = models.CharField(max_length = 100, default='')
	product = models.ForeignKey(Product)
	slug = models.SlugField(max_length = 100, default='')
	product_category = models.ForeignKey(CategoryProduct)
	product_text = models.TextField()
	seo_title = models.CharField(max_length = 100, default='')
	seo_description = models.CharField(max_length = 100, default='')
	seo_keywords = models.CharField(max_length = 100, default='')
	def __str__(self):
	    return self.name

class ProductImage(models.Model):
	article = models.ForeignKey(Product)
	product_image = models.FileField(upload_to='media/products/', blank=True, null=True)