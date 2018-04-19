import re
import sys
import requests

class Helpers:
    def request(self, url, method="get", accepts=[200], headers=None, data=None):
        action = getattr(requests, method)
        try:
            result = action(url, headers=headers, data=data)
            if result.text and result.status_code in accepts:
                return result.json()
            return result
        except Exception as e:
            self.print_error(e)
            return False

    def get_last_page(self, url):
        try:
            result = self.request(url, method="head")
            last_url = re.findall("https?://(?:[-\w.]|(?:%[\da-fA-F]{2})).+?(?=>)", result.headers["Link"])[-1]
            return int(last_url.split('=')[-1])
        except Exception as e:
            #self.print_error(e)
            return 0

    def flatten(self, lst):
        if not lst:
            return []
        else:
            return [item for sublist in lst for item in sublist]

    def print_error(self, *args, **kwargs):
        print(*args, file=sys.stderr, **kwargs)
