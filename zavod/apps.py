from django.apps import AppConfig
from watson import search as watson


class ZavodConfig(AppConfig):
    name = 'zavod'

    def ready(self):
        Article = self.get_model("Article")
        News = self.get_model("News")
        CategoryProduct = self.get_model("CategoryProduct")
        Product = self.get_model("Product")
        Gallery = self.get_model("Gallery")
        watson.register(Article)
        watson.register(News)
        watson.register(CategoryProduct)
        watson.register(Product)
        watson.register(Gallery)
