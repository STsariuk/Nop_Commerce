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
        self.client.headers = {'Content-Type': 'application/json'}
        self.options_headers = {'Access-Control-Request-Headers': 'content-type, x-yapi-client-guid'}

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
