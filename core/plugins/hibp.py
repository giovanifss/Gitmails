import time
import requests
from core.utils.helpers import Helpers
from core.utils.parser import Parser

class HIBP:
    def __init__(self, args, data):
        print("\nStarting Have I Been Pwned plugin...")
        self.args = args
        self.data = data
        all_authors = Parser(args).get_authors(self.data)
        if all_authors:
            self.check_authors(all_authors)

    def check_authors(self, authors):
        for author in authors:
            time.sleep(2)
            self.check_email(author.email)

    def check_email(self, email):
        try:
            url = "https://haveibeenpwned.com/api/v2/breachedaccount/{}?truncateResponse=true&includeUnverified=true".format(email)
            r = requests.get(url)
            if r.status_code == 503:
                Helpers().print_error("hibp: IP got in DDoS protection by CloudFare")
            elif r.status_code == 429:
                Helpers().print_error("hibp: Throttled by HIBP API")
            elif r.text:
                r = r.json()
                print("\n{} leaks:".format(email))
                for leak in r:
                    print("\t- {}".format(leak["Name"]))
                return True
            return False
        except Exception as e:
            print(e)
            return False
