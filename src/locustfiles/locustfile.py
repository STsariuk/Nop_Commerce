from locust import HttpUser, between
from locust.env import Environment
from config.config import TestConfig


from src.locustfiles.tests.test_add_product import UserPurchase


class TestExecution(HttpUser):

    conf = TestConfig()
    wait_time = between(conf.wait_time_min, conf.wait_time_max)
    host = conf.api_url
    tasks = {UserPurchase: 1}


if __name__ == '__main__':
    env = Environment(user_classes=[TestExecution])
    TestExecution(env).run()
