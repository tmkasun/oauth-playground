from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from oauth_playground.configs import Configs
from rest_framework.renderers import JSONRenderer
from requests_oauthlib import OAuth2Session

client_secret = "vGk7XPnf0tLM8gfihT_YLQQO9c4a"

host = "localhost"
port = 8243

authorization_base_url = 'https://{}:{}/authorize'.format(host, port)
token_url = 'https://{}:{}/token'.format(host, port)
callback_url = "http://{}:5000/callback".format(host)
import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@require_POST
def submit(request):
    """Step 1: User Authorization.

    Redirect the user/resource owner to the OAuth provider (i.e. WSO2 API Manager)
    using an URL with OAuth parameters.
    """
    client_id = request.POST.get('client_id')
    callback_url = Configs.get_callback_url()
    scope = request.POST.get('scope')
    auth_endpoint = request.POST.get('auth_endpoint')
    auth_endpoint = auth_endpoint if auth_endpoint else Configs.get_default_auth_endpoint_url()

    wso2_apim = OAuth2Session(client_id, redirect_uri=callback_url, scope=scope)
    authorization_url, state = wso2_apim.authorization_url(auth_endpoint)

    # State is used to prevent CSRF, keep this for later.
    request.session['oauth_state'] = state
    request.session['oauth_client_id'] = client_id
    request.session['oauth_callback_url'] = callback_url
    return redirect(authorization_url)


def callback(request):
    """ Step 3: Retrieving an access token.

    The user has been redirected back from the provider to your registered
    callback URL. With this redirection comes an authorization code included
    in the redirect URL. We will use that to obtain an access token.
    """
    auth_token = request.GET.get('code')
    request.session['oauth_response_url'] = request.build_absolute_uri()
    cont = {'auth_token': auth_token}
    return render(request, 'oauth/callback.html', cont)

@require_POST
def request_access_token(request):
    auth_response = request.session['oauth_response_url']
    client_id = request.session['oauth_client_id']
    callback_url = request.session['oauth_callback_url']
    wso2_apim = OAuth2Session(client_id, state=request.session['oauth_state'], redirect_uri=callback_url)
    token = wso2_apim.fetch_token(token_url, client_secret=client_secret,
                                  authorization_response=auth_response, verify=False)  # verify=False Because we don't
    # have trusted certificate in the server(Only for demo)

    # At this point you can fetch protected resources but lets save
    # the token and show how this is done from a persisted token
    request.session['oauth_token'] = token
    return JSONResponse({'access_token': token})