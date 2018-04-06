
def test_default_behavior_of_base_view(dummy_request):
    from ..views.default import home_view
    from pyramid.response import Response

    request = dummy_request
    response = home_view(request)
    # import pdb ; pdb.set_trace()
    assert isinstance(response, Response)
    assert response.text == 'I did a thing'


def test_default_behavior_of_entries_view(dummy_request):
    from ..views.default import entries_view

    response = entries_view(dummy_request)
    assert type(response) == dict
    assert response['entries'][0]['id'] == '1'
