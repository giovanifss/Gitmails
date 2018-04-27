import time
import requests
from core.utils.parser import Parser
from core.utils.helpers import Helpers
from core.models.plugin import BasePlugin


class HIBP(BasePlugin):

    def __init__(self, args):
        self.args = args
        self.base_url = "https://haveibeenpwned.com/api/v2/breachedaccount"
        self.url_parameters = "truncateResponse=true&includeUnverified=true"

    def execute(self, data):
        Helpers.print_warning("Starting Have I Been Pwned plugin...", jumpline=True)
        all_emails = Parser(self.args).all_unique_emails(data)
        if all_emails:
            self.check_all_emails(all_emails)
            return True

        return False

    def check_authors(self, authors):
        for author in authors:
            time.sleep(2)
            self.check_email(author.email)

    def check_all_emails(self, emails):
        for email in emails:
            time.sleep(2)
            self.check_email(email)

    def check_email(self, email):
        try:
            url = "{}/{}?{}".format(self.base_url, email, self.url_parameters)
            r = requests.get(url)
            if r.status_code == 503:
                Helpers.print_error("hibp: IP got in DDoS protection by CloudFare")
            elif r.status_code == 429:
                Helpers.print_error("hibp: Throttled by HIBP API")
            elif r.text:
                r = r.json()
                print("\n{} leaks:".format(email))
                for leak in r:
                    print("\t- {}".format(leak["Name"]))
                return True

            return False

        except Exception as e:
            Helpers.print_error(e)
            return False
