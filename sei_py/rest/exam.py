import json
import urllib
import sei_py.base
import sei_py.helpers


class ExamAPI(object):
    def __init__(self, http_context, exam_id):
        self._base_url = '{api_url}/exams/{exam_id}'.format(api_url=sei_py.base.UrlProvider.getApi(), exam_id=exam_id)
        self._http_context = http_context

    def get(self, **kwargs):
        query_string = sei_py.helpers.generate_query_string(kwargs)
        res = self._http_context.get('{base}{query}' \
            .format(base=self._base_url, query=query_string))
        return res.json()

    def save(self, exam_json):
        include = []
        if exam_json.get('settings'):
            include.append('settings')

        query_string = sei_py.helpers.generate_query_string({'include': ','.join(include)})

        res = self._http_context.put('{base}{query}' \
            .format(base=self._base_url, query=query_string), \
            data=json.dumps(exam_json), headers={'content-type': 'application/json'})
        return res.json()

    def get_settings(self):
        return self.get(include='settings').get('settings')

    def put_settings(self, settings_json):
        exam_json = {
            'settings': settings_json
        }
        return self.save(exam_json).get('settings')

    def create_lauchpad(self, **kwargs):
        launchpad_json = kwargs.get('launchpad')
        exam = kwargs.get('exam', self.get(include='settings'))
        settings = exam.get('settings')
        launchpads = settings.get('launchpads', [])
        launchpads.append(launchpad_json)
        settings['launchpads'] = launchpads
        new_settings = self.put_settings(settings)
        exam['settings'] = new_settings
        return '{launchpad_url}/{slug}/{name}' \
            .format(launchpad_url=sei_py.base.UrlProvider.getLaunchpad(), slug=exam.get('slug'), \
            name=urllib.parse.quote(launchpad_json.get('name').lower()))
