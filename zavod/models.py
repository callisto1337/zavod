from django.db import models
from django.utils import timezone


class Article(models.Model):
	slug = models.CharField(max_length = 100, default='')
	title = models.CharField(max_length = 100)
	preview_post = models.TextField(max_length = 200)
	text = models.TextField()
	date_created = models.DateTimeField(default=timezone.now)
	def __str__(self):
		return self.title

class ArticleImage(models.Model):
	article = models.ForeignKey(Article)
	article_image = models.FileField(upload_to='media/articles/', blank=True, null=True)


class CategoryProduct(models.Model):
	slug = models.CharField(max_length = 100, default='')
	category_name = models.CharField(max_length=50)
	def __str__(self):
		return self.category_name

class Product(models.Model):
	product_category = models.ForeignKey(CategoryProduct)
	product_title = models.CharField(max_length=50)
	product_text = models.TextField()
	def __str__(self):
	    return self.product_title

class ProductImage(models.Model):
	article = models.ForeignKey(Product)
	product_image = models.FileField(upload_to='media/products/', blank=True, null=True)