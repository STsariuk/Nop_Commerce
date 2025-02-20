import logging

from locust import SequentialTaskSet

logger = logging.getLogger('locust_log')
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('locust_test.log')
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


class BaseTaskSet(SequentialTaskSet):

    def __init__(self, parent):
        super().__init__(parent)
        self.success_status_codes = (200, 201, 202, 204, 300, 301, 302, 304)
        # self.client.headers = {'Content-Type': 'application/json'}
        self.client.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
            "Referer": "https://demo.nopcommerce.com/",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            'Content-type': 'application/x-www-form-urlencoded',
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
        }
        self.cookies = {
            '.Nop.Antiforgery': self.parent.conf.nop_antiforgery,
            # '.Nop.Culture': 'c%3Den-US%7Cuic%3Den-US',
            '.Nop.Customer': self.parent.conf.nop_customer,
            'cf_clearance': self.parent.conf.cf_clearance
        }

    def validate_response(self, response):
        if response.status_code in self.success_status_codes:
            response.success()
        else:
            response.failure(response.status_code)
            logger.error(
                f'error occurred: {response.request_meta["request_type"]}, '
                f'path {response.request_meta["name"]}, '
                f'response status {response.status_code}, '
                f'response content {response.content}'
            )
