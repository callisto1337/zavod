from django.shortcuts import render


def main(request):
	return render(request, 'zavod/main.html')

def articles(request):
	return render(request, 'zavod/articles.html')

# def articles_detail(request):
# 	return render(request, 'zavod/articles_detail.html')

def contacts(request):
	return render(request, 'zavod/contacts.html')

def prajjsy(request):
	return render(request, 'zavod/prajjsy.html')

def dostavka(request):
	return render(request, 'zavod/dostavka.html')

def dokumentatsija(request):
	return render(request, 'zavod/dokumentatsija.html')

def catalog(request):
	return render(request, 'zavod/catalog.html')
