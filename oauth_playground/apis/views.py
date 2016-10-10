from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from rest_framework.renderers import JSONRenderer

from requests_oauthlib import OAuth2Session

client_id = "kB9W2k3wJEofjIlUdnjoWjQ_P_Qa"
client_secret = "OTSI4TQRBfSFfzbNdmEGaqg1eqUa"
scope = "all"

host = "localhost"
port = 8243

authorization_base_url = 'https://{}:{}/authorize'.format(host, port)
token_url = 'https://{}:{}/token'.format(host, port)
callback_url = "http://{}:5000/callback".format(host)


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
@require_POST
def submit(request):
    """Step 1: User Authorization.

    Redirect the user/resource owner to the OAuth provider (i.e. WSO2 API Manager)
    using an URL with OAuth parameters.
    """
    wso2_apim = OAuth2Session(client_id, redirect_uri=callback_url, scope=scope)
    authorization_url, state = wso2_apim.authorization_url(authorization_base_url)

    # State is used to prevent CSRF, keep this for later.
    request.session['oauth_state'] = state
    return redirect(authorization_url)
