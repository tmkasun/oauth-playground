class Configs(object):
    facebook = {
        'auth_endpoint': "https://www.facebook.com/dialog/oauth",
        'token_endpoint': "https://graph.facebook.com/oauth/access_token",
        'client_id': 'YOUR_APP_ID',  # app_id
        'client_secret': 'YOUR_APP_SECRET',  # app_secret
        'scope': 'public_profile',
        'resource_endpoint': 'https://graph.facebook.com'
    }
    wso2 = {
        'auth_endpoint': "https://localhost:8243/authorize",
        'token_endpoint': "https://localhost:8243/token",
        'client_id': 'YOUR_CONSUMER_KEY',  # Consumer Key
        'client_secret': 'YOUR_CONSUMER_SECRET',  # Consumer Secret
        'scope': 'demo_read',
        'resource_endpoint': 'https://localhost:8243/t/bookstore.com/bookstore/1.0.0'
    }
    commons = {
        'callback_url': 'http://localhost:8000/oauth/callback/'
    }

    @staticmethod
    def get_callback_url():
        return Configs.commons['callback_url']
