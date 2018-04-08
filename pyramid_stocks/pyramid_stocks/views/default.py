from pyramid.view import view_config
from ..sample_data import MOCK_DATA
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
import requests

API_URL = 'https://api.iextrading.com/1.0'

@view_config(
    route_name='home',
    renderer='../templates/index.jinja2',
    request_method='GET')
def home_view(request):
    return {}


@view_config(
    route_name='auth',
    renderer='../templates/login.jinja2')
def auth_view(request):
    if request.method == 'GET':
        try:
            username = request.GET['username']
            password = request.GET['password']
            print('User: {}, Pass: {}'.format(username, password))

            return HTTPFound(location=request.route_url('portfolio'))

        except KeyError:
            return {}

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        print('User: {}, Pass: {}, Email: {}'.format(username, password, email))

        return HTTPFound(location=request.route_url('portfolio'))

    return HTTPNotFound()


@view_config(
    route_name='stock',
    renderer='../templates/stock-detail.jinja2',
    request_method='GET')
def stock_view(request):
    if request.method == 'GET':
        try:
            symbol = request.GET['symbol']
            response = requests.get(API_URL + '/stock/{}/company'.format(symbol))
            data = response.json()
            return {'company': data}

        except KeyError:
            return {}

    else:
        raise HTTPNotFound()


@view_config(
    route_name='portfolio',
    renderer='../templates/portfolio.jinja2',
    request_method='GET')
def portfolio_view(request):
    return {
        'entries': MOCK_DATA
    }


@view_config(
    route_name='detail',
    renderer='../templates/portfolio-detail.jinja2',
    request_method='GET')
def portfolio_stock_view(request):
    try:
        for entry in MOCK_DATA:
            if entry['symbol'] == request.matchdict['symbol']:
                return {'stock': entry}
    
    except KeyError:
        return {}

