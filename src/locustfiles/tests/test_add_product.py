from locust import task
import logging

from src.locustfiles.tasksets.main_page import HomePage


class UserPurchase(HomePage):

    def __init__(self, parent):
        super().__init__(parent)

    @task
    def new(self):
        self.get_main_page()
