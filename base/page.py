import math


class Page(object):
    def __init__(self, results, total, page, per_page):
        self.results = results
        self.current_page = page
        self.total_pages = math.ceil(total / per_page)
