class UrlProvider(object):
    _api = 'https://sei.caveon.com/api'
    _take = 'https://sei.caveon.com/take'
    _proctor = 'https://sei.caveon.com/proctor'
    _launchpad = 'https://sei.caveon.com/launchpad'

    @staticmethod
    def getApi():
        return UrlProvider._api

    @staticmethod
    def getTake():
        return UrlProvider._take

    @staticmethod
    def getProctor():
        return UrlProvider._proctor

    @staticmethod
    def getLaunchpad():
        return UrlProvider._launchpad

    def set_env(self, env):
        if env == 'local':
            UrlProvider._api = 'http://localhost:5000/api'
            UrlProvider._take = 'http://localhost:4000'
            UrlProvider._proctor = 'http://localhost:5000/proctor'
            UrlProvider._launchpad = 'http://localhost:5000/launchpad'

        if env == 'stage':
            UrlProvider._api = 'https://sei-stage.herokuap.com/api'
            UrlProvider._take = 'https://sei-stage.herokuapp.com/take'
            UrlProvider._proctor = 'https://sei-stage.herokuapp.com/proctor'
            UrlProvider._launchpad = 'https://sei-stage.herokuapp.com/launchpad'
