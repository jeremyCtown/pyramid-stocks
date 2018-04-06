
def test_default_behavior_of_home_view(dummy_request):
    from ..views.default import home_view

    response = home_view(dummy_request)
    assert type(response) == dict
    assert response == {}


def test_default_behavior_of_auth_view(dummy_request):
    from ..views.default import auth_view

    response = auth_view(dummy_request)
    assert type(response) == dict
    assert response == {}


def test_default_behavior_of_stock_view(dummy_request):
    from ..views.default import stock_view

    response = stock_view(dummy_request)
    assert type(response) == dict
    assert response == {}


def test_default_behavior_of_portfolio_view(dummy_request):
    from ..views.default import portfolio_view

    response = portfolio_view(dummy_request)
    assert type(response) == dict
    assert response['entries'][0]['symbol'] == 'GE'


def test_jeremy_is_awesome():
    assert True
