import requests
import sei_py.rest


class SeiClient(object):
    def __init__(self, http_context, exam_id):
        self.exam = sei_py.rest.ExamAPI(http_context, exam_id)
        self.delivery = sei_py.rest.DeliveryAPI(http_context, exam_id)
        self.item = sei_py.rest.ItemAPI(http_context, exam_id)


def create_client_with_context(username, password, exam_id, role_secret):
    http_context = requests.Session()
    http_context.auth = requests.auth.HTTPBasicAuth(username, password)
    http_context.headers.update({'x-sei-role-secret': role_secret})

    return SeiClient(http_context, exam_id)
