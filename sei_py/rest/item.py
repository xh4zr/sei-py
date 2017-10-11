import json
import sei_py.base
import sei_py.helpers


class ItemAPI(object):
    def __init__(self, http_context, exam_id):
        self._base_url = '{api_url}/exams/{exam_id}/items' \
            .format(api_url=sei_py.base.UrlProvider.getApi(), exam_id=exam_id)
        self._http_context = http_context

    def get(self, **kwargs):
        item_id = kwargs.pop('item_id')
        query_string = sei_py.helpers.generate_query_string(kwargs)
        res = self._http_context.get('{base_url}/{item_id}{query}' \
            .format(base_url=self._base_url, item_id=item_id, query=query_string))
        res_json = res.json()

        if res.status_code >= 400:
            raise sei_py.base.exception.SeiException( \
                res.status_code, res_json.get('messages', []))

        return res_json

    def list(self, **kwargs):
        kwargs['page'] = kwargs.get('page', 1)
        kwargs['per_page'] = kwargs.get('per_page', 30)

        query_string = sei_py.helpers.generate_query_string(kwargs)

        res = self._http_context.get('{base_url}{query}' \
            .format(base_url=self._base_url, query=query_string))
        res_json = res.json()

        if res.status_code >= 400:
            raise sei_py.base.exception.SeiException( \
                res.status_code, res_json.get('messages', []))

        return sei_py.base.Page(res_json.get('results'), res_json.get('total'), \
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
            .format(base_url=self._base_url, item_id=item_id), \
            data=json.dumps(payload), headers={'content-type': 'application/json'})
        if res.status_code < 400:
            return True
        return False

    def create(self, kwargs):
        item_json = kwargs.pop('item_json')
        query_string = sei_py.helpers.generate_query_string(kwargs)

        res = self._http_context.post('{base_url}{query}' \
            .format(base_url=self._base_url, query=query_string), \
            data=json.dumps(item_json), headers={'content-type': 'application/json'})
        res_json = res.json()

        if res.status_code >= 400:
            raise sei_py.base.exception.SeiException( \
                res.status_code, res_json.get('messages', []))

        return res_json

    def save(self, **kwargs):
        is_new = kwargs.pop('is_new', False)
        item_id = kwargs.pop('item_id', None)

        if item_id is not None:
            item_json = kwargs.pop('item_json')
            query_string = sei_py.helpers.generate_query_string(kwargs)
            res = self._http_context.put('{base_url}/{item_id}{query}' \
                .format(base_url=self._base_url, item_id=item_id, query=query_string), \
                data=json.dumps(item_json), headers={'content-type': 'application/json'})
            res_json = res.json()

            if res.status_code >= 400:
                raise sei_py.base.exception.SeiException( \
                    res.status_code, res_json.get('messages', []))

            return res_json
        else:
            return self.create(kwargs)

    def bulk_update(self, **kwargs):
        payload = {
            'field': kwargs.get('field'),
            'items': kwargs.get('items')
        }
        res = self._http_context.post('{base_url}/bulk_update' \
            .format(base_url=self._base_url), \
            data=json.dumps(payload), headers={'content-type': 'application/json'})
        res_json = res.json()

        if res.status_code >= 400:
            raise sei_py.base.exception.SeiException( \
                res.status_code, res_json.get('messages', []))

        return res_json
