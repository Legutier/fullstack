# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Category, Book
from django.shortcuts import render
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup
# Create your views here.

def index(request):
    return HttpResponse('Hello, world!')


"""
Returns all the books from every category scrapped
"""
def getScrapper(request):
    counter = 0
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
        query.save()
        counter += len(scrap_category(query,url+categories.get(category)))
        print(counter)
    print(counter)

    return HttpResponse(counter)

"""
Scraps through every book in specified category.
Returns a book list.
"""
def scrap_category(category_query,url):
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
            model = Book(category = category_query,
             title = book_soup.find('h1').get_text(),
             thumbnail = 'http://books.toscrape.com/'+book_soup.find('img')['src'],
             price = float(book_table[2].find('td').get_text()[1:]),
             stock = get_stock(book_table[5].find('td').get_text()) ,
             description = get_description(book_soup.find
                                            (id='product_description')),
             UPC = book_table[0].find('td').get_text(),
            )
            book_list.append(model)
        runs -= 1
    return book_list


"""
Gets the stock of desired book in scraper
"""
def scrap_stock(stock_str):
    stock_list = stock_str.replace('(','').split()
    for str in stock_list:
        if str.isdigit():
            return int(str)
    return 0


"""
Gets the description of desired book in scraper
"""
def scrap_description(book_soup):
    if book_soup is None:
        return 'None'
    else:
        return book_soup.next_sibling.next_sibling.get_text()
