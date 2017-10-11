import requests
import sei_py.rest
import sei_py.base


class SeiClient(object):
    def __init__(self, http_context, exam_id, integration_info=None):
        self._http_context = http_context
        self.exam = sei_py.rest.ExamAPI(http_context, exam_id)
        self.delivery = sei_py.rest.DeliveryAPI(http_context, exam_id)
        self.item = sei_py.rest.ItemAPI(http_context, exam_id)
        self.integration = sei_py.rest.IntegrationAPI(http_context, exam_id, integration_info)

    def make_request(self, **kwargs):
        method = kwargs.get('method', 'GET')
        resource = kwargs.get('url')
        headers = kwargs.get('headers', {})
        data = kwargs.get('data', {})

        if not resource or '//' in resource:
            raise sei_py.base.exception.SeiException( \
                False, ['url without origin is required'])

        result = self._http_context.request(method, sei_py.base.UrlProvider.getApi() + resource, headers=headers, data=data)
        return result.json()


def create_client_with_context(username, password, exam_id, role_secret):
    return create_client_with_basic_auth(username, password, exam_id, role_secret)

def create_client_with_basic_auth(username, password, exam_id, role_secret):
    http_context = requests.Session()
    http_context.auth = requests.auth.HTTPBasicAuth(username, password)
    http_context.headers.update({'x-sei-role-secret': role_secret})

    return SeiClient(http_context, exam_id)

def create_client(**kwargs):
    integration_info = sei_py.rest.IntegrationAPI.static_get(**kwargs)

    return create_client_with_integration(**integration_info)

def create_client_with_integration(**kwargs):
    token = kwargs.get('token')
    exam_id = kwargs.pop('exam_id')

    http_context = requests.Session()
    http_context.headers.update({'Authorization': 'Bearer ' + token})

    return SeiClient(http_context, exam_id, kwargs)
