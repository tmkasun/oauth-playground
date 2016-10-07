import requests
from requests_oauthlib import OAuth2Session
from flask import Flask, request, redirect, session, url_for
from flask.json import jsonify
import os

os.environ[
    'OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # Because we don't have trusted certificate in the server(Only for demo)

app = Flask(__name__)

# This information is obtained upon registration of a new Application in WSO2 API Manager
# You can add application from here: https://localhost:9443/store/site/pages/application-add.jag

client_id = "kB9W2k3wJEofjIlUdnjoWjQ_P_Qa"
client_secret = "OTSI4TQRBfSFfzbNdmEGaqg1eqUa"
scope = "all"

host = "localhost"
port = 8243

authorization_base_url = 'https://{}:{}/authorize'.format(host, port)
token_url = 'https://{}:{}/token'.format(host, port)
callback_url = "http://{}:5000/callback".format(host)


@app.route("/")
def demo():
    """Step 1: User Authorization.

    Redirect the user/resource owner to the OAuth provider (i.e. WSO2 API Manager)
    using an URL with OAuth parameters.
    """
    wso2_apim = OAuth2Session(client_id, redirect_uri=callback_url, scope=scope)
    authorization_url, state = wso2_apim.authorization_url(authorization_base_url)

    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state
    return redirect(authorization_url)


# Step 2: User authorization, this happens on the provider. In the above redirect call user(you) will be redirect to
# WSO2 APIM request authorization page, Where user(you) will be asked whether to grant permission for the
# requested resource or reject the request. With User's(your) action. WSO2 APIM (Service Provider) will redirect the
# client back to it's designated callback URL.That redirect request will hit the following method.

@app.route("/callback", methods=["GET"])
def callback():
    """ Step 3: Retrieving an access token.

    The user has been redirected back from the provider to your registered
    callback URL. With this redirection comes an authorization code included
    in the redirect URL. We will use that to obtain an access token.
    """
    wso2_apim = OAuth2Session(client_id, state=session['oauth_state'], redirect_uri=callback_url)
    token = wso2_apim.fetch_token(token_url, client_secret=client_secret,
                                  authorization_response=request.url, verify=False)  # verify=False Because we don't
    # have trusted certificate in the server(Only for demo)

    # At this point you can fetch protected resources but lets save
    # the token and show how this is done from a persisted token
    # in /profile.
    session['oauth_token'] = token
    return redirect(url_for('.consume_service'))


@app.route("/consume_service", methods=["GET"])
def consume_service():
    """Fetching a protected resource using an OAuth 2 token.
    """
    # print("Done!")
    # print("Client access key is = {}".format(session['oauth_token']))
    access_token = session['oauth_token']['access_token']
    endpoint = "https://localhost:8243/t/knnect.com/ebill_new/1.0.0/ebill"
    headers = {
        "Authorization": "{type} {value}".format(type="Bearer", value=access_token)
    }
    applications = requests.get(endpoint, headers=headers, verify=False)
    if not applications.ok:
        message = "ERROR: Something went wrong: {}".format(applications.content)
        print(message)
        return jsonify("'Error': {}".format(message))
    return jsonify(applications.json())


if __name__ == "__main__":
    # This allows us to use a plain HTTP callback
    os.environ['DEBUG'] = "1"
    app.secret_key = os.urandom(24)
    app.run(debug=True)
