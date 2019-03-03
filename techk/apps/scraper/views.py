# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Category, Book
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from .serializers import CategorySerializer, BookSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
import requests
from bs4 import BeautifulSoup

@permission_classes((AllowAny, ))
class Scraper(generics.ListCreateAPIView, generics.DestroyAPIView):

    """
    Scraper methord
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    def create(self,*args):
        """
        Overrided method
        """
        self.perform_create()
        return Response({'data':'scraper'},status=status.HTTP_201_CREATED)

    def perform_create(self):
        """
        POST(overrided) method, it does not need a body. Scraps categories,
        for each category calls scrap_category().

        Returns a Response when done.
        """
        categories = dict()
        url = "http://books.toscrape.com/"
        page = requests.get(url)
        soup = BeautifulSoup(page.content,'html.parser').find(class_="sidebar")
         #Categories are scrapped first.
        for category in soup.find_all('a', href=True):
            if 'Books' not in category.get_text():
                categories[category.get_text().strip().replace('\n','')] = category['href']
        for category in categories:
            query = Category(name=category)
            try:
                query_aux = Category.objects.get(name=category)
                query = query_aux
            except ObjectDoesNotExist:
                query.save()
            self.scrap_category(query,url+categories.get(category))
        return

    def scrap_category(self, category_query,url):
        """
        Scraps the category in order to get desired books.
        Inserts the books into DataBase
        """
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
                page = requests.get(url.replace('index.html',
                                    next_page.find('a')['href']))
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
                #Verifies if object doest not already exist.
                try:
                    model = Book.objects.get(UPC = code)
                except ObjectDoesNotExist:
                    try:
                        #If it does not exist, query is done.
                        model = Book(category = category_query,
                        title = book_soup.find('h1').get_text(),
                        thumbnail = ('http://books.toscrape.com/'
                                 + book_soup.find('img')['src']),
                        price = float(book_table[2].find('td').get_text()[1:]),
                        stock = self.scrap_stock(book_table[5].find('td').get_text()),
                        description = self.scrap_description(book_soup.find
                                                (id='product_description')),
                        UPC = code)
                        model.save()
                    except IntegrityError:
                        pass
            runs -= 1

    def scrap_stock(self, stock_str):
        """
        Gets the stock of desired book in scraper
        """
        stock_list = stock_str.replace('(','').split()
        for str in stock_list:
            if str.isdigit():
                return int(str)
        return 0

    def scrap_description(self, book_soup):
        """
        Gets the description of desired book in scraper
        """
        if book_soup is None:
            return 'None'
        else:
            return book_soup.next_sibling.next_sibling.get_text()
