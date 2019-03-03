from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from bs4 import BeautifulSoup
import requests


def index(request):
        return render(request, 'frontend/index.html')
