import json
import urllib
import sei_py.base


class DeliveryAPI(object):
    def __init__(self, http_context, exam_id):
        self._base_url = '{api_url}/exams/{exam_id}/deliveries' \
            .format(api_url=sei_py.base.UrlProvider.getApi(), exam_id=exam_id)
        self._http_context = http_context

    def get(self, **kwargs):
        delivery_id = kwargs.pop('delivery_id')
        query_string = sei_py.helpers.generate_query_string(kwargs)
        res = self._http_context.get('{base_url}/{delivery_id}{query}' \
            .format(base_url=self._base_url, delivery_id=delivery_id, query=query_string))
        return res.json()

    def list(self, **kwargs):
        kwargs['page'] = kwargs.get('page', 1)
        kwargs['per_page'] = kwargs.get('per_page', 30)

        query_string = sei_py.helpers.generate_query_string(kwargs)

        response = self._http_context.get('{base_url}{query}' \
            .format(base_url=self._base_url, query=query_string))
        res = response.json()
        return sei_py.base.Page(res.get('results'), res.get('total'), \
            kwargs.get('page'), kwargs.get('per_page'))

    def get_launch_url(self, **kwargs):
        delivery_id = kwargs.get('delivery_id')
        if delivery_id is None:
            delivery_id = kwargs.get('delivery').get('id')
        res = self._http_context.get('{base_url}/{delivery_id}/get_launch_token' \
            .format(base_url=self._base_url, delivery_id=delivery_id))
        token = res.json().get('launch_token')
        return '{take_url}?launch_token={token}' \
            .format(take_url=sei_py.base.UrlProvider.getTake(), token=token)

    def get_proctor_url(self, **kwargs):
        delivery_id = kwargs.get('delivery_id')
        if delivery_id is None:
            delivery_id = kwargs.get('delivery').get('id')
        res = self._http_context.get('{base_url}/{delivery_id}/get_proctor_token' \
            .format(base_url=self._base_url, delivery_id=delivery_id))
        token = res.json().get('proctor_token')
        return '{proctor_url}/{token}' \
            .format(proctor_url=sei_py.base.UrlProvider.getProctor(), token=token)

    def create(self, delivery_json={}):
        if delivery_json == {}:
            delivery_json['examinee_info'] = {}
        res = self._http_context.post(self._base_url, \
            data=json.dumps(delivery_json), headers={'content-type': 'application/json'})
        return res.json()

    def delete(self, **kwargs):
        delivery_id = kwargs.get('delivery_id')
        if delivery_id is None:
            delivery_id = kwargs.get('delivery').get('id')
        res = self._http_context.delete('{base_url}/{delivery_id}' \
            .format(base_url=self._base_url, delivery_id=delivery_id))
        if res.status_code == 204:
            return True
        return False
