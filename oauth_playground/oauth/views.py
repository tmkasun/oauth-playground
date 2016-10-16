import requests
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from oauth_playground.configs import Configs
from rest_framework.renderers import JSONRenderer
from requests_oauthlib import OAuth2Session
import os
import logging

logger = logging.getLogger(__name__)

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
    user_role = request.POST.get('user_role')
    request.session['user_role'] = user_role

    if user_role == 'wso2_user':
        auth_endpoint = Configs.wso2['auth_endpoint']
        token_endpoint = Configs.wso2['token_endpoint']
        scope = Configs.wso2['scope']
        client_id = Configs.wso2['client_id']
        client_secret = Configs.wso2['client_secret']
    elif user_role == 'facebook_user':
        auth_endpoint = Configs.facebook['auth_endpoint']
        token_endpoint = Configs.facebook['token_endpoint']
        scope = Configs.facebook['scope']
        client_id = Configs.facebook['client_id']
        client_secret = Configs.facebook['client_secret']
    else:
        client_id = request.POST.get('client_id')
        scope = request.POST.get('scope')
        auth_endpoint = request.POST.get('auth_endpoint')
        auth_endpoint = auth_endpoint if auth_endpoint else Configs.wso2['auth_endpoint']
        client_secret = ""
        token_endpoint = ""

    callback_url = Configs.get_callback_url()

    wso2_apim = OAuth2Session(client_id, redirect_uri=callback_url, scope=scope)
    authorization_url, state = wso2_apim.authorization_url(auth_endpoint)

    # State is used to prevent CSRF, keep this for later.
    request.session['oauth_state'] = state
    request.session['oauth_client_id'] = client_id
    request.session['oauth_callback_url'] = callback_url
    request.session['oauth_client_secret'] = client_secret
    request.session['oauth_token_endpoint'] = token_endpoint
    request.session['oauth_scope'] = scope

    logger.info("Redirecting user to : {}".format(auth_endpoint))
    logger.debug("Sessions saved for\n"
                 "oauth_scope : {}\n"
                 "oauth_state : {}\n"
                 "oauth_client_id : {}\n"
                 "oauth_callback_url : {}\n"
                 "oauth_client_secret : {}\n"
                 "oauth_token_endpoint : {}".format(scope, state, client_id, callback_url, client_secret,
                                                    token_endpoint))
    return redirect(authorization_url)


def callback(request):
    """ Step 3: Retrieving an access token.

    The user has been redirected back from the provider to your registered
    callback URL. With this redirection comes an authorization code included
    in the redirect URL. We will use that to obtain an access token.
    """
    auth_token = request.GET.get('code')
    request.session['oauth_response_url'] = request.build_absolute_uri()
    cont = {'auth_token': auth_token, 'user_role': request.session['user_role']}
    logger.info("Authorization code received : {}".format(auth_token))
    return render(request, 'oauth/callback.html', cont)


@require_POST
def request_access_token(request):
    auth_response = request.session['oauth_response_url']
    client_id = request.session['oauth_client_id']
    client_secret = request.session['oauth_client_secret']
    callback_url = request.session['oauth_callback_url']
    token_endpoint = request.session['oauth_token_endpoint']
    scope = request.session['oauth_scope']

    wso2_apim = OAuth2Session(client_id, state=request.session['oauth_state'], redirect_uri=callback_url, scope=scope)
    token = wso2_apim.fetch_token(token_endpoint, client_secret=client_secret,
                                  authorization_response=auth_response, verify=False)  # verify=False Because we don't
    # have trusted certificate in the server(Only for demo)

    # At this point you can fetch protected resources but lets save
    # the token and show how this is done from a persisted token
    request.session['oauth_token'] = token
    cont = {'access_token': JSONRenderer().render(token)}
    logger.info("Access token : {}".format(token))
    return render(request, 'oauth/access_response.html', cont)


@require_POST
def request_resource(request):
    token = request.session['oauth_token']
    user_role = request.session['user_role']
    cont = {'user_role': user_role}
    if user_role == 'wso2_user':
        data = _get_wso2_resource(token)
    elif user_role == 'facebook_user':
        data = _get_facebook_resource(token)
    else:
        data = token
    cont['data'] = data
    return render(request, 'oauth/resource.html', cont)


def _get_wso2_resource(token):
    access_token = token['access_token']
    wso2_conf = Configs.wso2
    wso2_api = wso2_conf['resource_endpoint']
    context = '/book'
    resource = {}
    headers = {
        'Authorization': 'Bearer {}'.format(access_token),
        'Accept': 'application/json'
    }
    request_url = wso2_api + context
    response = requests.get(request_url, headers=headers, verify=False)
    if response.ok:
        resource['books'] = response.json()
    return resource


def _get_facebook_resource(token):
    access_token = token['access_token']
    fb_conf = Configs.facebook
    graph_api = fb_conf['resource_endpoint']
    context = '/me'
    data = {
        'access_token': access_token,
        'redirect': '0'
    }
    request_url = graph_api + context
    response = requests.get(request_url, params=data)
    full_name = response.json()['name']

    context = '/me/picture'
    request_url = graph_api + context
    data['type'] = 'large'
    response = requests.get(request_url, params=data)
    profile_picture = response.json()['data']['url']
    return {'full_name': full_name, 'profile_picture': profile_picture}
