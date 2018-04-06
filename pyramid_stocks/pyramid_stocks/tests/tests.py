

def test_default_behavior_of_portfolio_view(dummy_request):
    from ..views.default import portfolio_view

    response = portfolio_view(dummy_request)
    assert type(response) == dict
    assert response['entries'][0]['symbol'] == 'GE'


def test_jeremy_is_awesome():
    assert True
