class Configs(object):
    callback = {
        'host': 'localhost',
        'port': '8000',
        'ssl': False,
        'context': '/oauth/callback'
    }
    auth_endpoint = {
        'host': 'localhost',
        'port': '8243',
        'ssl': True,
        'context': '/authorize'
    }

    @staticmethod
    def get_callback_url():
        return Configs._protocol(Configs.callback['ssl']) + "://" + Configs.callback['host'] + ":" + Configs.callback[
            'port'] + Configs.callback['context']

    @staticmethod
    def get_default_auth_endpoint_url():
        return Configs._protocol(Configs.auth_endpoint['ssl']) + "://" + Configs.auth_endpoint['host'] + ":" + \
               Configs.auth_endpoint[
                   'port'] + Configs.auth_endpoint['context']

    @staticmethod
    def _protocol(ssl=False):
        return 'https' if ssl else 'http'
