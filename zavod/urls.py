from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.main, name='main'),
    url(r'^prajjsy/$', views.prajjsy, name='prajjsy'),
    url(r'^articles/$', views.articles, name='articles'),
    url(r'^contacts/$', views.contacts, name='contacts'),
    url(r'^dostavka/$', views.dostavka, name='dostavka'),
    url(r'^dokumentatsija/$', views.dokumentatsija, name='dokumentatsija'),
    url(r'^catalog/$', views.catalog, name='catalog'),
]