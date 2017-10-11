import json
import sei_py.base
import sei_py.helpers
import requests
import python_jwt as jwt


class IntegrationAPI(object):
    def __init__(self, http_context, exam_id, info):
        info = info or {}
        self._base_url = '{api_url}/integrations/{exam_id}'.format(api_url=sei_py.base.UrlProvider.getApi(), exam_id=exam_id)
        self._http_context = http_context
        self._info = {
            'token': info.get('token'),
            'secret': info.get('secret')
        }

    def getCredentials(self):
        res = self._http_context.get('{base}/credentials' \
            .format(base=self._base_url))
        return res.json()

    def get(self):
        return self._info

    def set(self, integrationInfo):
        self._info = integrationInfo

    def verify(self, incoming_token):
        secret = self._info.get('secret')
        if not secret:
            raise sei_py.base.exception.SeiException( \
                False, ['secret not found'])

        header, claims = jwt.verify_jwt(incoming_token, secret, ['HS256'])
        return bool(header and claims)

    @staticmethod
    def static_get(**kwargs):
        exam_id = kwargs.get('exam_id')
        username = kwargs.get('username')
        password = kwargs.get('password')

        errors = []

        if not exam_id:
            errors.append('exam_id is required')
        
        if not username:
            errors.append('username is required')
        
        if not password:
            errors.append('password is required')

        url = '{api_url}/integrations/{exam_id}/credentials'.format(api_url=sei_py.base.UrlProvider.getApi(), exam_id=exam_id)
        if errors:
            raise sei_py.base.exception.SeiException( \
                False, errors)
        else:
            res = requests.get(url, auth=requests.auth.HTTPBasicAuth(username, password))
            res_json = res.json()
            if res.status_code >= 400:
                raise sei_py.base.exception.SeiException( \
                    res.status_code, res_json.get('messages', []))
            return res_json
