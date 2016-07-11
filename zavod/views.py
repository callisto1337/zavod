from django.shortcuts import render, get_object_or_404
from .models import Article, CategoryProduct, Product
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
	articles = Article.objects.all()[:5]
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
	category_products = CategoryProduct.objects.all()[:5]
	return render(request, 'zavod/catalog.html', {'category_products': category_products})

def catalog_category(request):
	path_catalog = str(request.path.replace('catalog', '').replace('/', ''))
	product = get_object_or_404(Product, slug=path_catalog)
	return render(request, 'zavod/catalog_category.html', {'product': product})


# def catalog_category(request):
# 	path_catalog = str(request.path.replace('articles', '').replace('/', ''))
# 	category = get_object_or_404(CategoryProduct, slug=path_catalog)
# 	return render(request, 'zavod/catalog_category.html', {'category': category})
