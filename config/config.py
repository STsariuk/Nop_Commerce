import os

from dotenv import dotenv_values
from pathlib import Path


class TestConfig:

    def __init__(self, env_file: str = '.env'):
        path = Path(__file__).parent.parent / env_file
        config = dotenv_values(path)

        url = config.get('BASE_URL', os.getenv('BASE_URL'))
        env_type = config.get('ENV_TYPE', os.getenv('ENV_TYPE'))
        self.wait_time_min = float(config.get('WAIT_TIME_MIN', os.getenv('WAIT_TIME_MIN')))
        self.wait_time_max = float(config.get('WAIT_TIME_MAX', os.getenv('WAIT_TIME_MAX')))
        self.api_url = f'https://{env_type}.{url}'
        self.nop_antiforgery = config.get('NOP_ANTIFORGERY', os.getenv('NOP_ANTIFORGERY'))
        self.nop_culture = config.get('NOP_CULTURE', os.getenv('NOP_CULTURE'))
        self.nop_customer = config.get('NOP_CUSTOMER', os.getenv('NOP_CUSTOMER'))
        self.cf_clearance = config.get('CF_CLEARANCE', os.getenv('CF_CLEARANCE'))
