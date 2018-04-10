from pyramid.view import view_config
from pyramid.response import Response
from . import DB_ERR_MSG
from sqlalchemy.exc import DBAPIError
from models import Stock
from ..sample_data import MOCK_DATA
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
import requests
from pyramid.security import NO_PERMISSION_REQUIRED

API_URL = 'https://api.iextrading.com/1.0'

@view_config(
    route_name='home',
    renderer='../templates/index.jinja2',
    request_method='GET')
def home_view(request):
    """
    Returns home view
    """
    return {}


@view_config(
    route_name='auth',
    renderer='../templates/login.jinja2')
def auth_view(request):
    """
    Returns login page
    """
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
    renderer='../templates/stock-detail.jinja2')
def stock_view(request):
    """
    Returns search form for an individual stock
    """
    if request.method == 'GET':
        try:
            symbol = request.GET['symbol']
        except KeyError:
            return {}
        response = requests.get(API_URL + '/stock/{}/company'.format(symbol))
        data = response.json()
        return {'company': data}
    
    else:
        raise HTTPNotFound()


@view_config(
    route_name='portfolio',
    renderer='../templates/portfolio.jinja2')
def portfolio_view(request):
    """
    Returns portfolio view with MOCK_DATA
    """
    
    if request.method == 'GET':
        try:
            query = request.dbsession.query(Stock)
            all_entries = query.all()
        except DBAPIError:
            return DBAPIError(DB_ERR_MSG, content_type='text/plain', status=500)

        return {'entries': all_entries}


    # if request.method == 'GET':
    #     return {
    #         'entries': MOCK_DATA
    #     }

    # if request.method == 'POST':
    #     symbol = request.POST['symbol']
    #     response = requests.get(API_URL + '/stock/{}/company'.format(symbol))
    #     data = response.json()
    #     MOCK_DATA.append(data)
    #     return {'entries': MOCK_DATA}


@view_config(
    route_name='detail',
    renderer='../templates/portfolio-detail.jinja2',
    request_method='GET')
def portfolio_stock_view(request):
    """
    Shows individual stock
    """
    
    try:
        entry_id = request.matchdict['symbol']
    except IndexError:
        return HTTPNotFound()

    try:
        query = request.dbsession.query(Stock)
        stock_detail = query.filter(Stock.symbol == entry_id).first()
    except DBAPIError:
        return DBAPIError(DB_ERR_MSG, content_type='txt/plain', status=500)
    
    # res = requests.get
    
    
    # try:
    #     for entry in MOCK_DATA:
    #         if entry['symbol'] == request.matchdict['symbol']:
    #             return {'stock': entry}
    
    # except KeyError:
    #     return {}



