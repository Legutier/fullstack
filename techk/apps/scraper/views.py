# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Category, Book
from django.core.exceptions import ObjectDoesNotExist
from .serializers import CategorySerializer, BookSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
import requests
from bs4 import BeautifulSoup
@permission_classes((AllowAny, ))
class Scraper(generics.ListCreateAPIView, generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def create(self,*args):
        self.perform_create()

    def perform_create(self):
        categories = dict()
        url = "http://books.toscrape.com/"
        page = requests.get(url)
        soup = BeautifulSoup(page.content,'html.parser').find(class_="sidebar")
        # Categories are scrapped first.
        for category in soup.find_all('a', href=True):
            if 'Books' not in category.get_text():
                categories[category.get_text().strip().replace('\n','')] = category['href']
        for category in categories:
            query = Category(name=category)
            try:
                object = Category.objects.get(name=category)
            except ObjectDoesNotExist:
                query.save()
            self.scrap_category(query,url+categories.get(category))
        return Response('Done')

    def scrap_category(self, category_query,url):
        print('scraping category: ' + category_query.name)
        #If it has a "next" link to scrap, 'runs' the scrapper once more.
        runs = 2
        page = requests.get(url)
        book_list = []
        #Scrapping category pages
        while(runs > 0):
            runs = 2
            content = page.content
            soup = BeautifulSoup(content, 'html.parser')
            books_area = soup.find(class_="page").find(class_="row").find('section')
            next_page = books_area.find(class_= "next")
            #Only runs once since is not neccesary to run again
            if  next_page is None:
                runs -= 1
            else:
                page = requests.get(url.replace('index.html',next_page.find('a')['href']))
            #Scrapping books
            books = books_area.find_all(class_="product_pod")
            for book  in books:
                bookurl = book.find('a')['href'].replace('../../../','')
                book_page = requests.get('http://books.toscrape.com/catalogue/'+bookurl)
                book_soup = BeautifulSoup(book_page.content, 'html.parser')
                book_soup = book_soup.find(class_="product_page")
                book_table = book_soup.find(class_="table").find_all('tr')
                #Model to make query
                code = book_table[0].find('td').get_text()
                model = Book(category = category_query,
                 title = book_soup.find('h1').get_text(),
                 thumbnail = 'http://books.toscrape.com/'+book_soup.find('img')['src'],
                 price = float(book_table[2].find('td').get_text()[1:]),
                 stock = self.scrap_stock(book_table[5].find('td').get_text()) ,
                 description = self.scrap_description(book_soup.find
                                                (id='product_description')),
                 UPC = code,
                )
                try:
                    object = Book.objects.get(UPC = code)
                except ObjectDoesNotExist:
                    model.save()
            runs -= 1

    """
    Gets the stock of desired book in scraper
    """
    def scrap_stock(self, stock_str):
        stock_list = stock_str.replace('(','').split()
        for str in stock_list:
            if str.isdigit():
                return int(str)
        return 0


    """
    Gets the description of desired book in scraper
    """
    def scrap_description(self, book_soup):
        if book_soup is None:
            return 'None'
        else:
            return book_soup.next_sibling.next_sibling.get_text()




#class CategoryList(generics.ListCreateAPIView, generics.DestroyAPIView):
#    serializer_class = BookSerializer
#    queryset = Book.objects.all()
