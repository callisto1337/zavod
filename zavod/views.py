from django.shortcuts import render, get_object_or_404
from .models import Article, CategoryProduct, Product, SubCategoryProduct
from django.http import HttpResponse, HttpResponsePermanentRedirect

def main(request):
	return render(request, 'zavod/main.html')

def contacts(request):
	return render(request, 'zavod/contacts.html')

def prajjsy(request):
	return render(request, 'zavod/prajjsy.html')

def dostavka(request):
	return render(request, 'zavod/dostavka.html')

def dokumentatsija(request):
	return render(request, 'zavod/dokumentatsija.html')


def articles(request):
	articles = Article.objects.all().filter(published=True)[:5]
	return render(request, 'zavod/articles.html', {'articles': articles})

def articles_detail(request):
	path_article = str(request.path.replace('articles', '').replace('/', ''))
	try:
		int(path_article)
		article = get_object_or_404(Article, pk=path_article)
		return HttpResponsePermanentRedirect(article.slug)
	except:
		article = get_object_or_404(Article, slug=path_article)
		return render(request, 'zavod/articles_detail.html', {'article': article})


def catalog(request):
	category_products = CategoryProduct.objects.all().filter(published=True)[:5]
	return render(request, 'zavod/catalog.html', {'category_products': category_products})

def catalog_category(request):
	path_catalog = request.path.replace('/', ' ').split()
	category = get_object_or_404(CategoryProduct, slug=path_catalog[1])
	subcategory = SubCategoryProduct(slug=path_catalog[1])

	if SubCategoryProduct.objects.all().filter(category=category):
		title = 'Вложенные категории'
		subcategories = SubCategoryProduct.objects.all().filter(category=category, published=True)
		return render(request, 'zavod/catalog_category.html', {'subcategories': subcategories, 'title': title})
	else:
		title = 'Список продуктов'
		parent = get_object_or_404(CategoryProduct, slug=path_catalog[1])
		products = Product.objects.all().filter(category=parent, published=True)
		return render(request, 'zavod/catalog_category.html', {'products': products, 'parent': parent, 'title': title})

def product_or_products(request):
	path_product = request.path.replace('/', ' ').split()
	category = get_object_or_404(CategoryProduct, slug=path_product[1])

	if len(path_product) == 3:
		if Product.objects.all().filter(slug=path_product[2]):
			product = Product.objects.all().filter(slug=path_product[2], published=True)
			return render(request, 'zavod/product.html', {'product': product})
		else:
			title = 'Список продуктов во вложенной категории'
			subcategory_id = get_object_or_404(SubCategoryProduct, slug=path_product[2])
			products = Product.objects.all().filter(subcategory=subcategory_id, published=True)
			return render(request, 'zavod/catalog_category.html', {'products': products, 'title': title})
	else:
		subcategory = get_object_or_404(SubCategoryProduct, slug=path_product[2])
		product = get_object_or_404(Product, slug=path_product[3])
		return render(request, 'zavod/product.html', {'product': product})