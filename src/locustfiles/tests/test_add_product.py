from locust import task
import logging
from random import choice

from src.locustfiles.tasksets.main_page import HomePage
from src.locustfiles.tasksets.category_page import GetCategoryPage
from src.locustfiles.tasksets.product_page import ProductPage
from src.locustfiles.tasksets.add_to_cart import MakePurchase


class UserPurchase(HomePage, GetCategoryPage, ProductPage, MakePurchase):

    def __init__(self, parent):
        super().__init__(parent)
        self.random_menu_item = None
        self.random_product = None
        self.product_data = None

    @task
    def new(self):
        menu_items = self.get_main_page()
        self.random_menu_item = choice(menu_items)

    @task
    def open_menu_item(self):
        category = self.get_category(page_url=self.random_menu_item)
        self.random_product = choice(category)

    @task
    def get_product(self):
        self.product_data = self.product(product_url=self.random_product)

    @task
    def add_product_to_cart(self):
        body = {
            f'addtocart_{self.product_data.get("product_id")}.EnteredQuantity': 1,
            'CountryId': 0,
            'StateProvinceId': 0,
            'ZipPostalCode': '',
            '__RequestVerificationToken': self.product_data.get('request_verification_token')
        }
        self.add(product_id=self.product_data.get("product_id"),
                 quantity='1',
                 payload=body)
