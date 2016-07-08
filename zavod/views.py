from django.shortcuts import render, get_object_or_404
from .models import Article, CategoryProduct
from django.http import HttpResponse, HttpResponsePermanentRedirect

def main(request):
	return render(request, 'zavod/main.html')

def articles(request):
	return render(request, 'zavod/articles.html')

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
	return render(request, 'zavod/catalog.html')

def catalog_category(request):
	path_catalog = str(request.path.replace('articles', '').replace('/', ''))
	category = get_object_or_404(CategoryProduct, slug=path_catalog)
	return render(request, 'zavod/catalog_category.html', {'category': category})

def contacts(request):
	return render(request, 'zavod/contacts.html')

def prajjsy(request):
	return render(request, 'zavod/prajjsy.html')

def dostavka(request):
	return render(request, 'zavod/dostavka.html')

def dokumentatsija(request):
	return render(request, 'zavod/dokumentatsija.html')
