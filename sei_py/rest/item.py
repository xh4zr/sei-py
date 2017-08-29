import json
import sei_py.base


class ItemAPI(object):
    def __init__(self, http_context, exam_id):
        self._base_url = '{api_url}/exams/{exam_id}/items' \
            .format(api_url=sei_py.base.UrlProvider.getApi(), exam_id=exam_id)
        self._http_context = http_context

    def _gen_query_string(self, params):
        query = []
        first = True
        for key, value in params.items():
            symbol = '&'
            if first:
                symbol = '?'
                first = False

            query.append('{symbol}{key}={value}'.format(symbol=symbol, key=key, value=value))
        return ''.join(query)

    def get(self, **kwargs):
        item_id = kwargs.pop('item_id')
        query_string = self._gen_query_string(kwargs)
        res = self._http_context.get('{base_url}/{item_id}{query}' \
            .format(base_url=self._base_url, item_id=item_id, query=query_string))
        return res.json()

    def list(self, **kwargs):
        kwargs['page'] = kwargs.get('page', 1)
        kwargs['per_page'] = kwargs.get('per_page', 30)

        query_string = self._gen_query_string(kwargs)

        response = self._http_context.get('{base_url}{query}' \
            .format(base_url=self._base_url, query=query_string))
        res = response.json()
        return sei_py.base.Page(res.get('results'), res.get('total'), \
            kwargs.get('page'), kwargs.get('per_page'))

    def make_live(self, **kwargs):
        version = kwargs.get('version', kwargs.get('item').get('version'))
        if version:
            version_number = version.get('version_number')
        else:
            version_number = kwargs.get('version_number', -1)

        item_id = version.get('item_id')

        payload = {
            'version_number': version_number
        }
        res = self._http_context.post('{base_url}/{item_id}/activate_version' \
            .format(base_url=self._base_url, item_id=item_id, \
            data=json.dumps(payload), headers={'content-type': 'application/json'}))
        if res.status_code < 400:
            return True
        return False

    def create(self, kwargs):
        item_json = kwargs.pop('item_json')
        query_string = self._gen_query_string(kwargs)

        res = self._http_context.post('{base_url}{query}' \
            .format(base_url=self._base_url, query=query_string), \
            data=json.dumps(item_json), headers={'content-type': 'application/json'})
        return res.json()

    def save(self, **kwargs):
        is_new = kwargs.pop('is_new', False)
        item_id = kwargs.pop('item_id')

        if item_id or is_new:
            item_json = kwargs.pop('item_json')
            query_string = self._gen_query_string(kwargs)
            res = self._http_context.put('{base_url}/{item_id}{query}' \
                .format(base_url=self._base_url, item_id=item_id, query=query_string), \
                data=json.dumps(item_json), headers={'content-type': 'application/json'})
            return res.json()
        else:
            return self.create(kwargs)

    def bulk_update(self, **kwargs):
        payload = {
            'field': kwargs.get('field'),
            'items': kwargs.get('items_to_update')
        }
        res = self._http_context.post('{base_url}/bulk_update' \
            .format(base_url=self._base_url), \
            data=json.dumps(payload), headers={'content-type': 'application/json'})
        return res.json()
