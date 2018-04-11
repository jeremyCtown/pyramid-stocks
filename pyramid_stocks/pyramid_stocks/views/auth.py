from pyramid.httpexceptions import HTTPFound, HTTPBadRequest, HTTPUnauthorized
from pyramid.security import
from pyramid.view import view_config
from sqlalchemy.exc import 





def auth_view(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']

        except KeyError:
            return HTTPBadRequest()

        try: 
            instance = Account(
                username=username,
                email=email,
                password=password,
            )

            headers = remember(request, userid=instance.username)
            # query = request.dbsession.query(Account)
            # is_in_db = query.filter(Account.username == instance.username).one_or_none()
            # request.dbsession.add(instance)
            # if is_in_db is None:
            #     request.dbsession.add(instance)
            # else:
            #     return HTTPConflict('That username already exists. Please try again')

            try:
                request.dbsession.add(instance)
                request.dbsession.flush()
            except IntegrityError:
                return {'error': 'something went wrong'}

            return HTTPFound(location=request.route_url('entries'), headers=headers)

        except DBAPIError:
            return Response(DB_ERR_MSG, content_type='text/plain', status=500)

    if request.method == 'GET':
        try:
            uername = request.GET['username']
            password = request.GET['password']

        except KeyError:
            return{}

        is_authenticated = Account.check_credentials(request, username, password)
        if is_authenticated[0]:
            headers = remember(request, userid=username)
            return HTTPFound(location=request.route_url('entries'), headers=headers)
        else:
            return HTTPUnauthorized('401 - NotAuthorized')

    return HTTPFound(location=request.route_url('home'))

@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(location=request.route_url('home'), headers=headers)