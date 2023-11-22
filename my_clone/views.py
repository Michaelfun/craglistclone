import requests
from django.shortcuts import render
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from . import models

# Create your views here.

BASE_URL = 'https://losangeles.craigslist.org/d/services/search/?query={}'
BASE_IMAGE_URL = "https://images.craigslist.org/{}_300x300.jpg"


def home(request):
    """
    starting first base view
    """
    return render(request, 'base.html')


def new_search(request):
    """
    taking search inputs
    """
    search = request.POST.get('search')
    print(search)
    models.Search.objects.create(search_field=search)
    final_url = BASE_URL.format(quote_plus(search))
    responce = requests.get(final_url)
    data = responce.text
    soup = BeautifulSoup(data, features='html.parser')

    post_listing = soup.find_all('li', {'class': 'result-row'})

    final_posting=[]

    for post in post_listing:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'No Price'

        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
        else:
            post_image_url='https://craigslist.org/images/peace.jpg'

        final_posting.append((post_title, post_url, post_price, post_image_url))

    stuff_for_frontend = {

        'search': search,
        'final_posting': final_posting,
    }

    return render(request, 'my_clone/new_search.html', stuff_for_frontend)
